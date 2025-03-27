<script lang="ts">
	import Fuse from 'fuse.js';
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';

	import { createEventDispatcher, getContext, onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { knowledge as _knowledge, showSidebar } from '$lib/stores';
	import { updateFileDataContentById, uploadFile } from '$lib/apis/files';
	import {
		addFileToKnowledgeById,
		getKnowledgeBases,
		getKnowledgeById,
		removeFileFromKnowledgeById,
		resetKnowledgeById,
		updateFileFromKnowledgeById,
		updateKnowledgeById
	} from '$lib/apis/knowledge';
	import { settings } from '$lib/stores';


	import { transcribeAudio } from '$lib/apis/audio';
	import { blobToFile, formatFileSize } from '$lib/utils';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import Files from './KnowledgeBase/Files.svelte';
	import AddFilesPlaceholder from '$lib/components/AddFilesPlaceholder.svelte';

	import AddContentMenu from './KnowledgeBase/AddContentMenu.svelte';
	import AddTextContentModal from './KnowledgeBase/AddTextContentModal.svelte';

	import SyncConfirmDialog from '../../common/ConfirmDialog.svelte';
	import RichTextInput from '$lib/components/common/RichTextInput.svelte';
	import Drawer from '$lib/components/common/Drawer.svelte';
	import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';
	import AccessControlModal from '../common/AccessControlModal.svelte';

	import Button from '$lib/components/common/Button/Button.svelte';
	import {
		ArrowLeftFromLine,
		ArrowRightFromLine, Bold,
		Edit,
		Globe, Heading1, Heading2, Italic, List,
		Menu,
		Save,
		Trash2,
		Undo2,
		Upload,
		X
	} from 'lucide-svelte';
	import ButtonFilter from '$lib/components/workspace/Knowledge/KnowledgeBase/Filters.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import SwatchList from '$lib/components/common/Swatch/SwatchList.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import { getUserById } from '$lib/apis/users';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const dispatch = createEventDispatcher();

	const i18n = getContext('i18n');

	let largeScreen = true;

	let pane;
	let showSidepanel = true;
	let minSize = 0;

	type Knowledge = {
		id: string;
		name: string;
		description: string;
		data: {
			file_ids: string[];
		};
		files: any[];
		color: string;
	};

	let fullSize = false;

	let id = null;
	let knowledge: Knowledge | null = null;
	let query = '';

	let showAddTextContentModal = false;
	let showSyncConfirmModal = false;
	let showAccessControlModal = false;

	let inputFiles = null;

	let filteredItems = [];
	$: if (knowledge && knowledge.files) {
		fuse = new Fuse(knowledge.files, {
			keys: ['meta.name', 'meta.description']
		});
	}

	$: if (fuse) {
		filteredItems = query
			? fuse.search(query).map((e) => {
				return e.item;
			})
			: (knowledge?.files ?? []);
	}

	let selectedFile = null;
	let selectedFileId = null;

	$: if (selectedFileId) {
		const file = (knowledge?.files ?? []).find((file) => file.id === selectedFileId);
		if (file) {
			file.data = file.data ?? { content: '' };
			selectedFile = file;
		} else {
			selectedFile = null;
		}
	} else {
		selectedFile = null;
	}

	let fuse = null;
	let debounceTimeout = null;
	let mediaQuery;
	let dragged = false;

	const createFileFromText = (name, content) => {
		const blob = new Blob([content], { type: 'text/plain' });
		const file = blobToFile(blob, `${name}.txt`);

		return file;
	};

	const uploadFileHandler = async (file) => {
		const tempItemId = uuidv4();
		const fileItem = {
			type: 'file',
			file: '',
			id: null,
			url: '',
			name: file.name,
			size: file.size,
			status: 'uploading',
			error: '',
			itemId: tempItemId
		};

		if (fileItem.size == 0) {
			toast.error($i18n.t('You cannot upload an empty file.'));
			return null;
		}

		_knowledge.files = [...(knowledge.files ?? []), fileItem];

		// Check if the file is an audio file and transcribe/convert it to text file
		if (['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/x-m4a'].includes(file['type'])) {
			const res = await transcribeAudio(localStorage.token, file).catch((error) => {
				toast.error(error);
				return null;
			});

			if (res) {
				const blob = new Blob([res.text], { type: 'text/plain' });
				file = blobToFile(blob, `${file.name}.txt`);
			}
		}

		try {
			toast.loading($i18n.t('Uploading file...'));
			const uploadedFile = await uploadFile(localStorage.token, file).then(
				(res) => {
					console.log('Uploading', res);
					return res;
				}
			).catch((e) => {
				toast.error(e);
				return null;
			});

			if (uploadedFile) {
				knowledge.files = knowledge.files.map((item) => {
					if (item.itemId === tempItemId) {
						item.id = uploadedFile.id;
					}

					// Remove temporary item id
					delete item.itemId;
					return item;
				});
				await addFileHandler(uploadedFile.id);
			} else {
				toast.error($i18n.t('Failed to upload file.'));
			}
		} catch (e) {
			toast.error(e);
		}
	};

	const uploadDirectoryHandler = async () => {
		// Check if File System Access API is supported
		const isFileSystemAccessSupported = 'showDirectoryPicker' in window;

		try {
			if (isFileSystemAccessSupported) {
				// Modern browsers (Chrome, Edge) implementation
				await handleModernBrowserUpload();
			} else {
				// Firefox fallback
				await handleFirefoxUpload();
			}
		} catch (error) {
			handleUploadError(error);
		}
	};

	// Helper function to check if a path contains hidden folders
	const hasHiddenFolder = (path) => {
		return path.split('/').some((part) => part.startsWith('.'));
	};

	// Modern browsers implementation using File System Access API
	const handleModernBrowserUpload = async () => {
		const dirHandle = await window.showDirectoryPicker();
		let totalFiles = 0;
		let uploadedFiles = 0;

		// Function to update the UI with the progress
		const updateProgress = () => {
			const percentage = (uploadedFiles / totalFiles) * 100;
			toast.info(`Upload Progress: ${uploadedFiles}/${totalFiles} (${percentage.toFixed(2)}%)`);
		};

		// Recursive function to count all files excluding hidden ones
		async function countFiles(dirHandle) {
			for await (const entry of dirHandle.values()) {
				// Skip hidden files and directories
				if (entry.name.startsWith('.')) continue;

				if (entry.kind === 'file') {
					totalFiles++;
				} else if (entry.kind === 'directory') {
					// Only process non-hidden directories
					if (!entry.name.startsWith('.')) {
						await countFiles(entry);
					}
				}
			}
		}

		// Recursive function to process directories excluding hidden files and folders
		async function processDirectory(dirHandle, path = '') {
			for await (const entry of dirHandle.values()) {
				// Skip hidden files and directories
				if (entry.name.startsWith('.')) continue;

				const entryPath = path ? `${path}/${entry.name}` : entry.name;

				// Skip if the path contains any hidden folders
				if (hasHiddenFolder(entryPath)) continue;

				if (entry.kind === 'file') {
					const file = await entry.getFile();
					const fileWithPath = new File([file], entryPath, { type: file.type });

					await uploadFileHandler(fileWithPath);
					uploadedFiles++;
					updateProgress();
				} else if (entry.kind === 'directory') {
					// Only process non-hidden directories
					if (!entry.name.startsWith('.')) {
						await processDirectory(entry, entryPath);
					}
				}
			}
		}

		await countFiles(dirHandle);
		updateProgress();

		if (totalFiles > 0) {
			await processDirectory(dirHandle);
		}
	};

	// Firefox fallback implementation using traditional file input
	const handleFirefoxUpload = async () => {
		return new Promise((resolve, reject) => {
			// Create hidden file input
			const input = document.createElement('input');
			input.type = 'file';
			input.webkitdirectory = true;
			input.directory = true;
			input.multiple = true;
			input.style.display = 'none';

			// Add input to DOM temporarily
			document.body.appendChild(input);

			input.onchange = async () => {
				try {
					const files = Array.from(input.files)
						// Filter out files from hidden folders
						.filter((file) => !hasHiddenFolder(file.webkitRelativePath));

					let totalFiles = files.length;
					let uploadedFiles = 0;

					// Function to update the UI with the progress
					const updateProgress = () => {
						const percentage = (uploadedFiles / totalFiles) * 100;
						toast.info(
							`Upload Progress: ${uploadedFiles}/${totalFiles} (${percentage.toFixed(2)}%)`
						);
					};

					updateProgress();

					// Process all files
					for (const file of files) {
						// Skip hidden files (additional check)
						if (!file.name.startsWith('.')) {
							const relativePath = file.webkitRelativePath || file.name;
							const fileWithPath = new File([file], relativePath, { type: file.type });

							await uploadFileHandler(fileWithPath);
							uploadedFiles++;
							updateProgress();
						}
					}

					// Clean up
					document.body.removeChild(input);
					resolve();
				} catch (error) {
					reject(error);
				}
			};

			input.onerror = (error) => {
				document.body.removeChild(input);
				reject(error);
			};

			// Trigger file picker
			input.click();
		});
	};

	// Error handler
	const handleUploadError = (error) => {
		if (error.name === 'AbortError') {
			toast.info('Directory selection was cancelled');
		} else {
			toast.error('Error accessing directory');
			console.error('Directory access error:', error);
		}
	};

	// Helper function to maintain file paths within zip
	const syncDirectoryHandler = async () => {
		if ((knowledge?.files ?? []).length > 0) {
			const res = await resetKnowledgeById(localStorage.token, id).catch((e) => {
				toast.error(e);
			});

			if (res) {
				knowledge = res;
				toast.success($i18n.t('Knowledge reset successfully.'));

				// Upload directory
				uploadDirectoryHandler();
			}
		} else {
			uploadDirectoryHandler();
		}
	};

	const addFileHandler = async (fileId) => {
		const updatedKnowledge = await addFileToKnowledgeById(localStorage.token, id, fileId).catch(
			(e) => {
				toast.error(e);
				return null;
			}
		);

		if (updatedKnowledge) {
			knowledge = updatedKnowledge;
			toast.success($i18n.t('File added successfully.'));
		} else {
			toast.error($i18n.t('Failed to add file.'));
			knowledge.files = knowledge.files.filter((file) => file.id !== fileId);
		}
	};

	const deleteFileHandler = async (fileId) => {
		const updatedKnowledge = await removeFileFromKnowledgeById(
			localStorage.token,
			id,
			fileId
		).catch((e) => {
			toast.error(e);
		});

		if (updatedKnowledge) {
			knowledge = updatedKnowledge;
			toast.success($i18n.t('File removed successfully.'));
		}
	};

	const updateFileContentHandler = async () => {
		const fileId = selectedFile.id;
		const content = selectedFile.data.content;

		const res = updateFileDataContentById(localStorage.token, fileId, content).catch((e) => {
			toast.error(e);
		});

		const updatedKnowledge = await updateFileFromKnowledgeById(
			localStorage.token,
			id,
			fileId
		).catch((e) => {
			toast.error(e);
		});

		if (res && updatedKnowledge) {
			knowledge = updatedKnowledge;
			toast.success($i18n.t('File content updated successfully.'));
		}
	};

	const changeDebounceHandler = () => {
		if (debounceTimeout) {
			clearTimeout(debounceTimeout);
		}

		debounceTimeout = setTimeout(async () => {
			if (knowledge.name.trim() === '' || knowledge.description.trim() === '') {
				toast.error($i18n.t('Please fill in all fields.'));
				return;
			}

			const res = await updateKnowledgeById(localStorage.token, id, {
				...knowledge,
				name: knowledge.name,
				description: knowledge.description,
				access_control: knowledge.access_control
			}).catch((e) => {
				toast.error(e);
			});

			if (res) {
				toast.success($i18n.t('Knowledge updated successfully'));
				_knowledge.set(await getKnowledgeBases(localStorage.token));
			}
		}, 1000);
	};

	const handleMediaQuery = async (e) => {
		if (e.matches) {
			largeScreen = true;
		} else {
			largeScreen = false;
		}
	};

	const onDragOver = (e) => {
		e.preventDefault();

		// Check if a file is being draggedOver.
		if (e.dataTransfer?.types?.includes('Files')) {
			dragged = true;
		} else {
			dragged = false;
		}
	};

	const onDragLeave = () => {
		dragged = false;
	};

	const onDrop = async (e) => {
		e.preventDefault();
		dragged = false;

		if (e.dataTransfer?.types?.includes('Files')) {
			if (e.dataTransfer?.files) {
				const inputFiles = e.dataTransfer?.files;

				if (inputFiles && inputFiles.length > 0) {
					for (const file of inputFiles) {
						await uploadFileHandler(file);
					}
				} else {
					toast.error($i18n.t(`File not found.`));
				}
			}
		}
	};

	async function mapUsersFromKnowledge(knowledge) {
		if (!knowledge || !knowledge.files || !Array.isArray(knowledge.files)) {
			console.error("La estructura del conocimiento no es válida.");
			return [];
		}

		// Extraer los user_id únicos de los archivos
		const userIds = knowledge.files
			.map(file => file.user_id)
			.filter((id, index, array) => id && array.indexOf(id) === index); // Filtrar nulos y duplicados

		const userMap = {};

		const users = await Promise.all(
			userIds.map(async (userId) => {
				try{
					const userData = await getUserById(localStorage.token, userId);
						userMap[userId] = userData.name
				}catch (e){
					userMap[userId] = 'Desconocido'
				}
			})
		);

		const enrichedFiles = knowledge.files.map(file => ({
			...file,
				user_name: userMap[file.user_id] || 'Desconocido'
		}))

		return {
			...knowledge,
			files: enrichedFiles
		}
	}

	onMount(async () => {
		// listen to resize 1024px
		mediaQuery = window.matchMedia('(min-width: 1024px)');

		mediaQuery.addEventListener('change', handleMediaQuery);
		handleMediaQuery(mediaQuery);

		// Select the container element you want to observe
		const container = document.getElementById('collection-container');

		// initialize the minSize based on the container width
		minSize = !largeScreen ? 100 : Math.floor((300 / container.clientWidth) * 100);

		// Create a new ResizeObserver instance
		const resizeObserver = new ResizeObserver((entries) => {
			for (let entry of entries) {
				const width = entry.contentRect.width;
				// calculate the percentage of 300
				const percentage = (300 / width) * 100;
				// set the minSize to the percentage, must be an integer
				minSize = !largeScreen ? 100 : Math.floor(percentage);

				if (showSidepanel) {
					if (pane && pane.isExpanded() && pane.getSize() < minSize) {
						pane.resize(minSize);
					}
				}
			}
		});

		// Start observing the container's size changes
		resizeObserver.observe(container);

		if (pane) {
			pane.expand();
		}

		id = $page.params.id;

		const res = await getKnowledgeById(localStorage.token, id).catch((e) => {
			toast.error(e);
			return null;
		});

		if (res) {
			knowledge = res;
			const enrichedKnowledge = await mapUsersFromKnowledge(knowledge);
			console.log('Knowledge by id:',enrichedKnowledge);
			knowledge = enrichedKnowledge;
		} else {
			goto('/workspace/knowledge');
		}

		const dropZone = document.querySelector('body');
		dropZone?.addEventListener('dragover', onDragOver);
		dropZone?.addEventListener('drop', onDrop);
		dropZone?.addEventListener('dragleave', onDragLeave);
	});

	onDestroy(() => {
		mediaQuery?.removeEventListener('change', handleMediaQuery);
		const dropZone = document.querySelector('body');
		dropZone?.removeEventListener('dragover', onDragOver);
		dropZone?.removeEventListener('drop', onDrop);
		dropZone?.removeEventListener('dragleave', onDragLeave);
	});
	let filters = ['documents', 'images', 'videos', 'audio', 'spreadsheets', 'presentations'];
</script>

{#if dragged}
	<div
		class="fixed {$showSidebar
			? 'left-0 md:left-[260px] md:w-[calc(100%-260px)]'
			: 'left-0'}  w-full h-full flex z-50 touch-none pointer-events-none"
		id="dropzone"
		role="region"
		aria-label="Drag and Drop Container"
	>
		<div class="absolute w-full h-full backdrop-blur bg-gray-800/40 flex justify-center">
			<div class="m-auto pt-64 flex flex-col justify-center">
				<div class="max-w-md">
					<AddFilesPlaceholder>
						<div class=" mt-2 text-center text-sm dark:text-gray-200 w-full">
							Drop any files here to add to my documents
						</div>
					</AddFilesPlaceholder>
				</div>
			</div>
		</div>
	</div>
{/if}

<SyncConfirmDialog
	bind:show={showSyncConfirmModal}
	message={$i18n.t(
		'This will reset the knowledge base and sync all files. Do you wish to continue?'
	)}
	on:confirm={() => {
		syncDirectoryHandler();
	}}
/>

<AddTextContentModal
	bind:show={showAddTextContentModal}
	on:submit={(e) => {
		const file = createFileFromText(e.detail.name, e.detail.content);
		uploadFileHandler(file);
	}}
/>

<input
	id="files-input"
	bind:files={inputFiles}
	type="file"
	multiple
	hidden
	on:change={async () => {
		if (inputFiles && inputFiles.length > 0) {
			for (const file of inputFiles) {
				await uploadFileHandler(file);
			}

			inputFiles = null;
			const fileInputElement = document.getElementById('files-input');

			if (fileInputElement) {
				fileInputElement.value = '';
			}
		} else {
			toast.error($i18n.t(`File not found.`));
		}
	}}
/>

<div class="{!fullSize ? 'layout' : 'layout--full-size'} w-full translate-y-1" id="collection-container">
	{#if id && knowledge}
		<AccessControlModal
			bind:show={showAccessControlModal}
			bind:accessControl={knowledge.access_control}
			onChange={() => {
				changeDebounceHandler();
			}}
		/>

		<!-- Header -->
		<header class="header w-full py-lg px-base border-b border-slate-300">
			<div class=" flex w-full">
					<div class="flex items-center justify-between w-full dark:border-gray-850">
						<div class="flex items-center gap-lg">
							<Button variant="icon" size="sm" icon={Undo2} buttonClasses="text-slate-500" />
							<span class="text-left w-full text-title text-slate-400 font-primary bg-transparent outline-none">Bases de conocimiento ></span>
							<Pill text={knowledge.name} pillColor={$settings?.knowledgeColor}/>
						</div>

						<div class="flex items-center gap-lg">
							<p class="font-[Archivo] text-sm text-slate-400">{$i18n.t('files')}: {knowledge.files.length}</p>
							<span class="text-label text-slate-400">|</span>
						<p class="font-[Archivo] text-sm text-slate-400">
							{$i18n.t('size')}:
							{formatFileSize(knowledge.files.reduce((total, file) => total + file.meta.size, 0))}
						</p>
						<span class="text-label text-slate-400">|</span>
						<p class="font-[Archivo] text-sm text-slate-400">
							{$i18n.t('last modified')}:
							{new Date(Math.max(...knowledge.files.map(file => new Date(file.updated_at * 1000).getTime()))).toLocaleDateString('es-ES', {
								year: 'numeric',
								month: 'long',
								day: 'numeric',
							})}

						</p>
						<Avatar initials="AO" />
						<Button variant="icon" size="sm" icon={Trash2} />
					</div>
				</div>
			</div>
		</header>

		<!-- Action panel toggle button-->
		{#if fullSize}
			<div class="side-toggle flex items-center">
				<Button variant="icon" size="base" icon={ArrowRightFromLine} buttonClasses="text-slate-500" onClick={()=>{fullSize = false;}} />
			</div>
		{/if}
		<!-- Results -->
		<div class="content {largeScreen ? 'flex-shrink-0 w-full' : 'flex-1'}
			flex
			flex-col
			p-3xl
			gap-lg
			dark:border-gray-850"
		>
			<div class="flex w-full px-1">
				<div class="flex-1">
					<label for="knowledge-name" class="text-label text-slate-400">{$i18n.t('Knowledge base name')}</label>
					<input
						id="knowledge-name"
						type="text"
						class="text-left w-full text-black dark:text-white text-title bg-transparent outline-none"
						bind:value={knowledge.name}
						placeholder="Knowledge Name"
						on:input={() => {
									changeDebounceHandler();
								}}
					/>
					<label for="knowledge-description" class="text-label text-slate-400">{$i18n.t('Description')}</label>
					<input
						id="knowledge-description"
						type="text"
						class="text-left text-base w-full text-slate-500 bg-transparent outline-none"
						bind:value={knowledge.description}
						placeholder="Knowledge Description"
						on:input={() => {
								changeDebounceHandler();
							}}
					/>
				</div>

				<div class="flex-1">
					<SwatchList key={knowledge.id}/>
				</div>

			</div>

			<div class="flex flex-wrap justify-between w-full">
				<div class="flex justify-between items-center w-full mb-2">
					<h3 class="flex text-label text-slate-400">Añadir archivo</h3>
					<h3 class="flex justify-end text-right text-label text-slate-400">{'Permisos'}</h3>
				</div>

				<div class="flex justify-between items-center w-full mb-2">
					<div class="flex justify-between gap-sm">
						<Button variant="primary" icon={Upload} onClick={() => {document.getElementById('files-input').click();}}>
							{$i18n.t('Subir archivos')}</Button>
						<Button variant="outline-primary" icon={Edit} onClick={()=>{showAddTextContentModal = true;}}>
							{$i18n.t('Escribir nuevo archivo')}
						</Button>
						<Button variant="outline-primary" icon={Globe}>{'Añadir URL'}</Button>
					</div>
					<Button variant="outline-primary" icon={Edit} onClick={() => {
									showAccessControlModal = true;
								}}>Administrar accesos
					</Button>
				</div>
			</div>

			<div class=" flex flex-col w-full rounded-lg h-full">
				<div class="w-full flex justify-start gap-sm flex-col flex-auto self-stretch">
					<div class="flex flex-wrap flex-col w-full">

						<div class="flex justify-between items-center w-full mb-2">
							<h3 class="text-label text-slate-400">{$i18n.t('Filters')}</h3>
							<h3 class="text-label text-right text-slate-400">{`${filteredItems.length} ${$i18n.t('files')}`}</h3>
						</div>

						<!-- Filters -->
						<div class="self-stretch flex justify-between items-center">
							<div>
								<ButtonFilter />
							</div>
							<!-- Search input-->
							<div class="flex items-center bg-white border border-slate-300 p-base rounded-sm gap-[10px]">
								<input
									class="w-full text-sm pr-4 py-1 outline-none bg-transparent"
									bind:value={query}
									placeholder={$i18n.t('Search Collection')}
									on:focus={() => {selectedFileId = null;}}
								/>
								<div class="self-center ml-1 mr-3">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 20 20"
										fill="currentColor"
										class="w-4 h-4"
									>
										<path
											fill-rule="evenodd"
											d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
											clip-rule="evenodd"
										/>
									</svg>
								</div>
								<div>
									<AddContentMenu
										on:upload={(e) => {
											if (e.detail.type === 'directory') {
												uploadDirectoryHandler();
											} else if (e.detail.type === 'text') {
												showAddTextContentModal = true;
											} else {
												document.getElementById('files-input').click();
											}
										}}
										on:sync={(e) => {
											showSyncConfirmModal = true;
										}}
									/>
								</div>
							</div>
						</div>

					</div>
					{#if filteredItems.length > 0}
						<div class=" flex overflow-y-auto h-full w-full scrollbar-hidden text-xs">
							<Files
								small={true}
								files={filteredItems}
								{selectedFileId}
								on:click={(e) => {
										selectedFileId = selectedFileId === e.detail ? null : e.detail;
									}}
								on:delete={(e) => {
										selectedFileId = null;
										deleteFileHandler(e.detail);
									}}
							/>
						</div>
					{:else}
						<div class="my-3 flex flex-col justify-center text-center text-gray-500 text-xs py-10">
							<div class="flex flex-col items-center">
								<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path
										d="M0 5.39326C0 2.41465 2.41464 0 5.39326 0H34.6067C37.5854 0 40 2.41464 40 5.39326V34.6067C40 37.5854 37.5854 40 34.6067 40H5.39326C2.41465 40 0 37.5854 0 34.6067V5.39326Z"
										fill="#DDF2FB" />
									<path fill-rule="evenodd" clip-rule="evenodd"
												d="M28.3145 18.8764C30.4244 18.8764 32.1347 17.166 32.1347 15.0562C32.1347 12.9463 30.4244 11.2359 28.3145 11.2359C26.2047 11.2359 24.4943 12.9463 24.4943 15.0562C24.4943 17.166 26.2047 18.8764 28.3145 18.8764ZM28.3145 21.573C31.9137 21.573 34.8314 18.6553 34.8314 15.0562C34.8314 11.457 31.9137 8.53931 28.3145 8.53931C24.7154 8.53931 21.7977 11.457 21.7977 15.0562C21.7977 18.6553 24.7154 21.573 28.3145 21.573Z"
												fill="#5DB0F5" />
									<path fill-rule="evenodd" clip-rule="evenodd"
												d="M15.3989 21.1231C15.8951 21.6784 16.7474 21.7263 17.3027 21.2301C17.8579 20.7339 17.9058 19.8815 17.4096 19.3263L13.511 14.9636L17.3899 10.8076C17.898 10.2632 17.8686 9.41002 17.3242 8.90193C16.7799 8.39384 15.9267 8.42326 15.4186 8.96765L11.6043 13.0544L7.97169 8.98935C7.4755 8.43409 6.62314 8.38621 6.06789 8.88239C5.51263 9.37858 5.46474 10.2309 5.96093 10.7862L9.85952 15.1489L5.98062 19.3049C5.47253 19.8493 5.50195 20.7025 6.04633 21.2105C6.59071 21.7186 7.44391 21.6892 7.952 21.1448L11.7663 17.0581L15.3989 21.1231Z"
												fill="#5DB0F5" />
									<path
										d="M19.8876 24.9438C22.556 24.9438 24.7191 27.1069 24.7191 29.7752C24.7191 32.4436 22.556 34.6067 19.8876 34.6067C17.2193 34.6067 15.0562 32.4436 15.0562 29.7752C15.0562 27.1069 17.2193 24.9438 19.8876 24.9438Z"
										fill="#5DB0F5" />
								</svg>
								<h2 class="text-brand-500 text-title">Esta base no tiene archivos</h2>
								<span>Escribe un nuevo documento o carga archivos para continuar</span>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- Action panel -->
		<aside class="sidebar flex flex-shrink-0 flex-col flex-1 py-xl px-2xl
		bg-slate-50 border-slate-300 dark:bg-slate-950 border-l dark:border-slate-700">
			{#if largeScreen}
				<div class="flex-1 flex justify-start w-full h-full max-h-full">
					{#if selectedFile}
						<div class=" flex flex-col w-full h-full max-h-full gap-lg">
							<header class=" flex justify-between items-center flex-shrink-0">
								<div class="flex items-center gap-sm">
									{#if !showSidepanel}
										<div class="-translate-x-2">
											<button
												class="w-full text-left text-sm p-1.5 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"
												on:click={() => {
												pane.expand();
											}}
											>
												<ChevronLeft strokeWidth="2.5" />
											</button>
										</div>
									{/if}
									{#if !fullSize}
										<Button variant="icon" icon={ArrowLeftFromLine} onClick={() => {fullSize = !fullSize;}} buttonClasses="text-slate-500" aria-label="{$i18n.t('Back')}"/>
									{/if}
									<h2 class="text-subtitle text-black dark:text-white">{$i18n.t('Upload files')}</h2>
								</div>
								<div class="flex items-center gap-sm">
									<Button variant="primary" icon={Save} onClick={() => {
											updateFileContentHandler();
										}} aria-label="{$i18n.t('Save')}"/>
									<Button variant="icon" icon={X} onClick={() => {}} class="text-slate-500" aria-label="{$i18n.t('Close')}"/>
								</div>
							</header>
							<section class="flex flex-col gap-sm justify-center items-start self-stretch">
								<h2 class="text-label text-slate-400">Titulo</h2>
								<div class=" flex-1 text-title">
									<a
										class="text-title text-black dark:text-white hover:text-gray-500 hover:dark:text-gray-100 hover:underline flex-grow line-clamp-1"
										href={selectedFile.id ? `/api/v1/files/${selectedFile.id}/content` : '#'}
										target="_blank"
									>
										{selectedFile?.meta?.name}
									</a>
								</div>
							</section>

							<div class=" flex-1 ">
								<div class="flex justify-between items-center w-full mb-2">
									<h2 class=" text-label text-slate-400">{$i18n.t('Content')}</h2>
									{#if selectedFile.data.content.length > 0}
										<div class=" text-label text-slate-400">{selectedFile.data.content.length} {$i18n.t('characters')}</div>
									{/if}
								</div>

								<div class="flex items-center w-full p-xs gap-sm rounded-md bg-white dark:bg-slate-800">
									<Tooltip content={$i18n.t('Bold')}>
										<Button variant="icon" icon={Bold} buttonClasses="text-slate-500" aria-label="{$i18n.t('Bold')}"/>
									</Tooltip>
									<Tooltip content={$i18n.t('Italic')}>
										<Button variant="icon" icon={Italic} buttonClasses="text-slate-500" aria-label="{$i18n.t('Italic')}"/>
									</Tooltip>
									<Tooltip content={$i18n.t('List')}>
										<Button variant="icon" icon={List} buttonClasses="text-slate-500" aria-label="{$i18n.t('List')}"/>
									</Tooltip>
									<Tooltip content={$i18n.t('Heading 1')}>
										<Button variant="icon" icon={Heading1} buttonClasses="text-slate-500" aria-label="{$i18n.t('Heading 1')}"/>
									</Tooltip>
									<Tooltip content={$i18n.t('Heading 2')}>
										<Button variant="icon" icon={Heading2} buttonClasses="text-slate-500" aria-label="{$i18n.t('Heading 2')}"/>
									</Tooltip>
								</div>

								<div
									class=" self-stretch h-[521px] text-black text-base font-normal font-['Archivo'] leading-normal p-sm border border-slate-300 dark:border-slate-700 rounded-sm bg-transparent outline-none overflow-y-auto scrollbar-hidden"
								>
									{#key selectedFile.id}
										<RichTextInput
											className="input-prose-sm"
											bind:value={selectedFile.data.content}
											placeholder={$i18n.t('Add content here')}
											preserveBreaks={true}
										/>
									{/key}
								</div>

							</div>
						</div>
					{:else}
						<div class="h-full flex w-full py-lg px-2xl flex-col items-start gap-lg flex-shrink-0">
							<header class="flex justify-between items-center self-stretch">
								<h2 class="text-subtitle text-black dark:text-white">{$i18n.t('Upload files')}</h2>
								<button class="p-xs" on:click={() => {selectedFileId = null;}}>
									<X class="text-slate-500" size="20"/>
								</button>
							</header>
							<section class="dropzone">
								<p class="text-brand-500 flex justify-between items-center gap-sm">
									{$i18n.t('Drag and drop a file to upload or select a file to view')}
									<Upload size="20"/>
								</p>
								<p class="text-slate-400 text-label">
									pdf, png, jpg or txt | max size
								</p>
							</section>
						</div>
					{/if}
				</div>
			{:else if !largeScreen && selectedFileId !== null}
				<Drawer
					className="h-full"
					show={selectedFileId !== null}
					on:close={() => {
						selectedFileId = null;
					}}
				>
					<div class="flex flex-col justify-start h-full max-h-full p-2">
						<div class=" flex flex-col w-full h-full max-h-full">
							<div class="flex-shrink-0 flex items-center">
								<div class="">
									<button
										class="w-full text-left text-sm p-1.5 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"
										on:click={() => {
											selectedFileId = null;
										}}
									>
										<ChevronLeft strokeWidth="2.5" />
									</button>
								</div>

								<p class=" flex-1 text-xl text-slate-400 line-clamp-1">
									{selectedFile?.meta?.name}
								</p>

								<div>
									<Button variant="primary" icon={Save} onClick={() => {
											updateFileContentHandler();
										}}/>
								</div>
							</div>

							<div
								class=" flex-1 w-full h-full max-h-full py-2.5 px-3.5 text-sm bg-transparent overflow-y-auto scrollbar-hidden"
							>
								{#key selectedFile.id}
									<RichTextInput
										className="input-prose-sm"
										bind:value={selectedFile.data.content}
										placeholder={$i18n.t('Add content here')}
										preserveBreaks={true}
									/>
								{/key}
							</div>
						</div>
					</div>
				</Drawer>
			{/if}
		</aside>
	{:else}
		<Spinner />
	{/if}
</div>

<style>
    .layout{
        display: grid;
        grid-template-areas:
				"header header"
				"content sidebar";
        grid-template-columns: 1fr minmax(437px, auto);
        grid-template-rows: auto 1fr;
    }

		.layout--full-size {
				display: grid;
				grid-template-areas:
				"header header"
				"toggle sidebar";
				grid-template-columns: auto 1fr;
				grid-template-rows: auto 1fr;
		}

		.layout--full-size .content {
				display: none;
		}

    .header {
        grid-area: header;
    }

    .content {
        grid-area: content;
    }

    .sidebar {
        grid-area: sidebar;
    }

		.layout--full-size .side-toggle {
				padding: var(--spacing-base);
				grid-area: toggle;
		}

		.dropzone {
				@apply flex flex-col gap-sm justify-center items-center flex-shrink-0 self-stretch p-lg border border-dashed h-[641px]
        rounded-lg border-brand-500 text-button text-center bg-brand-50 dark:bg-brand-900 text-brand-500 dark:text-gray-700;
		}
</style>
