<script>
	import { onMount } from 'svelte';
	import { models } from '$lib/stores';
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/workspace/Models.svelte';
	import ModelsRedesign from '$lib/components/workspace/ModelsRedesign.svelte';

	onMount(async () => {
		await Promise.all([
			(async () => {
				models.set(await getModels(localStorage.token));
			})()
		]);
	});
</script>

{#if $models !== null}
	<ModelsRedesign />
{/if}
