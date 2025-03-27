<!-- AssistantsManagement.svelte -->
<script lang="ts">
	// Lógica para gestionar asistentes
	import { createEventDispatcher, getContext } from 'svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	// Recibir los asistentes actuales del grupo y todos los modelos disponibles
	export let groupAssistants = [];
	export let allAssistants = [];
	export let group;

	// Crear un conjunto para determinar rápidamente cuáles están seleccionados
	let selectedModelIds = new Set(groupAssistants.map(assistant => assistant.id));

	// Función para actualizar los asistentes seleccionados
	function toggleModel(modelId) {
		if (selectedModelIds.has(modelId)) {
			selectedModelIds.delete(modelId);
		} else {
			selectedModelIds.add(modelId);
		}

		// Notificar cambios
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
				<div class="flex items-center p-2 border rounded">
					<input
						type="checkbox"
						id="model-{model.id}"
						checked={selectedModelIds.has(model.id)}
						on:change={() => toggleModel(model.id)}
						class="mr-2"
					/>
					<label for="model-{model.id}" class="flex-grow">{model.name}</label>
				</div>
			{/each}
		</div>
	{/if}
</div>


<!--<div class="w-full">-->
<!--	&lt;!&ndash; UI para gestionar asistentes &ndash;&gt;-->
<!--	<p>Interfaz para gestionar asistentes</p>-->

<!--	{#each models as model}-->
<!--		<Option id={model.id} selected={info.base_model_id === model.id} heading={model.name} description={model?.meta?.description ?? 'No description'} src={model?.meta?.profile_image_url ?? '/static/gpt.png'}-->
<!--						on:click>-->
<!--			<img sizes="100vw" src={model?.meta?.profile_image_url ?? '/static/gemini.png'} alt="splash" class="size-6 object-cover" slot="image"/>-->
<!--		</Option>-->

<!--	{/each}-->
<!--</div>-->
