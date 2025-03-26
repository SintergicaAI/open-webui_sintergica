<!-- AssistantsManagement.svelte -->
<script lang="ts">
	// Lógica para gestionar asistentes

import Option from '$lib/components/workspace/Models/Option.svelte';
	import { getModels } from '$lib/apis';
	import { onMount } from 'svelte';

	let models: any = [];

	let info = {
		id: '',
		base_model_id: null,
		name: '',
		meta: {
			profile_image_url: '/static/favicon.png',
			description: '',
			suggestion_prompts: null,
			tags: []
		},
		params: {
			system: ''
		}
	};

onMount(async () => {
	models = await getModels(localStorage.token, false)


})
</script>

<div class="w-full">
	<!-- UI para gestionar asistentes -->
	<p>Interfaz para gestionar asistentes</p>

	{#each models as model}
		<Option id={model.id} selected={info.base_model_id === model.id} heading={model.name} description={model?.meta?.description ?? 'No description'} src={model?.meta?.profile_image_url ?? '/static/gpt.png'}
						on:click>
			<img sizes="100vw" src={model?.meta?.profile_image_url ?? '/static/gemini.png'} alt="splash" class="size-6 object-cover" slot="image"/>
		</Option>

	{/each}
</div>