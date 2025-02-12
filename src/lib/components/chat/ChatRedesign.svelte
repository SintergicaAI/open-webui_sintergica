<script>
	import InputChat from '$lib/components/chat/InputChat.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import {
		ChevronDown, CircleHelp,
		FolderPlus,
		MessageCirclePlus,
		Package,
		Pin,
		Search, Settings,
		Share2,
		SidebarClose,
		Clipboard,
	} from 'lucide-svelte';
	import Accordeon from '$lib/components/common/List/Accordeon.svelte';
	import List from '$lib/components/common/List/List.svelte';
	import NavbarRedesign from '$lib/components/layout/NavbarRedesign.svelte';

	console.log('Chat redesign');
</script>

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
	</aside>
	<article class="chat__container">
		<!-- Toolbar -->
		<NavbarRedesign title="Title"/>
		<section class="flex justify-center items-end w-full h-full">
			<InputChat />
		</section>
	</article>
</main>

<style lang="scss">
  *, :after, :before {
    box-sizing: border-box;
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
    bg-lvl-1
    w-full
    rounded-lg;

    .chat__sidebar {
      @apply flex flex-col flex-grow gap-base border-r border-slate-300 w-full py-lg px-base h-full;
    }

    .chat__container {
      @apply flex flex-col gap-base w-full pb-lg h-full;
    }
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