<script lang="ts">
	import { Pin, Ellipsis, EllipsisVertical, ChevronDown, ChevronUp } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';

	export let items: string[] = [];
</script>

<div class="list-container">
	{#if items.length > 0}
		{#each items as item, index}
			<div class="list-item">
				<span class="list-content text-base">
					{index + 1}. {item}
				</span>
				<div>
					<Button variant="icon" size="sm" icon={Pin}/>
					<Button variant="icon" size="sm" icon={Ellipsis}/>
				</div>
			</div>
		{/each}
	{:else}
		<p>No hay elementos en la lista.</p>
	{/if}
</div>

<style lang="scss">
    .list-container {
				@apply flex flex-col items-start self-stretch space-y-none w-full max-w-sm gap-xs flex-grow border-2 border-gray-200;
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