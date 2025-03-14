<script>
	import Switch from '$lib/components/chat/Switch.svelte';
	import { CodeXml, FileText, Globe, Table, Type } from 'lucide-svelte';

	let activeFilters = new Set();
	const filterOptions = [
		{ label: 'pdf', icon: FileText },
		{ label: 'text', icon: Table },
		{ label: 'table', icon: Type },
		{ label: 'website', icon: Globe },
		{ label: 'script', icon: CodeXml }
	];

	function toggleFilter(filter) {
		activeFilters.has(filter) ? activeFilters.delete(filter) : activeFilters.add(filter);
	}
</script>

<div class="flex flex-row gap-xs">
	{#each filterOptions as { label, icon }}
		<Switch
			icon={icon}
			value={label}
			on:change={() => toggleFilter(label)}
			initialActive={false}
			size="sm"
			label={label}
			variant="static"
		/>
	{/each}
</div>