<script lang="ts">
	type color = 'red' | 'orange' | 'yellow' | 'green' | 'lime' | 'teal' | 'blue' | 'purple' | 'pink';
	export let color = 'red';
	export let isSelected = false;

	$: containerClass = `inline-flex p-xs rounded-sm hover:bg-brand-100 cursor-pointer ${
		isSelected ? 'bg-brand-200' : ''
	}`;

	$: circleClass = `w-6 h-6 rounded-full border-2 bg-${color}-200 border-${color}-500`;

</script>
<div class={`${containerClass}`} role="button" on:click>
	<div class={circleClass}></div>
</div>