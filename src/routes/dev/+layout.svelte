<script lang="ts">
	import SidebarRedesign from '$lib/components/layout/SidebarRedesign.svelte';
	import { getContext, onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { deleteDB, openDB } from 'idb';
	import { getUserSettings } from '$lib/apis/users/index.js';
	import {
		user,
		settings,
		models,
		tools,
		banners,
		showSettings,
		temporaryChatEnabled
	} from '$lib/stores';
	import { getModels } from '$lib/apis/index.js';
	import { getBanners } from '$lib/apis/configs/index.js';
	import { getTools } from '$lib/apis/tools/index.js';


	let DB = null;
	let localDBChats = [];

	onMount(async () => {
		if ($user === undefined) {
			await goto('/auth');
		} else if (['user', 'admin'].includes($user.role)) {
			try {
				DB = await openDB('Chats', 1);

				if (DB) {
					const chats = await DB.getAllFromIndex('chats', 'timestamp');
					localDBChats = chats.map((item, idx) => chats[chats.length - 1 - idx]);

					if (localDBChats.length === 0) {
						await deleteDB('Chats');
					}
				}

				console.log(DB);
			} catch (error) {
				// IndexedDB Not Found
			}

			const userSettings = await getUserSettings(localStorage.token).catch((error) => {
				console.error(error);
				return null;
			});

			if (userSettings) {
				settings.set(userSettings.ui);
			} else {
				let localStorageSettings = {} as Parameters<(typeof settings)['set']>[0];

				try {
					localStorageSettings = JSON.parse(localStorage.getItem('settings') ?? '{}');
				} catch (e: unknown) {
					console.error('Failed to parse settings from localStorage', e);
				}

				settings.set(localStorageSettings);
			}

			models.set(await getModels(localStorage.token));
			banners.set(await getBanners(localStorage.token));
			tools.set(await getTools(localStorage.token));

			document.addEventListener('keydown', async function (event) {
				const isCtrlPressed = event.ctrlKey || event.metaKey; // metaKey is for Cmd key on Mac
				// Check if the Shift key is pressed
				const isShiftPressed = event.shiftKey;

				// Check if Ctrl + Shift + O is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 'o') {
					event.preventDefault();
					console.log('newChat');
					document.getElementById('sidebar-new-chat-button')?.click();
				}

				// Check if Shift + Esc is pressed
				if (isShiftPressed && event.key === 'Escape') {
					event.preventDefault();
					console.log('focusInput');
					document.getElementById('chat-input')?.focus();
				}

				// Check if Ctrl + Shift + ; is pressed
				if (isCtrlPressed && isShiftPressed && event.key === ';') {
					event.preventDefault();
					console.log('copyLastCodeBlock');
					const button = [...document.getElementsByClassName('copy-code-button')]?.at(-1);
					button?.click();
				}

				// Check if Ctrl + Shift + C is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 'c') {
					event.preventDefault();
					console.log('copyLastResponse');
					const button = [...document.getElementsByClassName('copy-response-button')]?.at(-1);
					console.log(button);
					button?.click();
				}

				// Check if Ctrl + Shift + S is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === 's') {
					event.preventDefault();
					console.log('toggleSidebar');
					document.getElementById('sidebar-toggle-button')?.click();
				}

				// Check if Ctrl + Shift + Backspace is pressed
				if (
					isCtrlPressed &&
					isShiftPressed &&
					(event.key === 'Backspace' || event.key === 'Delete')
				) {
					event.preventDefault();
					console.log('deleteChat');
					document.getElementById('delete-chat-button')?.click();
				}

				// Check if Ctrl + . is pressed
				if (isCtrlPressed && event.key === '.') {
					event.preventDefault();
					console.log('openSettings');
					showSettings.set(!$showSettings);
				}

				// Check if Ctrl + / is pressed
				if (isCtrlPressed && event.key === '/') {
					event.preventDefault();
					console.log('showShortcuts');
					document.getElementById('show-shortcuts-button')?.click();
				}

				// Check if Ctrl + Shift + ' is pressed
				if (isCtrlPressed && isShiftPressed && event.key.toLowerCase() === `'`) {
					event.preventDefault();
					console.log('temporaryChat');
					temporaryChatEnabled.set(!$temporaryChatEnabled);
					await goto('/');
					const newChatButton = document.getElementById('new-chat-button');
					setTimeout(() => {
						newChatButton?.click();
					}, 0);
				}
			});
			await tick();
		}

		loaded = true;
	});
</script>

<svelte:head>
	<title>Turing</title>
</svelte:head>

<div class="app">
	<div class="flex">
		<SidebarRedesign />
	</div>
	<div class="content">
		<slot/>
	</div>

</div>

<style lang="scss">
  .sidebar {
    width: 56px;
    overflow-y: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-content: center;
    align-items: center;
    @apply
    py-sm
    space-y-base;
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

	.content {
		@apply flex-grow flex
    bg-lvl-1
    w-full
    rounded-lg
		;
	}

  .chat {
    display: grid;
    grid-template-columns: 250px 1fr;

    @apply
    bg-lvl-2
    w-full
    rounded-lg;

    .chat__sidebar {
      @apply flex flex-col gap-base border-r border-slate-300 w-full py-lg px-base;
    }

		.chat__container {
			@apply flex flex-col gap-base w-full pb-lg h-full;
    }
  }

  .app {
    @apply flex
			bg-lvl-0
    p-sm
			gap-sm
		dark:bg-gray-900 h-svh max-h-[100dvh]
  }

  .icon {
    @apply p-xs
    rounded-sm
    text-slate-500;
    height: 24px;
    width: 24px;

    &.icon--lg {
      @apply p-sm
      text-xs
      rounded-sm;
      height: 40px;
      width: 40px;


    }

    &:active {
      @apply text-brand-500
      bg-brand-100;

    }

    &:hover {
      @apply text-brand-500
      bg-brand-100;
    }

  }

</style>

