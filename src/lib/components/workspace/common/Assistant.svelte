<script lang="ts">
	import { Square, SquareCheckBig } from 'lucide-svelte';
	import {Checkbox} from 'bits-ui';
	const i18n = getContext('i18n');


	export let id: string = '';
	export let name: string = '';
	export let description: string = '';
	export let checked: boolean = false;
	export let label: string = '';
	export let disabled: boolean = false;
	export let color: string = '';

	import { createEventDispatcher, getContext } from 'svelte';
	const dispatch = createEventDispatcher();

	function handleChange(event: CustomEvent) {
		checked = event.detail;
		dispatch('change', checked);
	}

</script>

<li class="list-none self-stretch group {!checked ? 'bg-slate-50 dark:bg-slate-800' : 'bg-brand-50 dark:bg-brand-900'} rounded-sm gap-sm w-full
flex flex-col items-start justify-center p-lg">
	<div class="flex justify-between w-full">
		{#if name}
			<label for={id} class="flex-grow cursor-pointer flex items-center gap-sm">
				<div class="flex items-start">
					<slot name="image">
					</slot>
				</div>
				<span class="text-title text-black dark:text-white group-hover:text-brand-500">{name}</span>
			</label>
		{/if}
		<Checkbox.Root {id}
									 {disabled}
									 bind:checked={checked}
									 onCheckedChange={handleChange}
									 class="self-stretch flex items-center justify-center gap-sm">
			<Checkbox.Indicator let:isChecked>
				{#if isChecked}
					<SquareCheckBig size={20} class="text-brand-500"/>
				{:else}
					<Square size={20} class="group-hover:text-brand-500 text-slate-500" />
				{/if}
			</Checkbox.Indicator>
		</Checkbox.Root>
	</div>
	<div class="flex-grow">
		<span class="text-slate-500">{description || $i18n.t('No description')}</span>
	</div>
</li>