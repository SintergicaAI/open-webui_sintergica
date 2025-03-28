<!-- AssistantsManagement.svelte -->
<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import Assistant from '$lib/components/workspace/common/Assistant.svelte';
	import TuringFace from '$lib/components/icons/TuringFace.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let groupAssistants = [];
	export let allAssistants = [];
	export let group;

	let selectedModelIds = new Set(groupAssistants.map(assistant => assistant.id));

	function toggleModel(modelId) {
		if (selectedModelIds.has(modelId)) {
			selectedModelIds.delete(modelId);
		} else {
			selectedModelIds.add(modelId);
		}

		dispatch('update', {
			type: 'assistants',
			ids: Array.from(selectedModelIds)
		});
	}
</script>

<div class="w-full">
	<h2 class="text-lg font-medium mb-3">{$i18n.t('Available Assistants')}</h2>

	{#if allAssistants.length === 0}
		<p class="text-slate-500">{$i18n.t('Loading models...')}</p>
	{:else}
		<div class="space-y-2">
			{#each allAssistants as model}
				<Assistant label={model.name} name={model.name} id={model.id} description={model?.meta?.description} checked={selectedModelIds.has(model.id)} on:change={() => toggleModel(model.id)}>
						<div class="size-9 object-cover flex flex-col items-center justify-center rounded-sm {model.meta?.color ? `bg-${model.meta?.color}-400` : `bg-red-400`}" slot="image">
							{#if model.meta?.profile_image_url}
								<img sizes="100vw" src={model.meta.profile_image_url} alt="splash" class="size-9 object-cover"/>
							{:else}
								<TuringFace className="text-slate-50"/>
							{/if}
						</div>
				</Assistant>
			{/each}
		</div>
	{/if}
</div>