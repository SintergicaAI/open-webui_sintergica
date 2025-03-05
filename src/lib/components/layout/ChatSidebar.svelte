<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';

	import { goto } from '$app/navigation';
	import {
		channels,
		chatId,
		chats,
		config,
		currentChatPage,
		mobile,
		pinnedChats,
		scrollPaginationEnabled,
		showArchivedChats,
		showSidebar,
		socket,
		tags,
		temporaryChatEnabled,
		user
	} from '$lib/stores';
	import { getContext, onDestroy, onMount } from 'svelte';
	import {
		getAllTags,
		getChatById,
		getChatList,
		getChatListBySearchText,
		getPinnedChatList,
		importChat,
		toggleChatPinnedStatusById,
		updateChatFolderIdById
	} from '$lib/apis/chats';
	import { createNewFolder, getFolders, updateFolderParentIdById } from '$lib/apis/folders';

	import ArchivedChatsModal from './Sidebar/ArchivedChatsModal.svelte';
	import UserMenu from './Sidebar/UserMenu.svelte';
	import ChatItem from './Sidebar/ChatItem.svelte';
	import Spinner from '../common/Spinner.svelte';
	import Loader from '../common/Loader.svelte';
	import SearchInput from './Sidebar/SearchInput.svelte';
	import Folder from '../common/Folder.svelte';
	import Folders from './Sidebar/Folders.svelte';
	import { createNewChannel, getChannels } from '$lib/apis/channels';
	import ChannelModal from './Sidebar/ChannelModal.svelte';
	import ChannelItem from './Sidebar/ChannelItem.svelte';
	import PencilSquare from '../icons/PencilSquare.svelte';
	import NewFolderButton from '$lib/components/layout/Sidebar/NewFolderButton.svelte';
	import { FolderPlus, MessageCirclePlus, Search, SidebarClose, SidebarOpen } from 'lucide-svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import ChatBubbleOval from '$lib/components/icons/ChatBubbleOval.svelte';
	import Switch from '$lib/components/common/Switch.svelte';
	import MessageCircleDashedPlus from '$lib/components/icons/MessageCircleDashedPlus.svelte';

	const i18n = getContext('i18n');

	const BREAKPOINT = 768;

	export let className = '';

	let navElement;
	let search = '';

	let shiftKey = false;

	let selectedChatId = null;
	let showDropdown = false;
	let showPinnedChat = true;

	let showCreateChannel = false;

	// Pagination variables
	let chatListLoading = false;
	let allChatsLoaded = false;

	let folders = {};

	const initFolders = async () => {
		const folderList = await getFolders(localStorage.token).catch((error) => {
			toast.error(error);
			return [];
		});

		folders = {};

		// First pass: Initialize all folder entries
		for (const folder of folderList) {
			// Ensure folder is added to folders with its data
			folders[folder.id] = { ...(folders[folder.id] || {}), ...folder };
		}

		// Second pass: Tie child folders to their parents
		for (const folder of folderList) {
			if (folder.parent_id) {
				// Ensure the parent folder is initialized if it doesn't exist
				if (!folders[folder.parent_id]) {
					folders[folder.parent_id] = {}; // Create a placeholder if not already present
				}

				// Initialize childrenIds array if it doesn't exist and add the current folder id
				folders[folder.parent_id].childrenIds = folders[folder.parent_id].childrenIds
					? [...folders[folder.parent_id].childrenIds, folder.id]
					: [folder.id];

				// Sort the children by updated_at field
				folders[folder.parent_id].childrenIds.sort((a, b) => {
					return folders[b].updated_at - folders[a].updated_at;
				});
			}
		}
	};

	const createFolder = async (name = $i18n.t('Untitled')) => {
		if (name.trim() === '') {
			toast.error($i18n.t('Folder name cannot be empty.'));
			return;
		}

		const rootFolders = Object.values(folders).filter((folder) => folder.parent_id === null);

		name = getUniqueFolderName(name, rootFolders);

		const tempId = addTemporaryFolder(name);

		const res = await createNewFolder(localStorage.token, name).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			await initFolders();
		} else {
			delete folders[tempId];
		}
	};

	const getUniqueFolderName = (name, rootFolders) => {
		if (!rootFolders.find((folder) => folder.name.toLowerCase() === name.toLowerCase())) {
			return name;
		}
		let i = 1;
		while (rootFolders.find((folder) => folder.name.toLowerCase() === `${name} ${i}`.toLowerCase())) {
			i++;
		}
		return `${name} ${i}`;
	};

	const addTemporaryFolder = (name) => {
		const tempId = uuidv4();
		folders = {
			...folders,
			[tempId]: {
				id: tempId,
				name,
				created_at: Date.now(),
				updated_at: Date.now()
			}
		};
		return tempId;
	};

	const initChannels = async () => {
		await channels.set(await getChannels(localStorage.token));
	};

	const initChatList = async () => {
		// Reset pagination variables
		tags.set(await getAllTags(localStorage.token));
		pinnedChats.set(await getPinnedChatList(localStorage.token));
		initFolders();

		currentChatPage.set(1);
		allChatsLoaded = false;

		if (search) {
			await chats.set(await getChatListBySearchText(localStorage.token, search, $currentChatPage));
		} else {
			await chats.set(await getChatList(localStorage.token, $currentChatPage));
		}

		// Enable pagination
		scrollPaginationEnabled.set(true);
	};

	const loadMoreChats = async () => {
		chatListLoading = true;

		currentChatPage.set($currentChatPage + 1);

		let newChatList = [];

		if (search) {
			newChatList = await getChatListBySearchText(localStorage.token, search, $currentChatPage);
		} else {
			newChatList = await getChatList(localStorage.token, $currentChatPage);
		}

		// once the bottom of the list has been reached (no results) there is no need to continue querying
		allChatsLoaded = newChatList.length === 0;
		await chats.set([...($chats ? $chats : []), ...newChatList]);

		chatListLoading = false;
	};

	let searchDebounceTimeout;

	const searchDebounceHandler = async () => {
		chats.set(null);

		if (searchDebounceTimeout) {
			clearTimeout(searchDebounceTimeout);
		}

		if (search === '') {
			await initChatList();
			return;
		} else {
			searchDebounceTimeout = setTimeout(async () => {
				allChatsLoaded = false;
				currentChatPage.set(1);
				await chats.set(await getChatListBySearchText(localStorage.token, search));

				if ($chats.length === 0) {
					tags.set(await getAllTags(localStorage.token));
				}
			}, 1000);
		}
	};

	const importChatHandler = async (items, pinned = false, folderId = null) => {
		for (const item of items) {
			if (item.chat) {
				await importChat(localStorage.token, item.chat, item?.meta ?? {}, pinned, folderId);
			}
		}

		initChatList();
	};

	const inputFilesHandler = async (files) => {

		for (const file of files) {
			const reader = new FileReader();
			reader.onload = async (e) => {
				const content = e.target.result;

				try {
					const chatItems = JSON.parse(content);
					importChatHandler(chatItems);
				} catch {
					toast.error($i18n.t(`Invalid file format.`));
				}
			};

			reader.readAsText(file);
		}
	};

	const tagEventHandler = async (type, tagName, chatId) => {
		if (type === 'delete') {
			initChatList();
		} else if (type === 'add') {
			initChatList();
		}
	};

	let draggedOver = false;

	const onDragOver = (e) => {
		e.preventDefault();

		// Check if a file is being draggedOver.
		if (e.dataTransfer?.types?.includes('Files')) {
			draggedOver = true;
		} else {
			draggedOver = false;
		}
	};

	const onDragLeave = () => {
		draggedOver = false;
	};

	const onDrop = async (e) => {
		e.preventDefault();

		// Perform file drop check and handle it accordingly
		if (e.dataTransfer?.files) {
			const inputFiles = Array.from(e.dataTransfer?.files);

			if (inputFiles && inputFiles.length > 0) {
				inputFilesHandler(inputFiles); // Handle the dropped files
			}
		}

		draggedOver = false; // Reset draggedOver status after drop
	};

	let touchstart;
	let touchend;

	function checkDirection() {
		const screenWidth = window.innerWidth;
		const swipeDistance = Math.abs(touchend.screenX - touchstart.screenX);
		if (touchstart.clientX < 40 && swipeDistance >= screenWidth / 8) {
			if (touchend.screenX < touchstart.screenX) {
				showSidebar.set(false);
			}
			if (touchend.screenX > touchstart.screenX) {
				showSidebar.set(true);
			}
		}
	}

	const onTouchStart = (e) => {
		touchstart = e.changedTouches[0];
	};

	const onTouchEnd = (e) => {
		touchend = e.changedTouches[0];
		checkDirection();
	};

	const onKeyDown = (e) => {
		if (e.key === 'Shift') {
			shiftKey = true;
		}
	};

	const onKeyUp = (e) => {
		if (e.key === 'Shift') {
			shiftKey = false;
		}
	};

	const onFocus = () => {
	};

	const onBlur = () => {
		shiftKey = false;
		selectedChatId = null;
	};

	onMount(async () => {
		showPinnedChat = localStorage?.showPinnedChat ? localStorage.showPinnedChat === 'true' : true;

		mobile.subscribe((e) => {
			if ($showSidebar && e) {
				showSidebar.set(false);
			}

			if (!$showSidebar && !e) {
				showSidebar.set(true);
			}
		});

		showSidebar.set(!$mobile ? localStorage.sidebar === 'true' : false);
		showSidebar.subscribe((value) => {
			localStorage.sidebar = value;
		});

		await initChannels();
		await initChatList();

		window.addEventListener('keydown', onKeyDown);
		window.addEventListener('keyup', onKeyUp);

		window.addEventListener('touchstart', onTouchStart);
		window.addEventListener('touchend', onTouchEnd);

		window.addEventListener('focus', onFocus);
		window.addEventListener('blur', onBlur);

		const dropZone = document.getElementById('sidebar');

		dropZone?.addEventListener('dragover', onDragOver);
		dropZone?.addEventListener('drop', onDrop);
		dropZone?.addEventListener('dragleave', onDragLeave);
	});

	onDestroy(() => {
		window.removeEventListener('keydown', onKeyDown);
		window.removeEventListener('keyup', onKeyUp);

		window.removeEventListener('touchstart', onTouchStart);
		window.removeEventListener('touchend', onTouchEnd);

		window.removeEventListener('focus', onFocus);
		window.removeEventListener('blur', onBlur);

		const dropZone = document.getElementById('sidebar');

		dropZone?.removeEventListener('dragover', onDragOver);
		dropZone?.removeEventListener('drop', onDrop);
		dropZone?.removeEventListener('dragleave', onDragLeave);
	});
	let showSearchInput = false;
