<script lang="ts">
	import { Icon as IconType } from 'lucide-svelte';

	export let icon: typeof IconType;
	export let initialActive = false;
	export let activeLabel = 'Activo';
	export let inactiveLabel = 'Inactivo';
	export let label: string = '';
	export let onToggle: (event: Event) => void;
	export let isDisabled = false;
	export let size: 'sm' | 'base' | 'lg' = 'base';
	export let value: string | number | boolean;
	export let variant: 'toggle' | 'static' = 'toggle';

	const iconSizeMap = { sm: '16', base: '20', lg: '24' };

	let active = initialActive;

	function toggleSwitch(event: Event) {
		if (!isDisabled) {
			active = !active;
			onToggle(event);
		}
	}
</script>

<div
	class="switch {active ? 'active' : ''}"
	tabindex="0"
	on:click={toggleSwitch}
	on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggleSwitch(e)}
	role="switch"
	aria-label={variant === 'toggle' ? (active ? activeLabel : inactiveLabel) : label}
	aria-checked={variant === 'toggle' ? active : undefined}
	aria-disabled={isDisabled.toString()}
	data-value={value}
>
	{#if icon}
		<svelte:component this={icon} size={iconSizeMap[size]} />
	{/if}
	<span class="text-button">
		{variant === 'toggle' ? (active ? activeLabel : inactiveLabel) : label}
	</span>
</div>

<style lang="scss">
	.switch {
		@apply
			py-xs
			px-sm
			rounded-sm
			inline-flex
			align-baseline
			gap-xs
		bg-slate-200
		text-slate-500;

		&:hover {
			@apply text-brand-500;
			cursor: pointer;
		}

		&.active {
			@apply
				text-brand-500
				bg-brand-100;

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