<script lang="ts">

	import { getContext } from 'svelte';
	import ActionPanel from '$lib/components/admin/Users/Groups/ActionPanel.svelte';
	import SectionManager from '$lib/components/admin/Users/Groups/SectionManager.svelte';
	const i18n = getContext('i18n');

	import { models, } from '$lib/stores';


	export let edit: boolean = false;
	export let group: any = null;
	export let onSubmit: Function;

	let activePanel: 'bases' | 'assistants' | 'members' | null = null;

	function togglePanel(panel: 'bases' | 'assistants' | 'members') {
		activePanel = activePanel === panel ? null : panel;
	}
</script>

<div class=" flex">
	<div class="flex-grow text-base text-slate-500 flex flex-col gap-lg items-center justify-center ">
		<header class=" w-full max-w-screen-xl flex flex-col gap-sm">
			<p class="text-label text-slate-400">{$i18n.t('Name')}</p>
			<h1 class="text-title text-black dark:text-white">{group?.name}</h1>
		</header>

		<SectionManager type="bases" title={$i18n.t('Knowledge bases')} items={ $models || []}
		buttonText={$i18n.t('Manage bases')} on:action={()=> togglePanel('bases')}/>

		<SectionManager type="assistants" title={$i18n.t('Assistants')} items={[]}
										buttonText={$i18n.t('Manage assistants')} on:action={()=> togglePanel('assistants')}/>

		<SectionManager type="members" title={$i18n.t('Members')} items={[]}
										buttonText={$i18n.t('Manage members')} on:action={()=> togglePanel('members')}/>

		<section class=" w-full max-w-screen-xl flex flex-col gap-sm">
			<pre>{JSON.stringify(group, null, 2)}</pre>
		</section>
	</div>
	<!-- Panel lateral - visible solo cuando se activa un panel -->
	{#if activePanel}
		<ActionPanel panelType={activePanel} on:close={() => togglePanel(activePanel)}/>
	{/if}

</div>



