<script lang="ts">
	import NewFolder from '$lib/components/icons/NewFolder.svelte';

	export let content: string;
	export let handleClick: () => void;

	const CONTAINER_CLASSES = 'flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition';
	const FOLDER_ICON_CLASSES = 'size-4';
	const TEXT_CLASSES = 'self-center font-medium text-sm font-primary';

	function handleComponentClick() {
		handleClick();
	}
</script>

<div
	class={CONTAINER_CLASSES}
	on:click={handleComponentClick}
	draggable="false"
>
	<div class="self-center">
		<NewFolder class={FOLDER_ICON_CLASSES} strokeWidth="1" />
	</div>
	<div class="flex self-center">
		<div class={TEXT_CLASSES}>{content}</div>
	</div>
</div>