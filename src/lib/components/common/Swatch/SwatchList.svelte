<script lang="ts">
	import Swatch from '$lib/components/common/Swatch/Swatch.svelte';
	type color = 'lime' | 'red' | 'blue' | 'yellow' | 'green' | 'gray' | 'purple' | 'pink' | 'indigo' | 'teal' | 'orange' | 'rose';


	let selectedColor = '';

	function handleSwatchClick(color: color) {
		selectedColor = color;
	}
</script>

<div class="flex flex-wrap gap-sm justify-end">
	{#each ['red', 'orange', 'yellow', 'green', 'lime', 'teal', 'blue', 'purple', 'pink'] as color}
		<Swatch
			{color}
			isSelected={selectedColor === color}
			on:click={()=>handleSwatchClick(color)}
		/>
	{/each}
</div>
