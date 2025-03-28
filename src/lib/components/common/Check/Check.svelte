<!-- Check.svelte -->
<script lang="ts">
	import {Checkbox} from 'bits-ui'
	import { Square, SquareCheckBig } from 'lucide-svelte';

	export let id: string = '';
	export let checked: boolean = false;
	export let label: string = '';
	export let disabled: boolean = false;
	export let info: string = '';
	export let pill: string = '';
	export let avatar: string = '';
	export let pillColor: string = '';

	import { createEventDispatcher } from 'svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	const dispatch = createEventDispatcher();

	function handleChange(event: CustomEvent) {
		checked = event.detail;
		dispatch('change', checked);
	}
</script>

<div class="group {!checked ? 'bg-slate-50 dark:bg-slate-800' : 'bg-brand-50 dark:bg-brand-900'} rounded-sm gap-sm w-full flex justify-between items-center p-sm">
	{#if label || pill}
		<label for={id} class="flex-grow cursor-pointer flex items-center gap-sm">
			{#if avatar}
				<Avatar name={avatar} />
			{/if}
			{#if pill}
				<Pill pillColor={pillColor || 'brand'} text={pill} />
			{/if}
			<span class="text-slate-500 group-hover:text-brand-500">{label}</span>
		</label>
	{/if}
	<Checkbox.Root
		{id}
		{disabled}
		bind:checked={checked}
		onCheckedChange={handleChange}
		class="self-stretch flex items-center justify-center gap-sm"
	>
		{#if info}
			<span class="text-label group-hover:text-brand-500 text-slate-400">{info}</span>
		{/if}
		<Checkbox.Indicator let:isChecked>
			{#if isChecked}
				<SquareCheckBig size={20} class="text-brand-500"/>
			{:else}
				<Square size={20} class="group-hover:text-brand-500 text-slate-500" />
			{/if}
		</Checkbox.Indicator>
	</Checkbox.Root>
</div>