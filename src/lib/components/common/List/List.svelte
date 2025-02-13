<script lang="ts">
	import { Pin } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { createPinnedStore } from '$lib/stores/PinnedStore';
	import { Toggle } from 'bits-ui';


	export let items: string[] = [];
	const pinnedStore = createPinnedStore(items)
	let pinned: boolean[] = [];

	function togglePinned(index: number) {
		pinnedStore.togglePinned(index); // Alternar estado desde el store
	}
</script>

<div class="list-container">
	{#if items.length > 0}
		{#each items as item, index}
			<div class="list-item">
				<span class="list-content text-base">
					{item}
					{#if $pinnedStore[index]} (Pinneado) {/if}
				</span>
				<div>
					<Button
						variant="icon"
						size="sm"
						icon={Pin}
						onClick={() => togglePinned(index)}
						aria-label={$pinnedStore[index] ? "Quitar pin" : "Añadir pin"}
						aria-pressed={$pinnedStore[index] ? "true" : "false"}
					/>

				</div>
			</div>
		{/each}
	{:else}
		<p>No hay elementos en la lista.</p>
	{/if}
</div>

<style lang="scss">
  .list-container {
    @apply flex flex-col items-start self-stretch max-w-80 space-y-none w-full gap-xs flex-grow;
  }

  .list-content {
    flex: 1 0 0;
    @apply overflow-ellipsis overflow-hidden
  }

  .list-item {
    @apply
    flex
    justify-between
    self-stretch
    items-center p-sm rounded-sm text-base gap-xs
    ;
  }
</style>