<script lang="ts">
	type ButtonVariant = 'primary' | 'default' | 'primary-outlined' | 'danger-outlined' | 'secondary' | 'danger' | 'warning' | 'success' | 'info';

	export let variant: ButtonVariant = 'primary';
	export let size: string = 'base';
	export let isDisabled: boolean = true;
	export let icon: any | undefined = undefined;

	$: buttonClasses = `btn btn-${variant} btn-${size}`;
</script>

<button class={ buttonClasses } disabled={isDisabled}>
	{#if icon}
		{#if typeof icon === 'function'}
			<svelte:component this={icon} />
		{/if}
	{/if}
	<slot />
</button>

<style lang="scss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
	.text-button {
		font-size: 16pt;
    @apply font-medium;
	}
  .btn {
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: inherit;
		height: 36px;
		@apply space-x-sm;
		@apply px-base py-2;
    @apply rounded-sm;
		@apply text-button;

		&.btn-primary {
			@apply bg-brand-500;
			@apply text-white;
      &:hover {
        background-color: #3092F7;

      }
			&:active {
				background-color: #005ACD;
			}
			&:disabled {
				background-color: #3092F7;
      }
		}

		&.btn-primary-outlined {
			background-color: transparent;
			border: 1px solid #006EFA;
			@apply text-brand-500;
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

		&.btn-danger-outlined {
			background-color: transparent;
			border: 1px solid #FF4949;
			@apply text-red-500;
			&:hover {
				background-color: #FF7A7A;
      }
			&:active {
				background-color: #FF2626;
      }
			&:disabled {
				border: 1px solid #FF7A7A;
				color: #FF7A7A;
				cursor: not-allowed;
      }
		}
  }
</style>