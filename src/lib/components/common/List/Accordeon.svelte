<script>
	import { ChevronDown, ChevronUp } from 'lucide-svelte';

	let isOpen = false;
	export let title;
	export let icon;

	function toggleAccordion() {
		isOpen = !isOpen;
	}
</script>

<div class="accordion">
	<div class="accordion__header {isOpen ? 'accordion--open' : ''}" on:click={toggleAccordion}>
			<div class="accordion__header-content">
					{#if icon}
						<svelte:component this={icon} class="accordion__icon" size={24}/>
					{/if}
					<span class="accordion__header-text">{title}</span>
			</div>
			<span class="accordion__toggle">
				{#if isOpen}
					<ChevronUp size="24" />
				{:else}
					<ChevronDown size="24" />
				{/if}
			</span>
	</div>

	{#if isOpen}
		<div class="accordion__content">
			<slot>
				<p>Sin contenido.</p>
			</slot>
		</div>
	{/if}
</div>


<style lang="scss">
  .accordion {
    display: flex;
    width: 219px;
    flex-direction: column;
    align-items: flex-start;

    &__header {
      display: flex;
      height: 36px;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;
      animation-timing-function: ease-out;
      animation-duration: 300ms;
      @apply py-sm text-slate-500 cursor-pointer;

			&:hover {
				@apply text-brand-500;
      }

			&:active {
				@apply text-brand-800;
      }
    }

    &__header-content {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: var(--spacing-xs);
    }

    &__header-text {
      font-size: 1rem;
      color: inherit;
    }

    &__toggle {
      display: flex;
      align-items: center;
    }

    &__content {
      display: flex;
      max-width: 320px;
      flex-direction: column;
      align-items: flex-start;
      align-self: stretch;
    }

    &__item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;
      @apply p-sm text-slate-900;
    }

    &__item-text {
      flex-grow: 1;
    }

    &--open {
    }
  }
</style>