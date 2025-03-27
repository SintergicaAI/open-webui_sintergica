<script lang="ts">
	import { createEventDispatcher, getContext, onMount } from 'svelte';
	import { formatFileSize } from '$lib/utils';

	import FileItemModal from './FileItemModal.svelte';
	import Spinner from './Spinner.svelte';
	import Tooltip from './Tooltip.svelte';
	import {
		CircleCheckBig,
		CodeXml,
		Edit,
		FilePen,
		FileText,
		Globe,
		Image,
		LucideImage,
		Table,
		Trash2
	} from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	dayjs.extend(relativeTime);

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let className = 'w-60';
	export let colorClassName = 'bg-white dark:bg-gray-850 border border-gray-50 dark:border-white/5';
	export let url: string | null = null;

	export let dismissible = false;
	export let loading = false;

	export let item = null;
	export let edit = false;
	export let small = false;

	export let media: string;
	export let name: string;
	export let type: string;
	export let size: number;
	export let file = null;
	export let author: string;

	let showModal = false;

	const iconSizeMap = { sm: '16', base: '20', lg: '24' };


</script>

{#if item}
	<FileItemModal bind:show={showModal} bind:item {edit} />
{/if}

<button
	class="relative overflow-hidden group py-base px-lg {className} flex items-center gap-1 {colorClassName} rounded-lg text-left"
	type="button"
	on:click={async () => {
		if (item?.file?.data?.content) {
			showModal = !showModal;
		} else {
			if (url) {
				if (type === 'file') {
					window.open(`${url}/content`, '_blank').focus();
				} else {
					window.open(`${url}`, '_blank').focus();
				}
			}
		}

		dispatch('click');
	}}
>
	{#if !small}
		<div class="p-3 bg-black/20 dark:bg-white/10 text-white rounded-xl">
			{#if !loading}
				<CircleCheckBig size="20"/>
			{:else}
				<Spinner />
			{/if}
		</div>
	{/if}

	{#if !small}
		<div class="flex flex-col justify-center -space-y-0.5 px-2.5 w-full">
			<div class=" dark:text-gray-100 text-sm font-medium line-clamp-1 mb-1">
				{name}
			</div>

			<div class=" flex justify-between text-gray-500 text-xs line-clamp-1">
				{#if type === 'file'}
					{$i18n.t('File')}
				{:else if type === 'doc'}
					{$i18n.t('Document')}
				{:else if type === 'collection'}
					{$i18n.t('Collection')}
				{:else}
					<span class=" capitalize line-clamp-1">{type}</span>
				{/if}
				{#if size}
					<span class="capitalize">{formatFileSize(size)}</span>
				{/if}
			</div>
		</div>
	{:else}
		<Tooltip content={name} className="flex flex-col w-full" placement="top-start">
			<div class="flex flex-col justify-center -space-y-0.5 px-2.5 w-full">
				<div class=" dark:text-gray-100 text-sm flex justify-between items-center">
					{#if loading}
						<div class=" shrink-0 mr-2">
							<Spinner className="size-4" />
						</div>
						{:else}
						<div class="flex justify-between w-full">
							<div class="text-base font-normal h-[42px] text-slate-900 line-clamp-1 flex flex-wrap gap-sm items-center">
								{#if media === 'application/json' || media === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || media === 'application/pdf'}
									<FileText class="text-brand-500 text-base" size={iconSizeMap.base} />
								{:else if media.startsWith('image/')}
									<Image class="text-brand-500 text-base" size={iconSizeMap.base}/>
								{:else if media === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || media === 'text/csv'}
									<Table class="text-brand-500 text-base" size={iconSizeMap.base}/>
								{:else}
									<CodeXml class="text-brand-500 text-base" size={iconSizeMap.base}/>
								{/if}
								<span class="text-base text-slate-900 dark:text-slate-50">{name}</span>
							</div>
							<div class="flex items-center gap-sm text-label text-slate-500">
								<div class="text-label text-slate-500 capitalize shrink-0">{formatFileSize(size)}</div>
								{#if media === 'application/json'}
									<span class="text-label">{$i18n.t('json')}</span>
								{:else if media === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
									<span>{$i18n.t('word')}</span>
								{:else if media === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || media === 'text/csv'}
									<span>{$i18n.t('table')}</span>
								{:else }
									<span>{$i18n.t('other')}</span>
								{/if}

								<span class="text-label text-slate-500 ">{dayjs(file.updated_at * 1000).fromNow()}</span>

								<Avatar name={author} size="sm" />

								<p class="hoverable group-hover:flex hidden transition text-label text-slate-500 gap-1 items-center">
									{#if dismissible}
										<Button variant="icon" size="base" icon={Trash2} onClick={() => {
											dispatch('dismiss')}
										}/>
									{/if}
									<Button size="base" variant="icon" icon={FilePen} onClick={() => {
									dispatch('click')}}/>
								</p>
							</div>
						</div>
						{/if}

				</div>
			</div>
		</Tooltip>
	{/if}

	{#if loading}
		<div class="absolute bottom-0 left-0 w-[100%] h-1 bg-transparent rounded-full ">
			<div class="h-full bg-blue-500 transition-all" style="width: {loading ? '80%' : '0%'}"></div>
		</div>
	{/if}
</button>
