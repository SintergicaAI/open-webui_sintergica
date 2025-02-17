<script lang="ts">
	import Fuse from 'fuse.js';

	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	import { toast } from 'svelte-sonner';
	import { getContext, onMount } from 'svelte';
	import { knowledge, WEBUI_NAME } from '$lib/stores';
	import { deleteKnowledgeById, getKnowledgeBaseList, getKnowledgeBases } from '$lib/apis/knowledge';

	import { goto } from '$app/navigation';

	import DeleteConfirmDialog from '../common/ConfirmDialog.svelte';
	import Spinner from '../common/Spinner.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { CircleHelp, Search, SquarePlus } from 'lucide-svelte';
	import { FileSizeUtil } from '$lib/components/workspace/Knowledge/FileSizeUtil';

	dayjs.extend(relativeTime);

	const i18n = getContext('i18n');

	let loaded = false;

	let query = '';
	let selectedItem = null;
	let showDeleteConfirm = false;

	let fuse = null;

	let knowledgeBases = [];
	let filteredItems = [];

	$: if (knowledgeBases) {
		fuse = new Fuse(knowledgeBases, {
			keys: ['name', 'description']
		});
	}

	$: if (fuse) {
		filteredItems = query
			? fuse.search(query).map((e) => {
				return e.item;
			})
			: knowledgeBases;
	}

	const deleteHandler = async (item) => {
		const res = await deleteKnowledgeById(localStorage.token, item.id).catch((e) => {
			toast.error(e);
		});

		if (res) {
			knowledgeBases = await getKnowledgeBaseList(localStorage.token);
			knowledge.set(await getKnowledgeBases(localStorage.token));
			toast.success($i18n.t('Knowledge deleted successfully.'));
		}
	};

	function getTotalFileSize(files) {

		const totalSizeInBytes = FileSizeUtil.getFormattedTotalSize(files, 1);

		return totalSizeInBytes;
	}

	onMount(async () => {
		knowledgeBases = await getKnowledgeBaseList(localStorage.token);
		loaded = true;
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Knowledge')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<DeleteConfirmDialog
		bind:show={showDeleteConfirm}
		on:confirm={() => {
			deleteHandler(selectedItem);
		}}
	/>

	<div class="knowledge">
		<div class="knowledge__header">
			<div class="flex items-center">
				<div class="flex md:self-center text-title font-medium px-0.5 items-center">
					Bases de conocimientos
				</div>
				<Button size="base" variant="icon" icon={CircleHelp} />
			</div>
		</div>
		<section class="knowledge__container">
			<header id="action-panel" class="knowledge__action-panel">
				<div class="flex space-x-2">
					<Button variant="primary" icon="{SquarePlus}" iconSize="lg"
									onClick={() => {goto('/workspace/knowledge/create');}} aria-label={$i18n.t('Create Knowledge')}>
						Nueva base
					</Button>
				</div>
				<div class="flex space-x-base">
						<span class="text-lg font-medium text-gray-500 dark:text-gray-300"
						>{filteredItems.length}</span>
					<div class=" self-center ml-1 mr-3">
						<Search size="24" class="text-gray-500 dark:text-gray-300" />
					</div>
					<input
						class=" w-full text-sm py-1 rounded-r-xl outline-none bg-transparent"
						bind:value={query}
						placeholder={$i18n.t('Search Knowledge')}
					/>
				</div>
			</header>
			<section class="knowledge__content">
				{#each filteredItems as item}
					<button class="card" on:click={() => {
						goto(`/workspace/knowledge/${item.id}`);
				}}>
						<div>
							<div class="line-clamp-1">
								<Pill text={item.name} pillColor="green" />
							</div>
						</div>
						<div id="card__info" class="card__info">
							<span>{item?.files.length} of files</span>
							<div class="flex self-center w-[1px] h-6 mx-2.5 bg-gray-50 dark:bg-gray-850" />
							<span>{getTotalFileSize(item?.files)}</span>
							<div class="flex self-center w-[1px] h-6 mx-2.5 bg-gray-50 dark:bg-gray-850" />
							<div class=" text-xs text-gray-500 line-clamp-1">
								{$i18n.t('Updated')}
								{dayjs(item.updated_at * 1000).fromNow()}
							</div>
						</div>
					</button>
				{/each}
			</section>
		</section>
	</div>


{:else}
	<div class="w-full h-full flex justify-center items-center">
		<Spinner />
	</div>
{/if}

<style lang="scss">
  .knowledge {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 100px 1fr;

		@apply dark:bg-slate-900;

    &__header {
      @apply flex justify-between px-base py-lg border-b border-slate-300;
    }

    &__content {
      @apply mb-5 px-lg py-2xl grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-2;

    }

    &__action-panel {
      @apply flex justify-between items-center py-2xl px-lg;
    }

    &__container {
      @apply py-2xl px-lg;

    }
  }

  .card {
    @apply flex justify-between items-center self-start py-base px-lg bg-slate-50
    border border-slate-300
    hover:bg-white dark:bg-gray-850 rounded-md
    cursor-pointer;

    .card__info {
      @apply flex items-baseline text-slate-300 font-light text-sm;
    }
  }

</style>
