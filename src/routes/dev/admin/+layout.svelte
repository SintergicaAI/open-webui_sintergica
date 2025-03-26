<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';

	import { WEBUI_NAME, showSidebar, user } from '$lib/stores';
	import MenuLines from '$lib/components/icons/MenuLines.svelte';
	import { page } from '$app/stores';
	import { CircleHelp } from 'lucide-svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
		}
		loaded = true;
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Admin Panel')} | {$WEBUI_NAME}
	</title>
</svelte:head>

{#if loaded}
	<div
		class=" flex flex-col w-full {$showSidebar}">
		<header class="border-b bg-lvl-2 px-base py-lg flex items-center gap-sm">
			<h1 class="text-title dark:text-white">{$i18n.t('Users')}</h1>
			<CircleHelp size="20"/>
		</header>

		<section class=" flex-1 max-h-full overflow-y-auto py-2xl px-lg ">
			<slot />
		</section>
	</div>
{/if}