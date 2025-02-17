<script lang="ts">
	import { Icon as IconType } from 'lucide-svelte';

	// Extracted types (could be in a separate `types.ts` file)
	type ButtonVariant =
		'primary'
		| 'default'
		| 'icon'
		| 'secondary'
		| 'danger'
		| 'warning'
		| 'success'
		| 'info'
		| 'outline-primary'
		| 'outline-danger';
	type ButtonSize = 'base' | 'sm' | 'lg';
	type IconPlacement = 'left' | 'right';
	type IconSize = 'sm' | 'base' | 'lg';

	// Component Props
	export let variant: ButtonVariant = 'primary';
	export let size: ButtonSize = 'base';
	export let isDisabled: boolean = false;
	export let buttonClasses: string = '';
	export let icon: typeof IconType;
	export let iconPlacement: IconPlacement = 'left';
	export let iconSize: IconSize = 'base';
	export let onClick: (event: MouseEvent) => void = () => {
	};

	// Constants
	const BASE_CLASSES = 'btn flex items-center justify-center font-inherit gap-sm';
	const ICON_SIZES = {
		sm: '16',
		base: '20',
		lg: '24'
	};

	/** Utility function to compute dynamic classes */
	const computeButtonClasses = (
		variant: ButtonVariant,
		size: ButtonSize,
		buttonClasses: string
	) => {
		const isIconOnly = variant === 'icon';
		return `${BASE_CLASSES} ${buttonClasses} ${
			isIconOnly
				? `btn-icon btn-icon-${variant} btn-icon-${size}`
				: `btn-${variant} btn-${size}`
		}`;
	};

	// Reactive derived states
	$: computedClasses = computeButtonClasses(variant, size, buttonClasses);

</script>

<!-- Main Button -->
<button
	class={computedClasses}
	disabled={isDisabled}
	on:click|stopPropagation={onClick}
	{...$$restProps}
>
	{#if icon && (iconPlacement === 'left')}
		<svelte:component this={icon} size={ICON_SIZES[iconSize]} />
	{/if}
	<slot />
	{#if icon && iconPlacement === 'right'}
		<svelte:component this={icon} size={ICON_SIZES[iconSize]} />
	{/if}
</button>

<style lang="scss">
  .btn {
		@apply rounded-sm py-sm px-base;
		white-space: nowrap;
		flex-wrap: nowrap;

    &.btn-primary {
      @apply text-white bg-brand-500;
      @apply px-base py-2 rounded-sm transition-all focus:ring-2 focus:ring-brand-500;
      &:hover {
        @apply bg-brand-400
      }

      &:active {
				@apply bg-brand-600;
      }

      &:disabled {
        background-color: #3092f7;
        cursor: not-allowed;
        opacity: 0.4;
      }
    }

    // Variants outline
    &.btn-outline-primary {
      background-color: transparent;
      border: 1px solid #3092f7;
      @apply text-brand-500 transition-all;
      &:hover {
        @apply bg-brand-50;
      }

      &:active {
        @apply bg-brand-200;
      }

			&:disabled {
				opacity: 0.4;
				cursor: not-allowed;
      }
    }

    &.btn-outline-danger {
      background-color: transparent;
      border: 1px solid #ff4949;
      @apply text-red-500 transition-all;
      &:hover {
        background-color: #ffeaea;
      }

      &:active {
        background-color: #ffdbdb;
      }
    }

    // Variants
    &.btn-danger {
      background-color: #ff4949;
      @apply text-white;
      &:hover {
        background-color: #ff7a7a;
      }

      &:active {
        background-color: #ff2626;
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
      box-shadow: 0 0 0 3px rgba(48, 146, 247, 0.5); // Clearer focus indication
    }
  }

  .btn-icon {
    background-color: transparent;
    border: none;
    display: inline-flex;
    justify-content: center;
    align-items: center;

    &.btn-icon-primary {
      @apply text-brand-500;
    }

    &.btn-icon-base {
      @apply p-xs rounded-sm;
    }

    &.btn-icon-lg {
      @apply p-sm rounded-sm;
    }

    &.btn-icon-sm {
      @apply p-xs rounded-sm;
    }

    &:hover {
      @apply text-brand-500;
    }

    &:disabled {
      opacity: 0.4;
    }
  }
</style>