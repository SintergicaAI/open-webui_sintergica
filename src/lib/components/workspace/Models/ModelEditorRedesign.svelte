<script lang="ts">
	import { onMount, getContext, tick } from 'svelte';
	import { models, tools, functions, knowledge as knowledgeCollections, user, settings } from '$lib/stores';

	import { Image, LibraryBig, Save, X } from 'lucide-svelte';

	import AdvancedParams from '$lib/components/chat/Settings/Advanced/AdvancedParams.svelte';
	import Tags from '$lib/components/common/Tags.svelte';
	import Knowledge from '$lib/components/workspace/Models/Knowledge.svelte';
	import ToolsSelector from '$lib/components/workspace/Models/ToolsSelector.svelte';
	import FiltersSelector from '$lib/components/workspace/Models/FiltersSelector.svelte';
	import ActionsSelector from '$lib/components/workspace/Models/ActionsSelector.svelte';
	import Capabilities from '$lib/components/workspace/Models/Capabilities.svelte';
	import Textarea from '$lib/components/common/Textarea.svelte';
	import { getTools } from '$lib/apis/tools';
	import { getFunctions } from '$lib/apis/functions';
	import { getKnowledgeBases } from '$lib/apis/knowledge';
	import AccessControl from '../common/AccessControl.svelte';
	import { toast } from 'svelte-sonner';
	import SwatchList from '$lib/components/common/Swatch/SwatchList.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';

	const colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];

	function getRandomColor() {
		const randomIndex = Math.floor(Math.random() * colors.length);
		return colors[randomIndex];
	}

	let randomColor = getRandomColor();
	const i18n = getContext('i18n');

	export let onSubmit: Function;
	export let onBack: null | Function = null;

	export let model = null;
	export let edit = false;

	export let preset = true;

	let loading = false;
	let success = false;

	let filesInputElement;
	let inputFiles;

	let showAdvanced = false;
	let showPreview = false;

	let loaded = false;

	// ///////////
	// model
	// ///////////

	let id = '';
	let name = '';

	$: if (!edit) {
		if (name) {
			id = name
				.replace(/\s+/g, '-')
				.replace(/[^a-zA-Z0-9-]/g, '')
				.toLowerCase();
		}
	}

	let info = {
		id: '',
		base_model_id: null,
		name: '',
		meta: {
			profile_image_url: '/static/favicon.png',
			description: '',
			suggestion_prompts: null,
			tags: []
		},
		params: {
			system: ''
		}
	};

	let params = {
		system: ''
	};
	let capabilities = {
		vision: true,
		usage: undefined,
		citations: true
	};

	let knowledge = [];
	let toolIds = [];
	let filterIds = [];
	let actionIds = [];

	let accessControl = {};

	const addUsage = (base_model_id) => {
		const baseModel = $models.find((m) => m.id === base_model_id);

		if (baseModel) {
			if (baseModel.owned_by === 'openai') {
				capabilities.usage = baseModel?.meta?.capabilities?.usage ?? false;
			} else {
				delete capabilities.usage;
			}
			capabilities = capabilities;
		}
	};

	const submitHandler = async () => {
		loading = true;

		info.id = id;
		info.name = name;

		if (id === '') {
			toast.error('Model ID is required.');
		}

		if (name === '') {
			toast.error('Model Name is required.');
		}

		info.access_control = accessControl;
		info.meta.capabilities = capabilities;

		if (knowledge.length > 0) {
			info.meta.knowledge = knowledge;
		} else {
			if (info.meta.knowledge) {
				delete info.meta.knowledge;
			}
		}

		if (toolIds.length > 0) {
			info.meta.toolIds = toolIds;
		} else {
			if (info.meta.toolIds) {
				delete info.meta.toolIds;
			}
		}

		if (filterIds.length > 0) {
			info.meta.filterIds = filterIds;
		} else {
			if (info.meta.filterIds) {
				delete info.meta.filterIds;
			}
		}

		if (actionIds.length > 0) {
			info.meta.actionIds = actionIds;
		} else {
			if (info.meta.actionIds) {
				delete info.meta.actionIds;
			}
		}

		info.params.stop = params.stop ? params.stop.split(',').filter((s) => s.trim()) : null;
		Object.keys(info.params).forEach((key) => {
			if (info.params[key] === '' || info.params[key] === null) {
				delete info.params[key];
			}
		});

		await onSubmit(info);

		loading = false;
		success = false;
	};

	onMount(async () => {
		await tools.set(await getTools(localStorage.token));
		await functions.set(await getFunctions(localStorage.token));
		await knowledgeCollections.set(await getKnowledgeBases(localStorage.token));

		console.log($models);

		// Scroll to top 'workspace-container' element
		const workspaceContainer = document.getElementById('workspace-container');
		if (workspaceContainer) {
			workspaceContainer.scrollTop = 0;
		}

		if (model) {
			console.log(model);
			name = model.name;
			await tick();

			id = model.id;

			if (model.base_model_id) {
				const base_model = $models
					.filter((m) => !m?.preset && !(m?.arena ?? false))
					.find((m) => [model.base_model_id, `${model.base_model_id}:latest`].includes(m.id));

				console.log('base_model', base_model);

				if (base_model) {
					model.base_model_id = base_model.id;
				} else {
					model.base_model_id = null;
				}
			}

			params = { ...params, ...model?.params };
			params.stop = params?.stop
				? (typeof params.stop === 'string' ? params.stop.split(',') : (params?.stop ?? [])).join(
					','
				)
				: null;

			toolIds = model?.meta?.toolIds ?? [];
			filterIds = model?.meta?.filterIds ?? [];
			actionIds = model?.meta?.actionIds ?? [];
			knowledge = (model?.meta?.knowledge ?? []).map((item) => {
				if (item?.collection_name) {
					return {
						id: item.collection_name,
						name: item.name,
						legacy: true
					};
				} else if (item?.collection_names) {
					return {
						name: item.name,
						type: 'collection',
						collection_names: item.collection_names,
						legacy: true
					};
				} else {
					return item;
				}
			});
			capabilities = { ...capabilities, ...(model?.meta?.capabilities ?? {}) };

			if ('access_control' in model) {
				accessControl = model.access_control;
			} else {
				accessControl = {};
			}

			console.log(model?.access_control);
			console.log(accessControl);

			info = {
				...info,
				...JSON.parse(
					JSON.stringify(
						model
							? model
							: {
								id: model.id,
								name: model.name
							}
					)
				)
			};

			console.log(model);
		}

		loaded = true;
	});

	let isOpen = false;
	let selectedAction: string | null = null;

	let isChangingBaseModel = false;
	let selectedModel: string | null = null;
	let selectedBehavior: string | null = null;
