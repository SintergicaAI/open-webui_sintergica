<script lang="ts">
	import { ChevronDown, CircleHelp, EllipsisVertical, Package, Share2, SidebarClose, SidebarOpen } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Settings } from 'lucide-svelte';
	import { Clipboard } from 'lucide-svelte';
	import { getContext } from 'svelte';

	import {
		WEBUI_NAME,
		chatId,
		mobile,
		settings,
		showSettings,
		showArchivedChats,
		showControls,
		showSidebar,
		temporaryChatEnabled,
		user, showArtifacts, showOverview
	} from '$lib/stores';

	import { slide } from 'svelte/transition';
	import { page } from '$app/stores';

	import ShareChatModal from '../chat/ShareChatModal.svelte';
	import ModelSelector from '../chat/ModelSelector.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Menu from '$lib/components/layout/Navbar/Menu.svelte';
	import { copyToClipboard, createMessagesList } from '$lib/utils';
	import { toast } from 'svelte-sonner';


	const i18n = getContext('i18n');

	export let initNewChat: Function;
	export let shareEnabled: boolean = false;

	export let chat;
	export let selectedModels;
	export let showModelSelector = true;

	let {title} = chat.chat
	let showShareChatModal = false;
	let showDownloadChatModal = false;

	const getChatAsText = async () => {
		const history = chat.chat.history;
		const messages = createMessagesList(history, history.currentId);
		const chatText = messages.reduce((a, message, i, arr) => {
			return `${a}### ${message.role.toUpperCase()}\n${message.content}\n\n`;
		}, '');

		return chatText.trim();
	};
</script>

<ShareChatModal bind:show={showShareChatModal} chatId={$chatId} />

<header class="{showModelSelector ? 'border-b' : ''} bg-lvl-2 flex justify-between items-center p-base">
	<div class="flex gap-x-base items-center">


		<div
			class="{!$showSidebar
					? 'md:hidden'
					: ''} mr-1 self-start flex flex-none items-center text-gray-600 dark:text-zinc-500"
		>
			<button
				id="sidebar-toggle-button"
				class=" cursor-pointer p-[7px] flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				on:click={() => {
					showSidebar.set(!$showSidebar);
				}}
				aria-label="Toggle Sidebar"
			>
				<SidebarClose class="icon icon--lg text-slate-500 dark:text-zinc-500" />
			</button>
		</div>


			{#if showModelSelector}
				<div
					class="flex items-center flex-1 overflow-hidden max-w-full
			{$showSidebar ? '' : ''}
			">
					<div class="">
						<ModelSelector bind:selectedModels showSetDefault={false} showAddModel={false} />
					</div>
					<div class="text-slate-300 h-full space-x-base">|</div>
					<h2 class="text-subtitle text-black dark:text-white">{title}</h2>
				</div>
			{/if}


	</div>

	<div class="self-start flex flex-none items-center text-gray-600 dark:text-gray-400">
		<!-- <div class="md:hidden flex self-center w-[1px] h-5 mx-2 bg-gray-300 dark:bg-stone-700" /> -->
	</div>

	<div class="flex gap-x-sm">
		{#if shareEnabled && chat && (chat.id || $temporaryChatEnabled)}
			<Button variant="icon" size="sm" icon={Package} buttonClasses="text-slate-500" />
			<Button variant="icon" size="sm" icon={Clipboard} buttonClasses="text-slate-500" id="chat-copy-button"
							onClick={async () => {
						const res = await copyToClipboard(await getChatAsText()).catch((e) => {
							console.error(e);
						});
						if (res) {
							toast.success($i18n.t('Copied to clipboard'));
						}
				}}/>
			<Button variant="icon" size="sm" icon={Share2} buttonClasses="text-slate-500" onClick={() => {
						showShareChatModal = !showShareChatModal;
					}} />
			<Button variant="icon" size="sm" icon={CircleHelp} buttonClasses="text-slate-500" on:click={async () => {
				await showControls.set(true);
				await showArtifacts.set(true);
				await showOverview.set(false);
		}} />



			<button on:click={async () => {
			await showControls.set(true);
			await showArtifacts.set(true);
			await showOverview.set(false);
		}}>click me</button>
			<Menu
				{chat}
				{shareEnabled}
				shareHandler={() => {
							showShareChatModal = !showShareChatModal;
						}}
				downloadHandler={() => {
							showDownloadChatModal = !showDownloadChatModal;
						}}
			>
				<button
					class="flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
					id="chat-context-menu-button"
				>
					<EllipsisVertical size="20"/>
				</button>
			</Menu>
		{/if}
		<Button variant="icon" size="sm" icon={Settings} buttonClasses="text-slate-500" onClick={() => {
						showSettings.set(true);
					}}/>
	</div>
</header>