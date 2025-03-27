<script lang="ts">
	import { DropdownMenu } from 'bits-ui';
	import { flyAndScale } from '$lib/utils/transitions';
	import { getContext } from 'svelte';

	import Dropdown from '$lib/components/common/Dropdown.svelte';
	import GarbageBin from '$lib/components/icons/GarbageBin.svelte';
	import Pencil from '$lib/components/icons/Pencil.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Tags from '$lib/components/chat/Tags.svelte';
	import Share from '$lib/components/icons/Share.svelte';
	import ArchiveBox from '$lib/components/icons/ArchiveBox.svelte';
	import DocumentDuplicate from '$lib/components/icons/DocumentDuplicate.svelte';
	import ArrowDownTray from '$lib/components/icons/ArrowDownTray.svelte';
	import ArrowUpCircle from '$lib/components/icons/ArrowUpCircle.svelte';

	import { config } from '$lib/stores';
	import { Copy, Download, Trash2 } from 'lucide-svelte';

	const i18n = getContext('i18n');

	export let user;
	export let model;

	export let shareHandler: Function;
	export let cloneHandler: Function;
	export let exportHandler: Function;

	export let hideHandler: Function;
	export let deleteHandler: Function;
	export let onClose: Function;

	let show = false;
</script>

<Dropdown
	bind:show
	on:change={(e) => {
		if (e.detail === false) {
			onClose();
		}
	}}
>
	<Tooltip content={$i18n.t('More')}>
		<slot />
	</Tooltip>

	<div slot="content">
		<DropdownMenu.Content
			class="w-full max-w-[180px] rounded-xl p-base z-50 bg-white dark:bg-slate-800 dark:text-white shadow-[0px_0px_4px_rgba(0,0,0,0.25)]"
			sideOffset={-2}
			side="bottom"
			align="start"
			transition={flyAndScale}
		>
			<DropdownMenu.Item
				class="flex gap-2 items-center px-3 py-2 text-sm  font-medium cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
				on:click={() => {
					cloneHandler();
				}}
			>
				<Copy size="20"/>
				<div class="flex items-center">{$i18n.t('Clone')}</div>
			</DropdownMenu.Item>

			<DropdownMenu.Item
				class="flex gap-2 items-center px-3 py-2 text-sm  border-b border-b-slate-700 font-medium cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 "
				on:click={() => {
					exportHandler();
				}}
			>
				<Download size="20"/>
				<div class="flex items-center">{$i18n.t('Export')}</div>
			</DropdownMenu.Item>

			<DropdownMenu.Item
				class="flex  gap-2  items-center px-3 py-2 text-sm  font-medium cursor-pointer text-red-500 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md"
				on:click={() => {
					deleteHandler();
				}}
			>
				<Trash2 size="20"/>
				<div class="flex items-center">{$i18n.t('Delete')}</div>
			</DropdownMenu.Item>
		</DropdownMenu.Content>
	</div>
</Dropdown>
