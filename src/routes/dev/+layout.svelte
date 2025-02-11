<script xmlns:slot="http://www.w3.org/1999/html">
	import '../../tailwind.css';
	import '../../app.css';
	import 'tippy.js/dist/tippy.css';
	import {
		ChevronDown,
		ChevronUp,
		CircleHelp,
		Clipboard,
		FolderPlus,
		LibrarySquare,
		LogOut,
		MessageCircle,
		MessageCirclePlus,
		MessagesSquare,
		Package,
		Pin,
		Search,
		Settings,
		Share2,
		SidebarClose,
		UserPen,
		Users
	} from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import InputChat from '$lib/components/chat/InputChat.svelte';
	import Accordeon from '$lib/components/common/List/Accordeon.svelte';
	import List from '$lib/components/common/List/List.svelte';
	import ModelList from '$lib/components/admin/Settings/Models/ModelList.svelte';

	let pinnedOpen = false;
	let folderOpen = false;

	function togglePinned() {
		pinnedOpen = !pinnedOpen;
	}

	function toggleFolder() {
		folderOpen = !folderOpen;
	}
</script>

<svelte:head>
	<title>Turing</title>
</svelte:head>


<div class="app">
	<aside class="sidebar">
		<div class="button-group button-group--lg">
			<div class="logo">

			</div>
			<div class="icon icon--lg">
				<MessageCircle />
			</div>

			<Button variant="icon" size="lg" icon={MessageCircle} buttonClasses="text-slate-500"/>
			<div class="icon icon--lg">
				<MessagesSquare />
			</div>
			<div class="icon icon--lg">
				<UserPen />
			</div>
			<div class="icon icon--lg">
				<Users />
			</div>
			<div class="icon icon--lg">
				<LibrarySquare />
			</div>
		</div>
		<div class="button-group">
			<div class="icon icon--lg">
				<LogOut />
			</div>
			<div>
				<img src="/static/favicon.png" alt="logo turing" class="w-[48px] h-[48px]" />
			</div>
		</div>
	</aside>
	<main class="chat">
		<aside class="chat__sidebar">
			<header class="flex justify-between items-center self-stretch">
				<h1 class="text-title">Turing</h1>
				<menu class="button-group-row text-slate-500">
					<Button variant="icon" size="sm" icon={Search} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={FolderPlus} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={MessageCirclePlus} buttonClasses="text-slate-500"/>
				</menu>
			</header>
			<div class="flex justify-center">
				<Button variant="primary" icon={MessageCirclePlus} size="sm" buttonClasses="text-button w-full gap-sm">
					Nuevo chat
				</Button>
			</div>
			<section class="flex-col justify-center items-center">
				<Accordeon title="Anclados" icon={Pin}>
					<List items={['Chat pinned 1','Chat pinned 2']}/>
				</Accordeon>
				<Accordeon title="Finanzas" icon={Pin}>
					<List items={['Chat finanzas 1','Chat finanzas 2']}/>
				</Accordeon>
			</section>
			<slot/>
			<div>

			</div>
		</aside>
		<article class="chat-container__content">
			<!-- Toolbar -->
			<header class="border-b border-slate-300 flex justify-between items-center p-base">
				<div class="flex gap-x-base items-center">
					<SidebarClose class="icon icon--lg text-slate-500" />
					<div class="flex gap-x-base items-center">
						<div class="flex flex-col justify-center align-center rounded-full bg-orange-400 w-8 h-8 gap-sm ">
						</div>
						<h2 class="text-title">Model name</h2>
						<ModelList />
						<ChevronDown class="text-slate-500"/>
					</div>
					<span class="text-slate-500">|</span>
					<h2 class="text-subtitle">Generated title</h2>
				</div>

				<div class="flex gap-x-sm">
					<Button variant="icon" size="sm" icon={Package} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={Clipboard} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={Share2} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={CircleHelp} buttonClasses="text-slate-500"/>
					<Button variant="icon" size="sm" icon={Settings} buttonClasses="text-slate-500"/>
				</div>

			</header>
			<section class="flex justify-center items-end w-full h-full">
				<InputChat />
			</section>
		</article>

	</main>

</div>

<style lang="scss">
  *, :after, :before {
    box-sizing: border-box;
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

		.chat-container__content {
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

