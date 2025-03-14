<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	import FileItem from '$lib/components/common/FileItem.svelte';

	export let selectedFileId = null;
	export let files = [];

	export let small = false; //If is small will render the Avatar file icon
</script>

<div class=" max-h-full flex flex-col gap-sm w-full">
	{#each files as file}
		<div class="mt-1 px-2">
			<FileItem
				className="w-full"
				colorClassName="border {selectedFileId === file.id
					? 'bg-brand-50 border-brand-200 dark:border-brand-700 dark:bg-brand-800'
					: ' bg-slate-50 border-slate-200 dark:border-slate-800 dark:bg-slate-800'} hover:bg-white hover:border-slate-200 dark:hover:bg-slate-900 transition"
				{small}
				{file}
				name={file?.name ?? file?.meta?.name}
				type="file"
				size={file?.size ?? file?.meta?.size ?? ''}
				media={file?.meta['content_type']}
				loading={file.status === 'uploading'}
				author={file?.user_name }
				dismissible
				on:click={() => {
					if (file.status === 'uploading') {
						return;
					}

					dispatch('click', file.id);
				}}
				on:dismiss={() => {
					if (file.status === 'uploading') {
						return;
					}

					dispatch('delete', file.id);
				}}
			/>
		</div>
	{/each}
</div>
