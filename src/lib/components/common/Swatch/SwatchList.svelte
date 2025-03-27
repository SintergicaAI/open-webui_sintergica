<script lang="ts">
	import Swatch from '$lib/components/common/Swatch/Swatch.svelte';
	import { onMount } from 'svelte';
	import { getUserSettings, updateUserSettings } from '$lib/apis/users';
	import { settings } from '$lib/stores';
	type color = 'red' | 'orange' | 'yellow' | 'lime' | 'green' | 'sky' | 'blue' | 'purple' | 'pink';
	export let key;


	let selectedColor = '';

	async function handleSwatchClick(color: color) {
		const response = await updateUserSettings(localStorage.token, { ui: { knowledgeColor: color } }).catch(err => console.log(err));
		selectedColor = response.ui.knowledgeColor;
		const updated = { knowledgeColor: color };
		await settings.set({ ...$settings, ...updated });
	}

	onMount(async () => {
		try {
			const response = await getUserSettings(localStorage.token).catch(err => console.log(err));
			selectedColor = response.ui.knowledgeColor;
			const updated = {knowledgeColor: response.ui.knowledgeColor};
			await settings.set({ ...$settings, ...updated });
		} catch (e) {
			console.log(e);
		}
	})
</script>

<div class="flex flex-wrap gap-sm justify-end">
	{#each ['red', 'orange', 'yellow', 'lime', 'green', 'sky', 'blue', 'purple', 'pink'] as color}
		<Swatch
			{color}
			isSelected={selectedColor === color}
			on:click={()=>handleSwatchClick(color)}
		/>
	{/each}
</div>
