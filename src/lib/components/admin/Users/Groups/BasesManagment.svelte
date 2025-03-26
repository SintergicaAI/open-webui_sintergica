<!-- BasesManagement.svelte -->
<script lang="ts">
	// Lógica para gestionar bases de conocimiento
	import { onMount } from 'svelte';
	import { getKnowledgeBases } from '$lib/apis/knowledge';

	let knowledgeBases: any;

	onMount(async () => {
		knowledgeBases = await getKnowledgeBases(localStorage.token).catch(
			(error) => console.log(error)
		);

	})
</script>

<div class="w-full">
	<!-- UI para gestionar bases de conocimiento -->
	<p>Interfaz para gestionar bases de conocimiento</p>


	{#if knowledgeBases}
		<ul>
			{#each knowledgeBases as base}
				<li>{base.name}</li>
			{/each}
		</ul>
	{/if}
</div>