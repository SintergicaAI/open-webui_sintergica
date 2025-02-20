<script lang="ts">
	import { ChevronDown, CircleHelp, Package, Share2, SidebarClose } from 'lucide-svelte';
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
		user
	} from '$lib/stores';

	import { slide } from 'svelte/transition';
	import { page } from '$app/stores';

	import ShareChatModal from '../chat/ShareChatModal.svelte';
	import ModelSelector from '../chat/ModelSelector.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Menu from '$lib/components/layout/Navbar/Menu.svelte';
	import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
	import MenuLines from '../icons/MenuLines.svelte';
	import AdjustmentsHorizontal from '../icons/AdjustmentsHorizontal.svelte';

	import PencilSquare from '../icons/PencilSquare.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';


	const i18n = getContext('i18n');

	export let initNewChat: Function;
	export let title: string = $WEBUI_NAME;
	export let shareEnabled: boolean = false;

	export let chat;
	export let selectedModels;
	export let showModelSelector = true;

	let showShareChatModal = false;
	let showDownloadChatModal = false;
</script>
<header class="border-b border-slate-300 flex justify-between items-center p-base dark:bg-zinc-950 dark:border-zinc-900">
	<div class="flex gap-x-base items-center">
		<SidebarClose class="icon icon--lg text-slate-500 dark:text-zinc-500" />
		<div
			class="{$showSidebar
					? 'md:hidden'
					: ''} mr-1 self-start flex flex-none items-center text-gray-600 dark:text-zinc-500"
		>
			<button
				id="sidebar-toggle-button"
				class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
				on:click={() => {
						showSidebar.set(!$showSidebar);
					}}
				aria-label="Toggle Sidebar"
			>
				<div class=" m-auto self-center">
					<SidebarClose class="icon icon--lg text-slate-500" />
				</div>
			</button>
		</div>
		<div
			class="flex-1 overflow-hidden max-w-full py-0.5
			{$showSidebar ? 'ml-1' : ''}
			"
		>
			{#if showModelSelector}
				<ModelSelector bind:selectedModels showSetDefault={false} showAddModel={true} />
			{/if}
		</div>
		<span class="text-slate-500">|</span>
		<h2 class="text-subtitle">{title}</h2>
	</div>

	<div class="self-start flex flex-none items-center text-gray-600 dark:text-gray-400">
		<!-- <div class="md:hidden flex self-center w-[1px] h-5 mx-2 bg-gray-300 dark:bg-stone-700" /> -->
		{#if shareEnabled && chat && (chat.id || $temporaryChatEnabled)}
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
					<div class=" m-auto self-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="size-5"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
							/>
						</svg>
					</div>
				</button>
			</Menu>
		{/if}

		<Tooltip content={$i18n.t('New Chat')}>
			<button
				id="new-chat-button"
				class=" flex {$showSidebar
							? 'md:hidden'
							: ''} cursor-pointer px-2 py-2 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-850 transition"
				on:click={() => {
							initNewChat();
						}}
				aria-label="New Chat"
			>
				<div class=" m-auto self-center">
					<PencilSquare className=" size-5" strokeWidth="2" />
				</div>
			</button>
		</Tooltip>
	</div>

	<div class="flex gap-x-sm">
		<Button variant="icon" size="sm" icon={Package} buttonClasses="text-slate-500" />
		<Button variant="icon" size="sm" icon={Clipboard} buttonClasses="text-slate-500" />
		<Button variant="icon" size="sm" icon={Share2} buttonClasses="text-slate-500" />
		<Button variant="icon" size="sm" icon={CircleHelp} buttonClasses="text-slate-500" />
		<Button variant="icon" size="sm" icon={Settings} buttonClasses="text-slate-500"/>
	</div>
</header>