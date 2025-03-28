<script lang="ts">
	import Swatch from '$lib/components/common/Swatch/Swatch.svelte';
	import { createEventDispatcher } from 'svelte';
	import type { OnChangeFn } from 'bits-ui/dist/internal';
	import {RadioGroup} from 'bits-ui';

	type Color = 'red' | 'orange' | 'yellow' | 'lime' | 'green' | 'sky' | 'blue' | 'purple' | 'pink';

	export let value: Color = ''
	export let colors: Color[] = ['red', 'orange', 'yellow', 'lime', 'green', 'sky', 'blue', 'purple', 'pink']


	const dispatch = createEventDispatcher<{
		change: {color: Color}
	}>();

	function handleColorChange(color: OnChangeFn<Color>) {
		dispatch('change', { color: color });
	}

</script>


<RadioGroup.Root value={value}
								 onValueChange={handleColorChange} class="flex flex-wrap gap-sm justify-end">
	{#each colors as color}
		<RadioGroup.Item value={color}>
			<Swatch {color} isSelected={value === color}/>
		</RadioGroup.Item>
	{/each}
</RadioGroup.Root>
