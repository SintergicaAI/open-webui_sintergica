<script lang="ts">
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';
	import Sortable from 'sortablejs';

	import fileSaver from 'file-saver';

	const { saveAs } = fileSaver;

	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';

	const i18n = getContext('i18n');

	import { WEBUI_NAME, config, mobile, models as _models, settings, user } from '$lib/stores';
	import {
		createNewModel,
		deleteModelById,
		getModels as getWorkspaceModels,
		toggleModelById,
		updateModelById
	} from '$lib/apis/models';

	import { getModels } from '$lib/apis';

	import ModelMenu from './Models/ModelMenu.svelte';
	import ModelDeleteConfirmDialog from '../common/ConfirmDialog.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import GarbageBin from '../icons/GarbageBin.svelte';
	import Spinner from '../common/Spinner.svelte';
	import { capitalizeFirstLetter } from '$lib/utils';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Download, SquarePlus, Upload, Search, Pencil, EllipsisVertical } from 'lucide-svelte';
	import Switch from '$lib/components/chat/Switch.svelte';

	let shiftKey = false;

	let importFiles;
	let modelsImportInputElement: HTMLInputElement;
	let loaded = false;

	let models = [];

	let filteredModels = [];
	let selectedModel = null;

	let showModelDeleteConfirm = false;

	$: if (models) {
		filteredModels = models.filter(
			(m) => searchValue === '' || m.name.toLowerCase().includes(searchValue.toLowerCase())
		);
	}

	$: if (selectedModel) {
		document.title = `${selectedModel.name} | ${$WEBUI_NAME}`;
	}

	let searchValue = '';

	const deleteModelHandler = async (model) => {
		const res = await deleteModelById(localStorage.token, model.id).catch((e) => {
			toast.error(e);
			return null;
		});

		if (res) {
			toast.success($i18n.t(`Deleted {{name}}`, { name: model.id }));
		}

		await _models.set(await getModels(localStorage.token));
		models = await getWorkspaceModels(localStorage.token);
	};

	const cloneModelHandler = async (model) => {
		sessionStorage.model = JSON.stringify({
			...model,
			id: `${model.id}-clone`,
			name: `${model.name} (Clone)`
		});
		goto('/workspace/models/create');
	};

	const shareModelHandler = async (model) => {
		toast.success($i18n.t('Redirecting you to OpenWebUI Community'));

		const url = 'https://openwebui.com';

		const tab = await window.open(`${url}/models/create`, '_blank');

		// Define the event handler function
		const messageHandler = (event) => {
			if (event.origin !== url) return;
			if (event.data === 'loaded') {
				tab.postMessage(JSON.stringify(model), '*');

				// Remove the event listener after handling the message
				window.removeEventListener('message', messageHandler);
			}
		};

		window.addEventListener('message', messageHandler, false);
	};

	const hideModelHandler = async (model) => {
		let info = model.info;

		if (!info) {
			info = {
				id: model.id,
				name: model.name,
				meta: {
					suggestion_prompts: null
				},
				params: {}
			};
		}

		info.meta = {
			...info.meta,
			hidden: !(info?.meta?.hidden ?? false)
		};

		const res = await updateModelById(localStorage.token, info.id, info);

		if (res) {
			toast.success(
				$i18n.t(`Model {{name}} is now {{status}}`, {
					name: info.id,
					status: info.meta.hidden ? 'hidden' : 'visible'
				})
			);
		}

		await _models.set(await getModels(localStorage.token));
		models = await getWorkspaceModels(localStorage.token);
	};

	const downloadModels = async (models) => {
		let blob = new Blob([JSON.stringify(models)], {
			type: 'application/json'
		});
		saveAs(blob, `models-export-${Date.now()}.json`);
	};

	const exportModelHandler = async (model) => {
		let blob = new Blob([JSON.stringify([model])], {
			type: 'application/json'
		});
		saveAs(blob, `${model.id}-${Date.now()}.json`);
	};

	onMount(async () => {
		models = await getWorkspaceModels(localStorage.token);

		loaded = true;

		const onKeyDown = (event) => {
			if (event.key === 'Shift') {
				shiftKey = true;
			}
		};

		const onKeyUp = (event) => {
			if (event.key === 'Shift') {
				shiftKey = false;
			}
		};

		const onBlur = () => {
			shiftKey = false;
		};

		window.addEventListener('keydown', onKeyDown);
		window.addEventListener('keyup', onKeyUp);
		window.addEventListener('blur', onBlur);

		return () => {
			window.removeEventListener('keydown', onKeyDown);
			window.removeEventListener('keyup', onKeyUp);
			window.removeEventListener('blur', onBlur);
		};
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Models')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<ModelDeleteConfirmDialog
		bind:show={showModelDeleteConfirm}
		on:confirm={() => {
			deleteModelHandler(selectedModel);
		}}
	/>
		<main class="flex flex-col justify-self-center w-full max-w-screen-lg bg-lvl-1 pt-lg gap-[24px]">
		<header class="flex flex-col max-w-screen-lg w-full">
			<section class="flex flex-wrap justify-center gap-sm md:flex-nowrap md:justify-between items-center">
				<!-- Left button group-->
				<div class="flex items-center self-stretch gap-sm">
					<Button variant="primary" icon={SquarePlus} size="sm" iconSize="sm" onClick={()=>goto('/dev/models/create')}>Nuevo modelo</Button>
					{#if $user?.role === 'admin'}
						<input
							id="models-import-input"
							bind:this={modelsImportInputElement}
							bind:files={importFiles}
							type="file"
							accept=".json"
							hidden
							on:change={() => {

						let reader = new FileReader();
						reader.onload = async (event) => {
							let savedModels = JSON.parse(event.target.result);
							for (const model of savedModels) {
								if (model?.info ?? false) {
									if ($_models.find((m) => m.id === model.id)) {
										await updateModelById(localStorage.token, model.id, model.info).catch(
											(error) => {
												return null;
											}
										);
									} else {
										await createNewModel(localStorage.token, model.info).catch((error) => {
											return null;
										});
									}
								}
							}

							await _models.set(await getModels(localStorage.token));
							models = await getWorkspaceModels(localStorage.token);
						};

						reader.readAsText(importFiles[0]);
					}}
						/>

						<Button variant="outline-primary" icon={Upload} iconSize="sm" size="sm"
										onClick={()=>modelsImportInputElement.click()}>{$i18n.t('Import Models')}</Button>
						<Button variant="outline-primary" icon={Download} iconSize="sm" size="sm"
										onClick={()=>downloadModels($_models)}>{$i18n.t('Export Models')}</Button>
					{/if}
				</div>

				<!-- Right button group-->
				<div class="flex items-center self-stretch gap-base">
					<span class="text-lg font-medium text-gray-500 dark:text-gray-300">
						{filteredModels.length} asistentes
					</span>

					<!-- Search input-->
					<div class="self-stretch p-base inline-flex justify-center rounded-sm items-center bg-white">
						<input
							class=" flex-1 text-placeholder text-sm w-full outline-none"
							bind:value={searchValue}
							placeholder={$i18n.t('Search Models')}
						/>
						<Search size="20" class="text-slate-500" />
					</div>


				</div>
			</section>
		</header>
		<section class=" max-w-screen-2xl min-h-96" id="model-list">
			{#if filteredModels.length === 0}
				<div
					class=" flex flex-col items-center self-stretch flex-1 gap-2xl h-full py-4xl">
					<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120" fill="none">
						<path
							d="M0 16.1798C0 7.24394 7.24393 0 16.1798 0H103.82C112.756 0 120 7.24393 120 16.1798V103.82C120 112.756 112.756 120 103.82 120H16.1798C7.24394 120 0 112.756 0 103.82V16.1798Z"
							fill="#DDF2FB" />
						<path fill-rule="evenodd" clip-rule="evenodd"
									d="M84.9437 56.6294C91.2732 56.6294 96.4044 51.4983 96.4044 45.1687C96.4044 38.8392 91.2732 33.7081 84.9437 33.7081C78.6141 33.7081 73.483 38.8392 73.483 45.1687C73.483 51.4983 78.6141 56.6294 84.9437 56.6294ZM84.9437 64.7193C95.7412 64.7193 104.494 55.9662 104.494 45.1687C104.494 34.3712 95.7412 25.6182 84.9437 25.6182C74.1462 25.6182 65.3931 34.3712 65.3931 45.1687C65.3931 55.9662 74.1462 64.7193 84.9437 64.7193Z"
									fill="#89CAF5" />
						<path fill-rule="evenodd" clip-rule="evenodd"
									d="M46.1972 63.3696C47.6857 65.0354 50.2428 65.1791 51.9086 63.6905C53.5744 62.2019 53.718 59.6449 52.2295 57.9791L40.5337 44.891L52.1704 32.4231C53.6947 30.7899 53.6064 28.2303 51.9733 26.706C50.3401 25.1818 47.7805 25.27 46.2562 26.9032L34.8133 39.1635L23.9151 26.968C22.4266 25.3022 19.8695 25.1586 18.2037 26.6471C16.5379 28.1357 16.3943 30.6928 17.8829 32.3585L29.5786 45.4466L17.9419 57.9145C16.4176 59.5477 16.5059 62.1073 18.139 63.6316C19.7722 65.1558 22.3318 65.0676 23.8561 63.4344L35.299 51.1741L46.1972 63.3696Z"
									fill="#89CAF5" />
						<path
							d="M59.663 74.8315C67.668 74.8315 74.1574 81.3209 74.1574 89.3259C74.1574 97.331 67.668 103.82 59.663 103.82C51.658 103.82 45.1686 97.331 45.1686 89.3259C45.1686 81.3209 51.658 74.8315 59.663 74.8315Z"
							fill="#89CAF5" />
					</svg>
					<h2 class="text-title text-brand-500">Aun no tienes asistentes agregados</h2>
					<p class="self-stretch text-base">Crea un <b class="text-brand-500">Nuevo asistente</b> para comenzar a añadir
						bases de conocimientos y (preguntar) vincularlos a grupos</p>
				</div>
			{:else}
				<section class="self-stretch grid grid-cols-1 sm:grid-cols-2 gap-sm content-center items-center">
					{#each filteredModels as model}
<!--						<button-->
<!--							class=" model flex cursor-pointer border  rounded-sm p-lg hover:bg-white dark:hover:bg-white/5 transition {selectedModel?.id === model.id ? 'bg-brand-50 ' : 'bg-slate-50'}-->
<!--"-->
<!--							id="model-item-{model.id}" on:click={() => {-->
<!--							console.log('Selected model: ', model);-->
<!--							selectedModel = model-->
<!--						}}-->
<!--						>-->
<!--							<div class="flex gap-4 mt-0.5 mb-0.5">-->
<!--								<div class=" w-[44px]">-->
<!--									<div-->
<!--										class=" rounded-full object-cover {model.is_active-->
<!--								? ''-->
<!--								: 'opacity-50 dark:opacity-50'} "-->
<!--									>-->
<!--										<img-->
<!--											src={model?.meta?.profile_image_url ?? '/static/favicon.png'}-->
<!--											alt="modelfile profile"-->
<!--											class=" rounded-full w-full h-auto object-cover"-->
<!--										/>-->
<!--									</div>-->
<!--								</div>-->

<!--								<a-->
<!--									class=" flex flex-1 cursor-pointer w-full"-->
<!--									href={`/?models=${encodeURIComponent(model.id)}`}-->
<!--								>-->
<!--									<div class=" flex-1 self-center {model.is_active ? '' : 'text-gray-500'}">-->
<!--										<Tooltip-->
<!--											content={marked.parse(model?.meta?.description ?? model.id)}-->
<!--											className=" w-fit"-->
<!--											placement="top-start"-->
<!--										>-->
<!--											<div class=" font-semibold line-clamp-1">{model.name}</div>-->
<!--										</Tooltip>-->

<!--										<div class="flex gap-1 text-xs overflow-hidden">-->
<!--											<div class="line-clamp-1">-->
<!--												{#if (model?.meta?.description ?? '').trim()}-->
<!--													{model?.meta?.description}-->
<!--												{:else}-->
<!--													{model.id}-->
<!--												{/if}-->
<!--											</div>-->
<!--										</div>-->
<!--									</div>-->
<!--								</a>-->
<!--							</div>-->

<!--							<div class="flex justify-between items-center -mb-0.5 px-0.5">-->
<!--								<div class=" text-xs mt-0.5">-->
<!--									<Tooltip-->
<!--										content={model?.user?.email ?? $i18n.t('Deleted User')}-->
<!--										className="flex shrink-0"-->
<!--										placement="top-start"-->
<!--									>-->
<!--										<div class="shrink-0 text-gray-500">-->
<!--											{$i18n.t('By {{name}}', {-->
<!--												name: capitalizeFirstLetter(-->
<!--													model?.user?.name ?? model?.user?.email ?? $i18n.t('Deleted User')-->
<!--												)-->
<!--											})}-->
<!--										</div>-->
<!--									</Tooltip>-->
<!--								</div>-->

<!--								<div class="flex flex-row gap-0.5 items-center">-->
<!--									{#if shiftKey}-->
<!--										<Tooltip content={$i18n.t('Delete')}>-->
<!--											<button-->
<!--												class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"-->
<!--												type="button"-->
<!--												on:click={() => {-->
<!--										deleteModelHandler(model);-->
<!--									}}-->
<!--											>-->
<!--												<GarbageBin />-->
<!--											</button>-->
<!--										</Tooltip>-->
<!--									{:else}-->
<!--										{#if $user?.role === 'admin' || model.user_id === $user?.id}-->
<!--											<a-->
<!--												class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"-->
<!--												type="button"-->
<!--												href={`/workspace/models/edit?id=${encodeURIComponent(model.id)}`}-->
<!--											>-->
<!--												<svg-->
<!--													xmlns="http://www.w3.org/2000/svg"-->
<!--													fill="none"-->
<!--													viewBox="0 0 24 24"-->
<!--													stroke-width="1.5"-->
<!--													stroke="currentColor"-->
<!--													class="w-4 h-4"-->
<!--												>-->
<!--													<path-->
<!--														stroke-linecap="round"-->
<!--														stroke-linejoin="round"-->
<!--														d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"-->
<!--													/>-->
<!--												</svg>-->
<!--											</a>-->
<!--										{/if}-->

<!--										<ModelMenu-->
<!--											user={$user}-->
<!--											{model}-->
<!--											shareHandler={() => {-->
<!--									shareModelHandler(model);-->
<!--								}}-->
<!--											cloneHandler={() => {-->
<!--									cloneModelHandler(model);-->
<!--								}}-->
<!--											exportHandler={() => {-->
<!--									exportModelHandler(model);-->
<!--								}}-->
<!--											hideHandler={() => {-->
<!--									hideModelHandler(model);-->
<!--								}}-->
<!--											deleteHandler={() => {-->
<!--									selectedModel = model;-->
<!--									showModelDeleteConfirm = true;-->
<!--								}}-->
<!--											onClose={() => {}}-->
<!--										>-->
<!--											<button-->
<!--												class="self-center w-fit text-sm p-1.5 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"-->
<!--												type="button"-->
<!--											>-->
<!--												<EllipsisHorizontal className="size-5" />-->
<!--											</button>-->
<!--										</ModelMenu>-->


<!--										<div class="ml-1">-->
<!--											<Tooltip content={model.is_active ? $i18n.t('Enabled') : $i18n.t('Disabled')}>-->
<!--												<Switch-->
<!--													bind:state={model.is_active}-->
<!--													on:change={async (e) => {-->
<!--											toggleModelById(localStorage.token, model.id);-->
<!--											_models.set(await getModels(localStorage.token));-->
<!--										}}-->
<!--												/>-->
<!--											</Tooltip>-->
<!--										</div>-->
<!--									{/if}-->
<!--								</div>-->
<!--							</div>-->
<!--						</button>-->

						<article class="card {model.is_active ? '' : 'disabled'} cursor-pointer border  rounded-sm p-lg transition"
										 id="model-item-{model.id}">
							<header class="card__title">
								<div class="flex flex-col gap-[10px] w-[40px] h-[40px] bg-brand-500 rounded-sm">
									<div
										class=" rounded-full object-cover {model.is_active
								? ''
								: 'opacity-50 dark:opacity-50'} "
									>
										<img
											src={model?.meta?.profile_image_url ?? '/static/favicon.png'}
											alt="modelfile profile"
											class=" rounded-full w-full h-auto object-cover"
										/>
									</div>
								</div>

								<h3 class="flex flex-col justify-center flex-1 self-stretch text-title text-gray-900 dark:text-gray-100">{model.name}</h3>

								<div class="flex flex-row gap-2 items-center">
									{#if shiftKey}
										<Tooltip content={$i18n.t('Delete')}>
											<button
												class="self-center text-sm dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
												type="button"
												on:click={() => {
										deleteModelHandler(model);
									}}
											>
												<GarbageBin />
											</button>
										</Tooltip>
										{/if}

										{#if $user?.role === 'admin' || model.user_id === $user?.id}
											<a
												class="self-center w-fit text-sm px-2 py-2 text-slate-600 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
												type="button"
												href={`/dev/models/edit?id=${encodeURIComponent(model.id)}`}
											>
												<Pencil size="16"/>
											</a>
										{/if}

									<ModelMenu
										user={$user}
										{model}
										shareHandler={() => {
									shareModelHandler(model);
								}}
										cloneHandler={() => {
									cloneModelHandler(model);
								}}
										exportHandler={() => {
									exportModelHandler(model);
								}}
										hideHandler={() => {
									hideModelHandler(model);
								}}
										deleteHandler={() => {
									selectedModel = model;
									showModelDeleteConfirm = true;
								}}
										onClose={() => {}}
									>
										<button
											class="self-center w-fit text-sm p-1.5 text-slate-600 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
											type="button"
										>
											<EllipsisVertical size="20"/>
										</button>
									</ModelMenu>
								</div>
							</header>
							<section class="card__body">
								<p class="text-base text-slate-950 dark:text-white line-clamp-1">
									{#if (model?.meta?.description ?? '').trim()}
										{model?.meta?.description}
									{:else}
										{model.id}
									{/if}
								</p>
							</section>
							<footer class="card__footer">
								<p class="">
									<Tooltip
										content={model?.user?.email ?? $i18n.t('Deleted User')}
										className="flex items-center gap-xs"
										placement="top-start"
									>
										<span class="text-label text-slate-400">
											{$i18n.t('Created by')}
										</span>
										<b class="text-avatar text-brand-500">
											{capitalizeFirstLetter(
												model?.user?.name ?? model?.user?.email ?? $i18n.t('Deleted User')
											)}
										</b>
									</Tooltip>
								</p>
								<Tooltip content={model.is_active ? $i18n.t('Enabled') : $i18n.t('Disabled')}>
									<Switch
										activeLabel="Activo"
										inactiveLabel="Inactivo"
										bind:state={model.is_active}
										on:change={async (e) => {
											toggleModelById(localStorage.token, model.id);
											_models.set(await getModels(localStorage.token));
										}}
									/>
								</Tooltip>
							</footer>
						</article>
					{/each}
				</section>
			{/if}
		</section>
	</main>

{:else}
	<div class="w-full h-full flex justify-center items-center">
		<Spinner />
	</div>
{/if}

<style lang="scss">
		.card {
        display: flex;
        padding: var(--spacing-lg, 16px);
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        gap: var(--spacing-lg, 16px);
        border-radius: 12px;
				@apply border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-800;

				.card__title {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            align-self: stretch;
        }

				.card__footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            align-self: stretch;
        }
		}
		.card.disabled {
			@apply cursor-not-allowed border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950;
		}
</style>
