<script lang="ts">
	import { Icon as IconType } from 'lucide-svelte';

	type ButtonVariant = 'primary' | 'default' | 'icon' | 'secondary' | 'danger' | 'warning' | 'success' | 'info';
	type ButtonSize = 'base' | 'sm' | 'lg';
	type IconPlacement = 'left' | 'right';
	type IconSize = 'sm' | 'base' | 'lg';

	export let variant: ButtonVariant = 'primary';
	export let size: ButtonSize = 'base';
	export let isDisabled: boolean = false;
	export let buttonClasses: string = ''; // Clases extra para el botón
	export let icon: typeof IconType; // Icono mostrado en el Switch
	export let iconPlacement: IconPlacement = 'left'; // Posición del ícono
	export let iconSize: IconSize = 'base';
	export let onClick: (event: MouseEvent) => void = () => {
	};
	const baseClasses = 'btn flex items-center justify-center font-inherit';

	function computedButtonClasses(): string {
		const isIconOnly = variant === 'icon';
		return `${baseClasses} ${buttonClasses} ${isIconOnly ? `btn-icon btn-icon-${variant} btn-icon-${size}` : `btn-${variant} btn-${size}`}`;
	}

	const iconSizesEquivalence = {
		'sm': '16',
		'base': '20',
		'lg': '24'
	};

	$: buttonClasses = computedButtonClasses();
</script>

<button
	class={buttonClasses}
	disabled={isDisabled}
	on:click|stopPropagation={onClick}
	{...$$restProps}
>
	{#if icon && (iconPlacement === 'left')}
		<svelte:component this={icon} size={iconSizesEquivalence[iconSize]} />
	{/if}
	<slot />
	{#if icon && iconPlacement === 'right'}
		<svelte:component this={icon} size={iconSizesEquivalence[iconSize]} />
	{/if}
</button>

<style lang="scss">
  .btn {

    &.btn-primary {
      @apply text-white bg-brand-500;
      @apply px-base py-2 rounded-sm transition-all focus:ring-2 focus:ring-brand-500;
      &:hover {
        background-color: #3092F7;
      }

      &:active {
        background-color: #005ACD;
      }

      &:disabled {
        background-color: #3092F7;
        cursor: not-allowed;
        opacity: 0.7;
      }
    }

    &.btn-danger {
      background-color: #FF4949;
      @apply text-white;
      &:hover {
        background-color: #FF7A7A;
      }

      &:active {
        background-color: #FF2626;
      }
    }

    &.btn-danger-outline {
      background-color: transparent;
      border: 1px solid #FF4949;
      @apply text-red-500;
      &:hover {
        background-color: #FF7A7A;
      }

      &:active {
        background-color: #FF2626;
      }
    }

    &.btn-base {
      @apply px-base;
    }

    &.btn-sm {
      @apply px-sm;
    }

    &.btn-lg {
      @apply px-lg;
    }

    &:focus {
      outline: none;
      box-shadow: 0 0 0 3px rgba(48, 146, 247, 0.5); // Indicar foco claramente
    }
  }

  .btn-icon {
    background-color: transparent;
    border: none;
    height: auto;
    width: auto;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    @apply text-slate-500 p-xs rounded-sm;

    &.btn-icon-primary {
      @apply text-brand-500;
      @apply p-sm rounded-sm;
    }

    &.btn-icon-base {
      @apply p-xs rounded-sm;
      //icon size base : 20px
    }

    &.btn-icon-lg {
      @apply p-sm rounded-sm;
      //icon size lg : 24px
    }

    &.btn-icon-sm {
      @apply p-xs rounded-sm;
      //icon size sm: 16px
    }

    &:hover {
      @apply text-brand-500;
    }

    &:focus {
      outline: none;
      box-shadow: 0 0 0 3px rgba(48, 146, 247, 0.5); // Indicar foco claramente
    }

    &:disabled {
      opacity: 0.4;
    }

  }
</style>