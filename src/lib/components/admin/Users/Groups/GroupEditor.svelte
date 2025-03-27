<script lang="ts">

	import { getContext, onMount } from 'svelte';
	import ActionPanel from '$lib/components/admin/Users/Groups/ActionPanel.svelte';
	import SectionManager from '$lib/components/admin/Users/Groups/SectionManager.svelte';
	const i18n = getContext('i18n');


	export let edit: boolean = false;
	export let group: any = null;
	export let onSubmit: Function;

	let activePanel: 'bases' | 'assistants' | 'members' | null = null;

	function togglePanel(panel: 'bases' | 'assistants' | 'members') {
		activePanel = activePanel === panel ? null : panel;
	}

	function update(event: CustomEvent<{ type: string; ids: string[] }>) {
		const {type, ids} = event.detail;

		if (type === 'members') {
			// const updateHandler = async (_group) => {
			// 	const res = await updateGroupById(localStorage.token, group.id, _group).catch((error) => {
			// 		toast.error(error);
			// 		return null;
			// 	});
			//
			// 	if (res) {
			// 		toast.success($i18n.t('Group updated successfully'));
			// 		setGroups();
			// 	}
			// };
		}

		console.log(`Updating ${type.toUpperCase()} with IDs:`, ids);

		switch (type) {
			case 'bases': group.knowledgeBases = ids; break;
			case 'assistants': group.assistants = ids; break;
			case 'members': group.members = ids; break;
			default:
				break;
		}


	}
</script>

<div class=" flex gap-sm">
	<div class="flex-grow text-base text-slate-500 flex flex-col gap-lg py-2xl px-2xl items-start justify-start ">
		<header class=" w-full max-w-screen-xl flex flex-col gap-sm">
			<p class="text-label text-slate-400">{$i18n.t('Name')}</p>
			<h1 class="text-title text-black dark:text-white">{group?.name}</h1>
		</header>

		<SectionManager type="bases" title={$i18n.t('Knowledge bases')} items={ group?.knowledgeBases || []}
		buttonText={$i18n.t('Manage bases')} on:action={()=> togglePanel('bases')} />

		<SectionManager type="assistants" title={$i18n.t('Assistants')} items={group?.assistants || []}
										buttonText={$i18n.t('Manage assistants')} on:action={()=> togglePanel('assistants')}/>

		<SectionManager type="members" title={$i18n.t('Members')} items={group?.members || []}
										buttonText={$i18n.t('Manage members')} on:action={()=> togglePanel('members')}/>

		<section class=" w-full max-w-screen-xl flex flex-col gap-sm">
			<pre>{JSON.stringify(group, null, 2)}</pre>
		</section>
	</div>
	<!-- Panel lateral - visible solo cuando se activa un panel -->
	{#if activePanel}
		<ActionPanel panelType={activePanel} {group} on:close={() => togglePanel(activePanel)} on:udpate={update}/>
	{/if}

</div>