</script>

{#if loaded}
	{#if onBack}
		<button
			class="flex space-x-1"
			on:click={() => {
				onBack();
			}}
		>
			<div class=" self-center">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="h-4 w-4"
				>
					<path
						fill-rule="evenodd"
						d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<div class=" self-center text-sm font-medium">{'Back'}</div>
		</button>
	{/if}

	<div class=" flex flex-wrap overflow-auto gap-sm ">
		<section class="flex-1 max-h-full flex justify-center px-lg py-2xl">
			<input
				bind:this={filesInputElement}
				bind:files={inputFiles}
				type="file"
				hidden
				accept="image/*"
				on:change={() => {
				let reader = new FileReader();
				reader.onload = (event) => {
					let originalImageUrl = `${event.target.result}`;

					const img = new Image();
					img.src = originalImageUrl;

					img.onload = function () {
						const canvas = document.createElement('canvas');
						const ctx = canvas.getContext('2d');

						// Calculate the aspect ratio of the image
						const aspectRatio = img.width / img.height;

						// Calculate the new width and height to fit within 100x100
						let newWidth, newHeight;
						if (aspectRatio > 1) {
							newWidth = 250 * aspectRatio;
							newHeight = 250;
						} else {
							newWidth = 250;
							newHeight = 250 / aspectRatio;
						}

						// Set the canvas size
						canvas.width = 250;
						canvas.height = 250;

						// Calculate the position to center the image
						const offsetX = (250 - newWidth) / 2;
						const offsetY = (250 - newHeight) / 2;

						// Draw the image on the canvas
						ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);

						// Get the base64 representation of the compressed image
						const compressedSrc = canvas.toDataURL();

						// Display the compressed image
						info.meta.profile_image_url = compressedSrc;

						inputFiles = null;
						filesInputElement.value = '';
					};
				};

				if (
					inputFiles &&
					inputFiles.length > 0 &&
					['image/gif', 'image/webp', 'image/jpeg', 'image/png', 'image/svg+xml'].includes(
						inputFiles[0]['type']
					)
				) {
					reader.readAsDataURL(inputFiles[0]);
				} else {
					console.log(`Unsupported File Type '${inputFiles[0]['type']}'.`);
					inputFiles = null;
				}
			}}
			/>

			{#if !edit || (edit && model)}
				<form
					class="flex flex-col md:flex-row w-full gap-3 md:gap-6"
					on:submit|preventDefault={() => {
					submitHandler();
				}}
				>
					<div class="w-full flex flex-col py-2xl px-2xl gap-2xl">

						<div class=" flex gap-2xl">
							<!-- Image container -->
<!--							<div-->
<!--								class="self-center md:self-start flex flex-col gap-sm text-slate-400 justify-center my-2 flex-shrink-0 border border-slate-500">-->
<!--								<label class="text-label">Icono</label>-->
<!--								<div class="self-center">-->
<!--									<button-->
<!--										class="rounded-[33px] border > flex-shrink-0 items-center {info.meta.profile_image_url !==-->
<!--							'/static/favicon.png'-->
<!--								? 'bg-transparent'-->
<!--								: 'bg-white'} shadow-xl group relative"-->
<!--										type="button"-->
<!--										on:click={() => {-->
<!--								filesInputElement.click();-->
<!--							}}-->
<!--									>-->
<!--										{#if info.meta.profile_image_url}-->
<!--											<img-->
<!--												src={info.meta.profile_image_url}-->
<!--												alt="model profile"-->
<!--												class="rounded-[33px] md:size-60 object-cover shrink-0"-->
<!--											/>-->
<!--										{:else}-->
<!--											<img-->
<!--												src="/static/favicon.png"-->
<!--												alt="model profile"-->
<!--												class=" rounded-xl  object-cover shrink-0"-->
<!--											/>-->
<!--										{/if}-->

<!--										<div class="absolute bottom-0 right-0 z-10">-->
<!--											<div class="m-1.5">-->
<!--												<div-->
<!--													class="shadow-xl p-1 rounded-full border-2 border-white bg-gray-800 text-white group-hover:bg-gray-600 transition dark:border-black dark:bg-white dark:group-hover:bg-gray-200 dark:text-black"-->
<!--												>-->
<!--													<svg-->
<!--														xmlns="http://www.w3.org/2000/svg"-->
<!--														viewBox="0 0 16 16"-->
<!--														fill="currentColor"-->
<!--														class="size-5"-->
<!--													>-->
<!--														<path-->
<!--															fill-rule="evenodd"-->
<!--															d="M2 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4Zm10.5 5.707a.5.5 0 0 0-.146-.353l-1-1a.5.5 0 0 0-.708 0L9.354 9.646a.5.5 0 0 1-.708 0L6.354 7.354a.5.5 0 0 0-.708 0l-2 2a.5.5 0 0 0-.146.353V12a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V9.707ZM12 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"-->
<!--															clip-rule="evenodd"-->
<!--														/>-->
<!--													</svg>-->
<!--												</div>-->
<!--											</div>-->
<!--										</div>-->

<!--										<div-->
<!--											class="absolute top-0 bottom-0 left-0 right-0 bg-white dark:bg-black rounded-lg opacity-0 group-hover:opacity-20 transition"-->
<!--										></div>-->
<!--									</button>-->

<!--									<div class="flex w-full mt-1 justify-end">-->
<!--										<button-->
<!--											class="px-2 py-1 text-gray-500 rounded-lg text-xs"-->
<!--											on:click={() => {-->
<!--									info.meta.profile_image_url = '/static/favicon.png';-->
<!--								}}-->
<!--											type="button"-->
<!--										>-->
<!--											Reset Image-->
<!--										</button-->
<!--										>-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->

							<div class="flex flex-col items-start gap-sm">
								<label class="text-label text-slate-400" for="model-icon">
									Icono
								</label>

									<article class={`relative w-[120px] h-[120px] p-2xl rounded-[33px] flex justify-center items-center aspect-square`} style={info.meta.profile_image_url.url ? `background-image: url(${info.meta.profile_image_url}); background-size: cover; background-position: center;)` : 'background-color: red;'} >
										<svg xmlns="http://www.w3.org/2000/svg" width="64" height="49" viewBox="0 0 64 49" fill="currentColor" class=" aspect-[4/3]" >
											<path fill-rule="evenodd" clip-rule="evenodd" d="M13.5057 9.26133C14.2768 8.33604 15.652 8.21102 16.5774 8.9821L25.3011 16.2517C25.8297 16.6922 26.1194 17.3563 26.0827 18.0434C26.046 18.7305 25.6872 19.36 25.1146 19.7416L16.3909 25.5573C15.3887 26.2254 14.0347 25.9546 13.3665 24.9524C12.6984 23.9503 12.9692 22.5962 13.9714 21.9281L20.2648 17.7326L13.785 12.3329C12.8596 11.5618 12.7346 10.1866 13.5057 9.26133ZM41.7492 22.2883C44.1582 22.2883 46.1111 20.3355 46.1111 17.9266C46.1111 15.5177 44.1582 13.5649 41.7492 13.5649C39.3402 13.5649 37.3873 15.5177 37.3873 17.9266C37.3873 20.3355 39.3402 22.2883 41.7492 22.2883ZM41.7492 26.6501C46.5672 26.6501 50.4729 22.7444 50.4729 17.9266C50.4729 13.1088 46.5672 9.20312 41.7492 9.20312C36.9312 9.20312 33.0255 13.1088 33.0255 17.9266C33.0255 22.7444 36.9312 26.6501 41.7492 26.6501ZM23.0818 32.3802C22.2979 31.4657 20.9211 31.3598 20.0065 32.1436C19.092 32.9275 18.9861 34.3043 19.77 35.2188C21.4533 37.1826 24.5206 39.5626 28.3747 40.2699C32.4041 41.0094 36.9546 39.8536 41.1985 35.2835C42.0181 34.4008 41.967 33.0209 41.0843 32.2014C40.2017 31.3818 38.8217 31.4329 38.0021 32.3155C34.6854 35.8872 31.6027 36.4277 29.162 35.9798C26.5459 35.4997 24.3063 33.8088 23.0818 32.3802Z" fill="white"/>
										</svg>

										<div class="absolute -bottom-1 -right-1 z-10">
											<div class="m-1.5">
												<div
													class="shadow-xl p-xs rounded-sm bg-slate-100 text-slate-500 group-hover:bg-gray-600 transition dark:bg-slate-900 dark:group-hover:bg-gray-200 dark:text-slate-500"
												>
													<Image size="20"/>
												</div>
											</div>
										</div>
									</article>

							</div>

							<!-- Header model section -->
							<div class="flex flex-col gap-lg flex-1">
								<div class=" flex justify-between">
									<div>
										<label for="model-name" class="text-label text-slate-400">{$i18n.t('Name')}</label>
										<input
											class="text-slate-950 text-title w-full bg-transparent outline-none"
											placeholder={$i18n.t('Assistant name')}
											id="model-name"
											bind:value={name}
											required
										/>

										<div class="flex-1">
											<div>
												<input
													class="text-xs w-full bg-transparent text-gray-500 outline-none"
													placeholder={$i18n.t('Assistant ID')}
													bind:value={id}
													disabled={edit}
													required
												/>
											</div>
										</div>
									</div>

									<div class="flex flex-col gap-sm">
										<label class="text-label text-slate-400">Color del icono</label>
										<SwatchList />
									</div>
								</div>

								<div class="my-1">
									<div class="mb-1 flex w-full justify-between items-center">
										<div class=" self-center text-label text-slate-400 font-semibold">{$i18n.t('Description')}</div>

										<button
											class="p-1 text-xs flex rounded transition"
											type="button"
											on:click={() => {
									if (info.meta.description === null) {
										info.meta.description = '';
									} else {
										info.meta.description = null;
									}
								}}
										>
											{#if info.meta.description === null}
												<span class="ml-2 self-center">{$i18n.t('Default')}</span>
											{:else}
												<span class="ml-2 self-center">{$i18n.t('Custom')}</span>
											{/if}
										</button>
									</div>

									{#if info.meta.description !== null}
										<div class=" border dark:border-slate-700 bg-white dark:bg-slate-950 rounded-sm focus-within:dark:border-brand-300">
											<Textarea
												className=" p-base text-markdown-base dark:text-slate-50 placeholder:text-placeholder placeholder:text-slate-500 w-full h-[105px] outline-none resize-none overflow-y-hidden "
												placeholder={$i18n.t('Add a short description about what this model does')}
												bind:value={info.meta.description}
											/>
										</div>

									{/if}
								</div>

							</div>
						</div>

						{#if preset}
							<div class=" flex self-stretch justify-between items-center gap-lg p-base">
								<article class="basis-96 flex flex-col gap-sm">
										<h3 class="text-label text-slate-400">Modelo base</h3>
										<button class="flex w-full flex-start gap-sm rounded-lg border transition-all {selectedModel ? 'border-brand-300 bg-brand-50' : 'border-slate-50 bg-white'} py-base px-lg" type="button"
														on:click={()=>(selectedAction = 'models')}>
											{#if selectedModel}
												<div>
													<img class="w-6 h-6" src="/static/splash.png" alt="splash"/>
												</div>
												<div>
													<div class=" self-center text-subtitle text-slate-950 font-semibold">
														{selectedModel.name}
													</div>
													<div class=" self-center text-xs text-gray-500">
														{selectedModel.owned_by}
													</div>

												</div>
											{:else}
												Selecciona un modelo
											{/if}

										</button>
								</article>
								<article class="basis-96 flex flex-col gap-sm">
									<h3 class="text-label text-slate-400">{$i18n.t('Comportamiento')}</h3>
									<button class="flex w-full flex-start gap-sm rounded-lg border transition-all {selectedModel ? 'border-brand-300 bg-brand-50' : 'border-slate-50 bg-white'} py-base px-lg" type="button"
													on:click={()=>(selectedAction = 'models')}>
										{#if selectedModel}
											<div>
												<img class="w-6 h-6" src="/static/splash.png" alt="splash"/>
											</div>
											<div>
												<div class=" self-center text-subtitle text-slate-950 font-semibold">
													{selectedModel.name}
													{selectedBehavior.name}
												</div>
												<div class=" self-center text-xs text-gray-500">
													{selectedBehavior.description}
												</div>

											</div>
										{:else}
											Selecciona un modelo
										{/if}

									</button>
								</article>
							</div>
						{/if}

						<section class="">
							<div class="">
								<div class="mb-sm gap-sm">
									<label class=" text-label text-slate-400">Instrucciones de entrada</label>
									<div class=" border dark:border-slate-700 bg-white dark:bg-slate-950 rounded-sm focus-within:dark:border-brand-300">
										<Textarea
											className=" p-base text-markdown-base dark:text-slate-50 placeholder:text-placeholder placeholder:text-slate-500 w-full h-[105px] outline-none resize-none overflow-y-hidden "
											placeholder={`Write your model system prompt content here\ne.g.) You are Mario from Super Mario Bros, acting as an assistant.`}
											rows={4}
											bind:value={info.params.system}
										/>
									</div>
								</div>

								<div class="flex w-full justify-between">
									<div class=" self-center text-xs font-semibold">
										{$i18n.t('Advanced Params')}
									</div>

									<button
										class="p-1 px-3 text-xs flex rounded transition"
										type="button"
										on:click={() => {
										showAdvanced = !showAdvanced;
									}}
									>
										{#if showAdvanced}
											<span class="ml-2 self-center">{$i18n.t('Hide')}</span>
										{:else}
											<span class="ml-2 self-center">{$i18n.t('Show')}</span>
										{/if}
									</button>
								</div>
								{#if showAdvanced}
									<div class="my-2">
										<AdvancedParams
											admin={true}
											bind:params
											on:change={(e) => {
											info.params = { ...info.params, ...params };
										}}
										/>
									</div>
								{/if}
							</div>
						</section>

						<section class="flex flex-col gap-sm">
							<header class="flex justify-between items-center ">
								<h2	 class="text-label text-slate-500"> Bases de conocimientos</h2>
								<Button variant="outline-primary" size="base" icon={LibraryBig} onClick={()=>(selectedAction = 'knowledge')} buttonClasses="text-slate-500">Añadir bases de conocimiento</Button>
							</header>
							<div id="content" class="flex flex-wrap justify-start items-start gap-sm bg-slate-200 py-2xl rounded-md self-stretch">
								{#if knowledge && knowledge.length > 0}
									{#each knowledge as k}
										<Pill text={k.name} pillColor="{randomColor}" />
									{/each}
								{:else}
									<p class="text-center text-base text-slate-500">Sin bases de conocimiento asociadas, da click en <b class=" font-bold text-brand-500">Añadir bases de conocimientos</b> para vincularlas</p>
								{/if}
							</div>
						</section>

						<section class="">
							<div class="px-3 py-2 bg-gray-50 dark:bg-gray-950 rounded-lg">
								<AccessControl bind:accessControl />
							</div>
						</section>

						<section class="">
							<div class="flex w-full justify-between items-center">
								<div class="flex w-full justify-between items-center">
									<div class=" self-center text-sm font-semibold">
										{$i18n.t('Prompt suggestions')}
									</div>

									<button
										class="p-1 text-xs flex rounded transition"
										type="button"
										on:click={() => {
										if ((info?.meta?.suggestion_prompts ?? null) === null) {
											info.meta.suggestion_prompts = [{ content: '' }];
										} else {
											info.meta.suggestion_prompts = null;
										}
									}}
									>
										{#if (info?.meta?.suggestion_prompts ?? null) === null}
											<span class="ml-2 self-center">{$i18n.t('Default')}</span>
										{:else}
											<span class="ml-2 self-center">{$i18n.t('Custom')}</span>
										{/if}
									</button>
								</div>

								{#if (info?.meta?.suggestion_prompts ?? null) !== null}
									<button
										class="p-1 px-2 text-xs flex rounded transition"
										type="button"
										on:click={() => {
										if (
											info.meta.suggestion_prompts.length === 0 ||
											info.meta.suggestion_prompts.at(-1).content !== ''
										) {
											info.meta.suggestion_prompts = [
												...info.meta.suggestion_prompts,
												{ content: '' }
											];
										}
									}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 20 20"
											fill="currentColor"
											class="w-4 h-4"
										>
											<path
												d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z"
											/>
										</svg>
									</button>
								{/if}
							</div>

							{#if info?.meta?.suggestion_prompts}
								<div class="flex flex-col space-y-1 mt-1 mb-3">
									{#if info.meta.suggestion_prompts.length > 0}
										{#each info.meta.suggestion_prompts as prompt, promptIdx}
											<div class=" flex rounded-lg">
												<input
													class=" text-sm w-full bg-transparent outline-none border-r border-gray-50 dark:border-gray-850"
													placeholder={$i18n.t('Write a prompt suggestion (e.g. Who are you?)')}
													bind:value={prompt.content}
												/>

												<button
													class="px-2"
													type="button"
													on:click={() => {
													info.meta.suggestion_prompts.splice(promptIdx, 1);
													info.meta.suggestion_prompts = info.meta.suggestion_prompts;
												}}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 20 20"
														fill="currentColor"
														class="w-4 h-4"
													>
														<path
															d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
														/>
													</svg>
												</button>
											</div>
										{/each}
									{:else}
										<div class="text-xs text-center">No suggestion prompts</div>
									{/if}
								</div>
							{/if}
						</section>

						<section class=" p-5">
							<button class="border " type="button" on:click={()=>(selectedAction = 'knowledge')}>Manage knowledge</button>
							<Knowledge bind:selectedKnowledge={knowledge} collections={$knowledgeCollections} />
						</section>

						<section class="">
							<ToolsSelector bind:selectedToolIds={toolIds} tools={$tools} />
						</section>

						<section class="">
							<FiltersSelector
								bind:selectedFilterIds={filterIds}
								filters={$functions.filter((func) => func.type === 'filter')}
							/>
						</section>

						<section class="">
							<ActionsSelector
								bind:selectedActionIds={actionIds}
								actions={$functions.filter((func) => func.type === 'action')}
							/>
						</section>

						<section class="">
							<div class="">
								<Tags
									tags={info?.meta?.tags ?? []}
									on:delete={(e) => {
									const tagName = e.detail;
									info.meta.tags = info.meta.tags.filter((tag) => tag.name !== tagName);
								}}
									on:add={(e) => {
									const tagName = e.detail;
									if (!(info?.meta?.tags ?? null)) {
										info.meta.tags = [{ name: tagName }];
									} else {
										info.meta.tags = [...info.meta.tags, { name: tagName }];
									}
								}}
								/>
							</div>
						</section>

						<section class="">
							<Capabilities bind:capabilities />
						</section>

						<section class=" text-gray-300 dark:text-gray-700">
							<div class="flex w-full justify-between mb-2">
								<div class=" self-center text-sm font-semibold">{$i18n.t('JSON Preview')}</div>

								<button
									class="p-1 px-3 text-xs flex rounded transition"
									type="button"
									on:click={() => {
									showPreview = !showPreview;
								}}
								>
									{#if showPreview}
										<span class="ml-2 self-center">{$i18n.t('Hide')}</span>
									{:else}
										<span class="ml-2 self-center">{$i18n.t('Show')}</span>
									{/if}
								</button>
							</div>

							{#if showPreview}
								<div>
								<textarea
									class="text-sm w-full bg-transparent outline-none resize-none"
									rows="10"
									value={JSON.stringify(info, null, 2)}
									disabled
									readonly
								/>
								</div>
							{/if}
						</section>

						<section class=" flex justify-end pb-20">
							<Button icon={Save} buttonClasses="text-sm px-3 py-2 transition rounded-lg {loading
								? ' cursor-not-allowed '
								: ''} flex w-full justify-center" variant="primary">
								<span class=" self-center font-medium">
									{#if edit}
										{$i18n.t('Save & Update')}
									{:else}
										{$i18n.t('Save & Create')}
									{/if}
								</span>
								{#if loading}
									<div class="ml-1.5 self-center">
										<svg
											class=" w-4 h-4"
											viewBox="0 0 24 24"
											fill="currentColor"
											xmlns="http://www.w3.org/2000/svg"
										>
											<style>
                          .spinner_ajPY {
                              transform-origin: center;
                              animation: spinner_AtaB 0.75s infinite linear;
                          }

                          @keyframes spinner_AtaB {
                              100% {
                                  transform: rotate(360deg);
                              }
                          }
											</style>
											<path
												d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
												opacity=".25"
											/>
											<path
												d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
												class="spinner_ajPY"
											/>
										</svg
										>
									</div>
								{/if}
							</Button>
							<button
								class=" text-sm px-3 py-2 transition rounded-lg {loading
								? ' cursor-not-allowed bg-primary-500 hover:bg-primary-700 text-white dark:bg-white dark:hover:bg-gray-100 dark:text-black'
								: 'bg-primary-500 hover:bg-primary-700 text-white dark:bg-white dark:hover:bg-gray-100 dark:text-black'} flex w-full justify-center"
								type="submit"
								disabled={loading}
							>
								<div class=" self-center font-medium">
									{#if edit}
										{$i18n.t('Save & Update')}
									{:else}
										{$i18n.t('Save & Create')}
									{/if}
								</div>

								{#if loading}
									<div class="ml-1.5 self-center">
										<svg
											class=" w-4 h-4"
											viewBox="0 0 24 24"
											fill="currentColor"
											xmlns="http://www.w3.org/2000/svg"
										>
											<style>
                          .spinner_ajPY {
                              transform-origin: center;
                              animation: spinner_AtaB 0.75s infinite linear;
                          }

                          @keyframes spinner_AtaB {
                              100% {
                                  transform: rotate(360deg);
                              }
                          }
											</style>
											<path
												d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
												opacity=".25"
											/>
											<path
												d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
												class="spinner_ajPY"
											/>
										</svg
										>
									</div>
								{/if}
							</button>
						</section>
					</div>
				</form>
			{/if}
		</section>
		<aside class:open={!!selectedAction}
					 class="action-panel bg-slate-50 flex-1 border-l border-slate-300 p-lg max-w-md transition">
			{#if selectedAction}
				<article>
					<header class="flex justify-between">
						<h1 class="text-label text-slate-400">
							{#if (selectedAction === 'models')}
								Models
							{:else if selectedAction === 'knowledge'}
								Knowledge
							{:else}
								<p>Por favor selecciona una acción válida.</p>
							{/if}
						</h1>
						<Button variant="icon" icon={X} buttonClasses="text-slate-500"
										onClick={() => { isChangingBaseModel = false; isOpen = !isOpen; }} />

					</header>
					<div class="content">
						{#if selectedAction === 'models'}
							<div class="flex flex-col gap-sm">
								<h2 class="text-md font-semibold">Elige un modelo</h2>
								<ol class="flex flex-col gap-sm">
									{#each $models.filter((m) => (model ? m.id !== model.id : true) && !m?.preset && m?.owned_by !== 'arena') as model}

										<li
											on:click={() => {selectedModel = model}}
											class="flex w-full flex-start gap-sm rounded-lg border transition-all hover:-translate-y-2 {selectedModel === model ? 'border-brand-300 bg-brand-50' : 'border-slate-50 bg-white'} py-base px-lg"
										>
											<input type="radio" name="model" value={model.id} class="hidden" />
											<div>
												<img class="w-6 h-6" src="/static/splash.png" alt="splash"/>
											</div>
											<div>
												<div class=" self-center text-subtitle text-slate-950 font-semibold">
													{model.name}
												</div>
												<div class=" self-center text-xs text-gray-500">
													{model.owned_by}
												</div>
											</div>
										</li>
									{/each}
								</ol>
							</div>
						{:else if selectedAction === 'tools'}
							<!-- Contenido relacionado con herramientas -->
							<div>
								<p>Configuración de herramientas irá aquí.</p>
							</div>
						{:else if selectedAction === 'knowledge'}
							<div class="flex flex-col flex-start self-stretch gap-sm">
								<!-- Does not show models owned by arena-->
								{#each $models.filter((m) => (model ? m.id !== model.id : true) && !m?.preset && m?.owned_by !== 'arena') as model}
									<article>
										<div
											class=" card gap-sm rounded-lg border {selectedModel === model ? 'active':'default'}
											 py-base px-lg">
											{#if model.preset}
												<h1>Hola</h1>

											{/if}
											<div>
												<img class="w-6 h-6" />
											</div>
											<div>
												<div class=" self-center text-subtitle text-slate-950 font-semibold">
													{model.name}
												</div>
												<div class=" self-center text-xs text-gray-500">
													{model.owned_by}
												</div>

											</div>

										</div>
									</article>
								{/each}

							</div>
							<!-- Si se habilitan otras acciones en el futuro -->
						{:else}
							<p>Por favor selecciona una acción válida.</p>
						{/if}

					</div>
					<div class=" text-sm font-semibold mb-1">{$i18n.t('Base Model (From)')}</div>
					<div class=" border p-base rounded-sm">
						<select
							class="text-sm w-full outline-none"
							placeholder="Select a base model (e.g. llama3, gpt-4o)"
							bind:value={info.base_model_id}
							on:change={(e) => {
												isOpen = !isOpen;
										addUsage(e.target.value);
									}}
							required
						>
							<option value={null} class=" text-gray-900"
							>{$i18n.t('Select a base model')}</option
							>
							{#each $models.filter((m) => (model ? m.id !== model.id : true) && !m?.preset && m?.owned_by !== 'arena') as model}
								<option value={model.id} class=" text-gray-900">{model.name}</option>
							{/each}
						</select>
					</div>

				</article>
			{/if}
		</aside>
	</div>

{/if}

<style lang="scss">

	.horizontal-divider {
    height: 1px;
    max-width: 1024px;
    flex-shrink: 0;
    align-self: stretch;
    stroke-width: 1px;
    stroke: var(--slate-300, #CBD5E1);
	}

	.card {
		@apply flex justify-start w-full gap-sm rounded-lg border transition-all hover:-translate-y-2 py-base px-lg;
	}

	.card.active {
		@apply border-brand-300 bg-brand-50;
	}

	.card.default {
		@apply border-slate-50 bg-white;
	}

  aside {
    display: none;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }

  aside.open {
    display: block;
    opacity: 1;
  }
</style>
