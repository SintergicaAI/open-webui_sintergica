<!-- BasesManagement.svelte -->
<script lang="ts">
	// Lógica para gestionar bases de conocimiento
	import { createEventDispatcher, getContext } from 'svelte';
	import Check from '$lib/components/common/Check/Check.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let groupBases = [];
	export let allBases = [];
	export let group;

	let selectedBaseIds: Set<string> = new Set(groupBases.map(base => base.id));

	function toggleBase(baseId: string): void {
		if (selectedBaseIds.has(baseId)) {
			selectedBaseIds.delete(baseId);
		} else {
			selectedBaseIds.add(baseId);
		}

		dispatch('update', {
			type: 'bases',
			ids: Array.from(selectedBaseIds)
		})
	}

	// $: {
	// 	if (groupBases) {
	// 		selectedBaseIds = new Set(groupBases.map(base => base.id));
	// 	}
	// }



</script>

<div class="w-full">
	<h2 class="text-lg font-medium mb-3">{$i18n.t('Available Knowledge Bases')}</h2>

	{#if allBases.length === 0}
		<p class="text-slate-500">{$i18n.t('Loading knowledge bases...')}</p>
	{:else}
		<div class="space-y-2">
			{#each allBases as base}
				<Check checked={selectedBaseIds.has(base.id)} on:change={() => toggleBase(base.id)} pill={base.name} info={base.files.length + ' ' + $i18n.t('files')}/>
			{/each}
		</div>
	{/if}
</div>
