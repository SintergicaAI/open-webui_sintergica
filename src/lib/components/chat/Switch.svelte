<script lang="ts">
	import { Icon as IconType } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte'
	import {Switch} from 'bits-ui'

	export let icon: typeof IconType;
	export let initialActive = false;
	export let activeLabel = 'Activo';
	export let inactiveLabel = 'Inactivo';
	export let label: string = '';
	export let isDisabled = false;
	export let size: 'sm' | 'base' | 'lg' = 'base';
	export let value: string | number | boolean;
	export let variant: 'toggle' | 'static' = 'toggle';

	export let state = false;
	const iconSizeMap = { sm: '16', base: '20', lg: '24' };

	const dispatch = createEventDispatcher();
	$: dispatch('change', state)
	let active = initialActive;

	function toggleSwitch(event: Event) {
		if (!isDisabled) {
			active = !active;
		}
	}
</script>

<Switch.Root
	bind:checked={state}
	>
	<div
		class="switch {state ? 'active' : ''}"
		tabindex="0"
		on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggleSwitch(e)}
		role="switch"
		aria-label={variant === 'toggle' ? (state ? activeLabel : inactiveLabel) : label}
		aria-checked={variant === 'toggle' ? state : undefined}
		data-value={value}
	>
		{#if icon}
			<svelte:component this={icon} size={iconSizeMap[size]} />
		{/if}
		<span class="text-button">
		{variant === 'toggle' ? (state ? activeLabel : inactiveLabel) : label}
	</span>
	</div>
</Switch.Root>


<style lang="scss">
	.switch {
		@apply
			py-sm
			px-base
			rounded-sm
			inline-flex
			align-baseline
			gap-xs
		bg-slate-200
		dark:bg-slate-800
		text-slate-500;

		&:hover {
			@apply text-brand-500;
			cursor: pointer;
		}

		&.active {
			@apply
				text-brand-500
				bg-brand-100
				dark:bg-brand-800;

			&:disabled {
				opacity: 0.4;
			}
		}

		&:disabled {
			opacity: 0.4;
		}

    &:focus {
      @apply outline-none ring-2 ring-offset-2 ring-brand-500;
    }
	}
</style>