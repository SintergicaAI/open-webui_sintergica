<script>
	import { onMount } from 'svelte';
	import { knowledge } from '$lib/stores';

	import { getKnowledgeBases } from '$lib/apis/knowledge';
	import KnowledgeBaseOverview from '$lib/components/workspace/KnowledgeRedesign.svelte';


	onMount(async () => {
		await Promise.all([
			(async () => {
				knowledge.set(await getKnowledgeBases(localStorage.token));
			})()
		]);
	});
</script>

{#if $knowledge !== null}
	<KnowledgeBaseOverview />
{/if}
