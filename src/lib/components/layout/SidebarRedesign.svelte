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
	import { WEBUI_BASE_URL } from '$lib/constants';

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
	import { LibrarySquare, LogOut, MessageCircle, MessagesSquare, UserPen, Users } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import NavigationMenu from '$lib/components/layout/NavigationMenu.svelte';

	const i18n = getContext('i18n');

	const BREAKPOINT = 768;

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

	export let customClass: string = '';

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

	const onFocus = () => {};

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

	function logout() {
		return '';
	}

	const routes = [
		{ name: 'Chat', path: '/dev', icon:MessageCircle},
		{ name: 'Usuario', path: '/dev/user', icon: UserPen },
		{ name: 'Usuarios', path: '/dev/users', icon: Users },
		{ name: 'Conocimiento', path: '/dev/knowledge', icon: LibrarySquare}
	];
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<aside class="sidebar {customClass}">
	<div class="button-group button-group--lg">
		<div class="logo"/>
		<NavigationMenu routes={routes} />
		<div data-svg-wrapper>
			<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path fill-rule="evenodd" clip-rule="evenodd" d="M10.6873 11.595C11.1116 11.0859 11.8683 11.0171 12.3774 11.4414L17.1774 15.4413C17.4682 15.6837 17.6276 16.0491 17.6074 16.4272C17.5872 16.8053 17.3898 17.1516 17.0748 17.3617L12.2748 20.5616C11.7234 20.9293 10.9783 20.7803 10.6107 20.2288C10.2431 19.6774 10.3921 18.9324 10.9435 18.5647L14.4063 16.2562L10.841 13.2851C10.3318 12.8608 10.263 12.1041 10.6873 11.595ZM25.609 18.7632C26.9345 18.7632 28.009 17.6887 28.009 16.3632C28.009 15.0377 26.9345 13.9632 25.609 13.9632C24.2836 13.9632 23.2091 15.0377 23.2091 16.3632C23.2091 17.6887 24.2836 18.7632 25.609 18.7632ZM25.609 21.1631C28.26 21.1631 30.409 19.0141 30.409 16.3632C30.409 13.7122 28.26 11.5632 25.609 11.5632C22.9581 11.5632 20.8091 13.7122 20.8091 16.3632C20.8091 19.0141 22.9581 21.1631 25.609 21.1631ZM15.7204 24.3822C15.2891 23.879 14.5315 23.8207 14.0283 24.252C13.5251 24.6834 13.4669 25.4409 13.8982 25.9441C14.8244 27.0247 16.5121 28.3342 18.6326 28.7234C20.8497 29.1303 23.3535 28.4944 25.6885 25.9797C26.1395 25.494 26.1114 24.7348 25.6257 24.2838C25.1401 23.8328 24.3808 23.861 23.9299 24.3466C22.1049 26.3119 20.4088 26.6093 19.0658 26.3629C17.6264 26.0987 16.3942 25.1683 15.7204 24.3822Z" fill="#64748B"/>
			</svg>
		</div>
	</div>
	<div class="button-group">
		<div class="icon icon--lg" on:click={logout}>
			<LogOut />
		</div>
		<div>
			<img src="/static/favicon.png" alt="logo turing" class="w-[48px] h-[48px]" />
		</div>
	</div>
</aside>

<style lang="scss">
    .scrollbar-hidden:active::-webkit-scrollbar-thumb,
    .scrollbar-hidden:focus::-webkit-scrollbar-thumb,
    .scrollbar-hidden:hover::-webkit-scrollbar-thumb {
        visibility: visible;
    }
    .scrollbar-hidden::-webkit-scrollbar-thumb {
        visibility: hidden;
    }

    $sidebar-width: 56px;

    .sidebar {
      width: $sidebar-width;
      overflow-y: hidden;

      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;

      @apply py-sm space-y-base;
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

    .chat {
      display: grid;
      grid-template-columns: 250px 1fr;

      @apply
      bg-slate-100
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
      px-sm
      py-base
      space-x-sm
      bg-slate-200
      m-0
      h-screen
    }

    .logo {
      height: 48px;
      width: 48px;
      border-radius: 8px;
      background-image: url('/favicon.png');
      background-color: lightgray;
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
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
