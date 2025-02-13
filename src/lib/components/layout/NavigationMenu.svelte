<script lang="ts">
	import { page } from '$app/stores';
	import { derived } from 'svelte/store';

	export let routes: { name: string; path: string; icon: any }[] = [];

	const currentPath = derived(page, ($page) => $page.url.pathname);

	function isActive(path: string) {
		return $currentPath === path ? 'active' : '';
	}
</script>

<nav class="nav">
	{#each routes as route}
		<a
			href={route.path}
			class="nav__link {isActive(route.path)}"
			aria-label={route.name}
		>
			<svelte:component this={route.icon} aria-hidden="true" class="nav__icon" />
		<span class="sr-only">{route.name}</span>
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