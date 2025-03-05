<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import {
		WEBUI_NAME,
		showSidebar,
		functions,
		user,
		mobile,
		models,
		prompts,
		knowledge,
		tools
	} from '$lib/stores';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	import MenuLines from '$lib/components/icons/MenuLines.svelte';
	import { CircleHelp } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		if ($user?.role !== 'admin') {
			if ($page.url.pathname.includes('/models') && !$user?.permissions?.workspace?.models) {
				goto('/');
			} else if (
				$page.url.pathname.includes('/knowledge') &&
				!$user?.permissions?.workspace?.knowledge
			) {
				goto('/');
			} else if (
				$page.url.pathname.includes('/prompts') &&
				!$user?.permissions?.workspace?.prompts
			) {
				goto('/');
			} else if ($page.url.pathname.includes('/tools') && !$user?.permissions?.workspace?.tools) {
				goto('/');
			}
		}

		loaded = true;
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Workspace')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<main
		class=" relative knowledge bg-lvl-1 scrollbar-none flex flex-col w-full h-full max-h-[100dvh]"
	>
		{#if $user?.role === 'admin' || $user?.permissions?.workspace?.models}
			<div class="knowledge__header">
				<div class="flex items-center gap-sm">
					<h2 class="flex text-title dark:text-white items-center">
						{$i18n.t('Models')}
					</h2>
					<Button size="base" variant="icon" icon={CircleHelp} buttonClasses="text-slate-500 dark:text-slate-400" />
				</div>
			</div>
		{/if}
		<div class="  knowledge__content" id="workspace-container">
			<slot />
		</div>
	</main>
{/if}

<style lang="scss">
  .knowledge {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 100px 1fr;
    &__header {
      @apply flex justify-between px-base py-lg border-b;
    }

    &__content {
      @apply overflow-y-auto gap-2;

    }

    &__action-panel {
      @apply flex justify-between items-center py-2xl px-lg;
    }

    &__container {
      @apply py-2xl px-lg;

    }
  }

	</style>