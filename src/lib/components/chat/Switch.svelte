<script lang="ts">
	import { Icon as IconType } from 'lucide-svelte';

	export let icon: typeof IconType; // Icono mostrado en el Switch
	export let initialActive: boolean = false; // Estado inicial del Switch
	export let activeLabel: string = 'Activo';
	export let inactiveLabel: string = 'Inactivo';
	export let onToggle: (event: Event) => void; // Función callback al cambiar estado
	export let isDisabled: boolean = false;
	export let size: 'sm' | 'base' | 'lg' = 'base';
	const iconSizesEquivalence = {
		'sm': '16',
		'base': '20',
		'lg': '24'
	}

	let isActive = initialActive;

	function handleClick(event: Event) {
		isActive = !isActive;
		onToggle(event);
	}
</script>

<div
	class="switch {isActive ? 'active' : ''}"
	tabindex="0"
	on:click={handleClick}
	on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick(e); }}
	aria-label={inactiveLabel}
	role="switch"
	aria-checked="{isActive}"
	aria-disabled="{isDisabled}"
>
	{#if icon}
		<svelte:component this={icon} size={iconSizesEquivalence[size]} />
	{/if}
	<span class="text-button">
		{isActive ? activeLabel : inactiveLabel}
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
		bg-slate-100
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

    }
	}
</style>