</script>

<ArchivedChatsModal
	bind:show={$showArchivedChats}
	on:change={async () => {
		await initChatList();
	}}
/>

<ChannelModal
	bind:show={showCreateChannel}
	onSubmit={async ({ name, access_control }) => {
		const res = await createNewChannel(localStorage.token, {
			name: name,
			access_control: access_control
		}).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			$socket.emit('join-channels', { auth: { token: $user.token } });
			await initChannels();
			showCreateChannel = false;
		}
	}}
/>

<!-- svelte-ignore a11y-no-static-element-interactions -->

{#if $showSidebar}
	<div
		class=" fixed md:hidden z-40 top-0 right-0 left-0 bottom-0 bg-black/60 w-full min-h-screen h-screen flex justify-center overflow-hidden overscroll-contain"
		on:mousedown={() => {
			showSidebar.set(!$showSidebar);
		}}
	/>
{/if}

<aside
	bind:this={navElement}
	id="sidebar"
	data-state={$showSidebar}
>
	{#if $showSidebar}
		<div
		class="flex flex-col justify-between h-screen max-h-[100dvh] overflow-x-hidden z-50 gap-base {$showSidebar
			? ''
			: 'invisible'}"
	>

		<header class=" flex justify-between items-center self-stretch">
			<h1 class="text-title">{$i18n.t('Chats')}</h1>
			<menu class="button-group-row text-slate-500">
				{#if !showSearchInput}
					<Button
						variant="icon"
						size="sm"
						icon={Search}
						buttonClasses="text-slate-500"
						onClick={() => { showSearchInput = true; }}
					/>
				{/if}
				<Tooltip content={$i18n.t('Create new folder')}>
					<Button variant="icon" size="sm" icon={FolderPlus} buttonClasses="text-slate-500"
									onClick={()=>createFolder()} />
				</Tooltip>
				<Tooltip content={$i18n.t('Temporary Chat')}>
					<Button variant="icon" size="sm" icon={MessageCircleDashedPlus} buttonClasses="text-slate-500 {$temporaryChatEnabled ? 'bg-brand-100 text-brand-500' : ''}"
					onClick={
						async () => {
							temporaryChatEnabled.set(!$temporaryChatEnabled);
							await goto('/dev');
							const newChatButton = document.getElementById('new-chat-button');
							setTimeout(() => {
								newChatButton?.click();
							}, 0);

							// add 'temporary-chat=true' to the URL
							if ($temporaryChatEnabled) {
								history.replaceState(null, '', '?temporary-chat=true');
							} else {
								history.replaceState(null, '', location.pathname);
							}
						}
					}/>
				</Tooltip>
			</menu>
		</header>
		<section class="">
			<Tooltip content={$i18n.t('New Chat')} className="flex flex-1">
				<Button variant="primary" icon={MessageCirclePlus} buttonClasses="w-full inline-flex text-button"
								onClick={async () => { await goto('/dev');
								const newChatButton = document.getElementById('new-chat-button');
								setTimeout(() => {
									newChatButton?.click();
									if ($mobile) {
										showSidebar.set(false);
									}
								}, 0);
								}}>
					Nuevo chat
				</Button>
			</Tooltip>
		</section>

		{#if showSearchInput}
			<section>
				<div class="relative {$temporaryChatEnabled ? 'opacity-20' : ''}">
					{#if $temporaryChatEnabled}
						<div class="absolute z-40 w-full h-full flex justify-center"></div>
					{/if}
					<SearchInput
						bind:value={search}
						on:input={searchDebounceHandler}
						placeholder={$i18n.t('Search')}
					/>
				</div>
			</section>
		{/if}


		<!-- Pinned chats -->
		<section
			class="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden {$temporaryChatEnabled
				? 'opacity-20'
				: ''}"
		>
			{#if !search && $pinnedChats.length > 0}
				<div class="flex flex-col space-y-1">
					<Folder
						className="p-sm"
						bind:open={showPinnedChat}
						on:change={(e) => {
							localStorage.setItem('showPinnedChat', e.detail);
						}}
						on:import={(e) => {
							importChatHandler(e.detail, true);
						}}
						on:drop={async (e) => {
							const { type, id, item } = e.detail;

							if (type === 'chat') {
								let chat = await getChatById(localStorage.token, id).catch((error) => {
									return null;
								});
								if (!chat && item) {
									chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
								}

								if (chat) {
									if (chat.folder_id) {
										const res = await updateChatFolderIdById(
											localStorage.token,
											chat.id,
											null
										).catch((error) => {
											toast.error(error);
											return null;
										});
									}

									if (!chat.pinned) {
										const res = await toggleChatPinnedStatusById(localStorage.token, chat.id);
									}

									initChatList();
								}
							}
						}}
						name={$i18n.t('Pinned')}
					>
						<div
							class=" flex flex-col gap-lg overflow-y-auto scrollbar-hidden"
						>
							{#each $pinnedChats as chat, idx}
								<ChatItem
									className=""
									id={chat.id}
									title={chat.title}
									{shiftKey}
									selected={selectedChatId === chat.id}
									on:select={() => {
										selectedChatId = chat.id;
									}}
									on:unselect={() => {
										selectedChatId = null;
									}}
									on:change={async () => {
										initChatList();
									}}
									on:tag={(e) => {
										const { type, name } = e.detail;
										tagEventHandler(type, name, chat.id);
									}}
								/>
							{/each}
						</div>
					</Folder>
				</div>
			{/if}

			{#if $config?.features?.enable_channels && ($user.role === 'admin' || $channels.length > 0) && !search}
				<Folder
					className="px-2 mt-0.5"
					name={$i18n.t('Channels')}
					dragAndDrop={false}
					onAdd={$user.role === 'admin'
						? () => {
								showCreateChannel = true;
							}
						: null}
					onAddLabel={$i18n.t('Create Channel')}
				>
					{#each $channels as channel}
						<ChannelItem
							{channel}
							onUpdate={async () => {
								await initChannels();
							}}
						/>
					{/each}
				</Folder>
			{/if}

			{#if !search && folders}
				<!-- Folders -->
				<Folders
					{folders}
					on:import={(e) => {
						const { folderId, items } = e.detail;
						importChatHandler(items, false, folderId);
					}}
					on:update={async (e) => {
						initChatList();
					}}
					on:change={async () => {
						initChatList();
					}}
				/>
			{/if}

			<!-- Chats -->
			<Folder
				collapsible={!search}
				className=" px-2 mt-0.5"
				name={$i18n.t('Chats')}
				on:import={(e) => {
					importChatHandler(e.detail);
				}}
				on:drop={async (e) => {
					const { type, id, item } = e.detail;

					if (type === 'chat') {
						let chat = await getChatById(localStorage.token, id).catch((error) => {
							return null;
						});
						if (!chat && item) {
							chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
						}

						if (chat) {
							if (chat.folder_id) {
								const res = await updateChatFolderIdById(localStorage.token, chat.id, null).catch(
									(error) => {
										toast.error(error);
										return null;
									}
								);
							}

							if (chat.pinned) {
								const res = await toggleChatPinnedStatusById(localStorage.token, chat, id);
							}

							initChatList();
						}
					} else if (type === 'folder') {
						if (folders[id].parent_id === null) {
							return;
						}

						const res = await updateFolderParentIdById(localStorage.token, id, null).catch(
							(error) => {
								toast.error(error);
								return null;
							}
						);

						if (res) {
							await initFolders();
						}
					}
				}}
			>
				{#if $temporaryChatEnabled}
					<div class="absolute z-40 w-full h-full flex justify-center"></div>
				{/if}

				<div class=" flex-1 flex flex-col overflow-y-auto scrollbar-hidden">
					<div class="pt-1.5">
						{#if $chats}
							{#each $chats as chat, idx}
								{#if idx === 0 || (idx > 0 && chat.time_range !== $chats[idx - 1].time_range)}
									<div
										class="w-full pl-2.5 text-xs text-slate-400 dark:text-gray-500 font-medium {idx ===
										0
											? ''
											: 'pt-5'} pb-1.5"
									>
										{$i18n.t(chat.time_range)}
										<!-- localisation keys for time_range to be recognized from the i18next parser (so they don't get automatically removed):
							{$i18n.t('Today')}
							{$i18n.t('Yesterday')}
							{$i18n.t('Previous 7 days')}
							{$i18n.t('Previous 30 days')}
							{$i18n.t('January')}
							{$i18n.t('February')}
							{$i18n.t('March')}
							{$i18n.t('April')}
							{$i18n.t('May')}
							{$i18n.t('June')}
							{$i18n.t('July')}
							{$i18n.t('August')}
							{$i18n.t('September')}
							{$i18n.t('October')}
							{$i18n.t('November')}
							{$i18n.t('December')}
							-->
									</div>
								{/if}

								<ChatItem
									className="{selectedChatId === chat.id ? 'bg-brand-50 dark:bg-gray-900' : ''}"
									id={chat.id}
									title={chat.title}
									{shiftKey}
									selected={selectedChatId === chat.id}
									on:select={() => {
										selectedChatId = chat.id;
									}}
									on:unselect={() => {
										selectedChatId = null;
									}}
									on:change={async () => {
										initChatList();
									}}
									on:tag={(e) => {
										const { type, name } = e.detail;
										tagEventHandler(type, name, chat.id);
									}}
								/>
							{/each}

							{#if $scrollPaginationEnabled && !allChatsLoaded}
								<Loader
									on:visible={(e) => {
										if (!chatListLoading) {
											loadMoreChats();
										}
									}}
								>
									<div
										class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2"
									>
										<Spinner className=" size-4" />
										<div class=" ">Loading...</div>
									</div>
								</Loader>
							{/if}
						{:else}
							<div class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2">
								<Spinner className=" size-4" />
								<div class=" ">Loading...</div>
							</div>
						{/if}
					</div>
				</div>
			</Folder>
		</section>

	</div>
	{:else}
			<button
				class="flex justify-center items-center h-full cursor-pointer p-lg flex rounded-sm text-slate-500 hover:bg-brand-50 dark:hover:bg-gray-900 transition"
				on:click={() => {
					showSidebar.set(!$showSidebar);
				}}
			>
				<SidebarOpen size="20"/>
			</button>


	{/if}
</aside>


<!--<aside class="chat__sidebar dark:bg-zinc-950">-->
<!--	<header class=" flex justify-between items-center self-stretch">-->
<!--		<h1 class="text-title">Chats</h1>-->
<!--		<menu class="button-group-row text-slate-500">-->
<!--			<Button variant="icon" size="sm" icon={Search} buttonClasses="text-slate-500" />-->
<!--			<Button variant="icon" size="sm" icon={FolderPlus} buttonClasses="text-slate-500" />-->
<!--			<Button variant="icon" size="sm" icon={MessageCirclePlus} buttonClasses="text-slate-500" />-->
<!--		</menu>-->
<!--	</header>-->

<!--	<div class="flex justify-center">-->
<!--		<Tooltip content={$i18n.t('New Chat')}>-->
<!--			<Button variant="primary" icon={MessageCirclePlus} size="sm" buttonClasses="text-button w-full gap-sm"-->
<!--							on:click={() => { initNewChat(); }}>-->
<!--				Nuevo chat-->
<!--			</Button>-->
<!--		</Tooltip>-->
<!--	</div>-->
<!--	<section class="flex-col justify-center items-center">-->
<!--		<Accordeon title="Anclados" icon={Pin}>-->
<!--			<List items={['Chat pinned 1','Chat pinned 2']} />-->
<!--		</Accordeon>-->
<!--		<Accordeon title="Finanzas" icon={Folder}>-->
<!--			<List items={chatsElements} />-->
<!--		</Accordeon>-->


<!--	</section>-->
<!--</aside>-->
<style lang="scss">

  .chat__sidebar {
    @apply flex flex-col flex-grow gap-base border-r border-slate-300 dark:border-zinc-900 w-full py-lg px-base h-full;
  }

  .chat__container {
    @apply flex flex-col gap-base w-full pb-lg h-full;
  }
  .chat__sidebar {
    @apply flex flex-col flex-grow gap-base border-r border-slate-300 dark:border-zinc-900 w-full py-lg px-base h-full ;
  }

  .chat__sidebar.chat__sidebar--collapsed {
    @apply flex flex-col justify-center items-center flex-shrink-0;
  }

  .chat.chat--collapsed {
    display: grid;
    grid-template-columns: 55px 1fr;
  }

  .button-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    @apply gap-lg;

    &.button-group--sm {
      @apply gap-sm
    }

    &.button-group--lg {
      @apply gap-3xl
    }
  }

  .button-group-row {
    display: flex;
    align-items: center;
    justify-content: center;
    @apply gap-lg;
  }
</style>
