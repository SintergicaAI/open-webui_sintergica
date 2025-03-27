<script lang="ts">
	import{
	user
	} from '$lib/stores';
	import { showArchivedChats } from '$lib/stores';
	import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import { onMount } from 'svelte';
	export let routes: { name: string; path: string; icon: any }[] = [];
	import {page} from '$app/stores';
	import TuringFace from '$lib/components/icons/TuringFace.svelte';
	import MessageCircleDashedPlus from '$lib/components/icons/MessageCircleDashedPlus.svelte';

	let currentPath = '';

	onMount(() => {
		currentPath = window.location.pathname;

	})

	function navigateTo(path: string) {
		currentPath = path;
		window.history.pushState({}, '', path);
	}
</script>

<nav class="nav">
	{#if $user !== undefined}
		<UserMenu
			className="max-w-[200px]"
			role={$user.role}
			on:show={(e) => {
							if (e.detail === 'archived-chat') {
								showArchivedChats.set(true);
							}
						}}
		>
			<button
				class="select-none flex rounded-xl p-1.5 w-full hover:bg-gray-50 dark:hover:bg-gray-850 transition"
				aria-label="User Menu">
				<Avatar name={$user.name}/>
			</button>
		</UserMenu>
	{/if}
	{#each routes as {name, path, icon}}
		<a
			href={path}
			class="nav__link {$page.url.pathname === path ? 'active' : ''}"
			aria-label={name}
		>
			<svelte:component this={icon} aria-hidden="true" class="nav__icon" />
			<span class="sr-only">{name}</span>
		</a>
	{/each}

</nav>

<style lang="scss">
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
    .nav {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
    }

    .nav__link {
        text-decoration: none;

      @apply p-sm
      rounded-sm
      text-slate-500;
        transition: background-color 0.2s ease, color 0.2s ease;
    }

    .nav__link.active {
        @apply bg-brand-100 text-brand-500;
    }

    .nav__link:hover {
        background-color: var(--bg-color-hover, #0056b3);
        color: var(--color-hover, white);
    }

    .nav__icon {
      @apply p-sm
      rounded-sm
      text-slate-500;
    }

    .sr-only {
        border: 0;
        clip: rect(0, 0, 0, 0);
        height: 1px;
        margin: -1px;
        overflow: hidden;
        padding: 0;
        position: absolute;
        width: 1px;
        white-space: nowrap;
    }
</style>