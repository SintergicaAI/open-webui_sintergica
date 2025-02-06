<script lang="ts">
	import { Search } from 'lucide-svelte';

	type ButtonVariant = 'primary' | 'default' | 'secondary' | 'danger' | 'warning' | 'success' | 'info';

	export let variant: ButtonVariant = 'primary';
	export let size: string = 'base';
	export let isDisabled: boolean = true;
	export let icon: string = '';

	$: buttonClasses = `btn btn-${variant} btn-${size}`;
</script>

<button class={ buttonClasses } disabled={isDisabled}>
	<Search size={16}/>
	<slot />
</button>

<style lang="scss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
  .btn {
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: inherit;
		@apply px-base py-2;
    @apply rounded-sm;

		&.btn-primary {
			background-color: #006EFA;
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

  }
</style>