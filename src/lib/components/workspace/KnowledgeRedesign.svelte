<script lang="ts">
	import Fuse from 'fuse.js';

	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	import { toast } from 'svelte-sonner';
	import { getContext, onMount } from 'svelte';
	import { knowledge, settings, WEBUI_NAME } from '$lib/stores';
	import { deleteKnowledgeById, getKnowledgeBaseList, getKnowledgeBases } from '$lib/apis/knowledge';

	import { goto } from '$app/navigation';

	import DeleteConfirmDialog from '../common/ConfirmDialog.svelte';
	import Spinner from '../common/Spinner.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { CircleHelp, Search, SquarePlus } from 'lucide-svelte';
	import { FileSizeUtil } from '$lib/components/workspace/Knowledge/FileSizeUtil';
	import { capitalizeFirstLetter } from '$lib/utils/index.js';

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
				<div class="flex md:self-center text-title dark:text-white items-center">
					Bases de conocimientos
				</div>
				<Button size="base" variant="icon" icon={CircleHelp} buttonClasses="text-slate-500" />
			</div>
		</div>
		<section class="knowledge__container">
			<header id="action-panel" class="knowledge__action-panel">
				<div class="flex ">
					<Button variant="primary" icon="{SquarePlus}" iconSize="lg"
									onClick={() => {goto('/workspace/knowledge/create');}} aria-label={$i18n.t('Create Knowledge')}>
						Nueva base
					</Button>
				</div>
				<div class="flex items-center gap-sm">
						<span class="text-label text-slate-500"
						>{filteredItems.length} {$i18n.t('bases')}</span>

					<div class="self-stretch p-base inline-flex justify-center rounded-sm items-center border 	bg-white dark:bg-brand-950 dark:border-slate-700">
						<input
							class=" flex-1 text-base text-slate-500 placeholder:text-slate-500 placeholder:text-placeholder w-full outline-none bg-transparent"
							bind:value={query}
							placeholder={$i18n.t('Search')}
						/>
						<Search size="20" class="text-slate-500" />
					</div>
				</div>
			</header>
			<section class="knowledge__content">
				{#each filteredItems as item}
					<a class="card" href={`/dev/knowledge/${item.id}`}>
						<header class="card__header">
							<div class="line-clamp-1">
								<Pill text={item.name} pillColor={$settings.knowledgeColor} />
							</div>
							<p class="text-label text-slate-400">
								<span>{item?.files.length} of files</span>
							</p>
						</header>
						<footer id="card__info" class="card__footer">
							<div class="flex items-center gap-xs">
								<div class=" text-label text-slate-400 line-clamp-1">
									{$i18n.t('Updated')}
									{dayjs(item.updated_at * 1000).fromNow()}
								</div>
								<b class=" text-avatar text-brand-500 ">{capitalizeFirstLetter(item?.user?.name ?? $i18n.t('Deleted User'))}</b>
							</div>
							<span class=" text-label text-slate-400"> {getTotalFileSize(item?.files)}</span>
						</footer>
					</a>
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
      @apply flex-1 self-stretch px-lg py-2xl grid grid-cols-1 items-start content-start md:grid-cols-2 gap-sm;
    }

    &__action-panel {
      @apply self-stretch flex justify-between items-center py-2xl px-lg;
    }

    &__container {
      @apply self-stretch py-2xl px-lg flex flex-col gap-2xl items-center flex-shrink-0 ;

    }
  }

  .card {
    @apply w-full flex flex-col items-start py-base px-lg;
    gap: 12px;
		border-radius: var(--spacing-base, 12px);

    @apply border bg-slate-50 border-slate-200 dark:bg-slate-800 dark:border-slate-800 rounded-md
    cursor-pointer;

		&:hover {
			@apply bg-white border-slate-200 dark:border-slate-800 dark:bg-slate-900 ;
		}

		&:active {
			@apply bg-brand-50 border-brand-200 dark:border-slate-700 dark:bg-brand-800 ;
		}

    .card__info {
      @apply flex items-baseline text-slate-300 font-light text-sm;
    }

		.card__header {
      display: flex;
			justify-content: space-between;
      align-items: center;
			align-self: stretch;
    }

		.card__footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;
		}
  }

</style>
