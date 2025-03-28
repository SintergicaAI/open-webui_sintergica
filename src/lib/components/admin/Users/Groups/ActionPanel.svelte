<!-- ActionPanel.svelte -->
<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import { X } from 'lucide-svelte';
	import BasesManagment from '$lib/components/admin/Users/Groups/BasesManagment.svelte';
	import AssistantsManagment from '$lib/components/admin/Users/Groups/AssistantsManagment.svelte';
	import MembersManagment from '$lib/components/admin/Users/Groups/MembersManagment.svelte';
	import { knowledge, models, members } from '$lib/stores';
	import { updateGroupById } from '$lib/apis/groups';
	import { toast } from 'svelte-sonner';
	import Button from '$lib/components/common/Button/Button.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let panelType: 'bases' | 'assistants' | 'members';
	export let group: Group;
	export let onSubmit: (group) => void;
	// Obtener el título basado en el tipo de panel
	const getPanelTitle = () => {
		switch (panelType) {
			case 'bases': return $i18n.t('Knowledge Bases');
			case 'assistants': return $i18n.t('Assistants');
			case 'members': return $i18n.t('Members');
			default: return '';
		}
	};

	// Cerrar el panel
	function closePanel() {
		dispatch('close');
	}




	function update(event: CustomEvent<{ type: string; ids: string[] }>) {
		const {type, ids} = event.detail;

		console.log(`Updating ${type.toUpperCase()} with IDs:`, ids);

		let updatedGroup = { ...group };

		if (type === 'bases') {
			updatedGroup.knowledgeBases = ids.map(id => {
				return $knowledge?.find(base => base.id === id);
			});
		} else if (type === 'assistants') {
			updatedGroup.assistants = ids.map(id => {
				return $models?.find(model => model.id === id);
			});
		} else if (type === 'members') {
			updatedGroup.user_ids = ids;
			updatedGroup.members = ids.map(id => {
				return $members?.find(member => member.id === id);
			});
		}

		console.log(`Updated group:`, updatedGroup);

		onSubmit(updatedGroup);

		toast.success(`${type.toUpperCase()} updated successfully`);
	}
</script>

<aside class="border-l border-slate-300 dark:border-slate-700 dark:bg-slate-950 flex flex-shrink-0 basis-1/3 flex-col flex-1 p-lg gap-lg">
	<header class="self-stretch flex justify-between items-center">
		<h1 class="text-subtitle text-black dark:text-white">{getPanelTitle()}</h1>
		<Button buttonClasses="text-slate-500" variant="icon" icon={X} onClick={closePanel}/>
	</header>

	<div class="self-stretch flex flex-col items-start justify-center gap-sm">
		<p class="text-label text-slate-500">{$i18n.t(`Manage ${getPanelTitle()}`)}</p>
		<!-- Contenido específico según el tipo de panel -->
		{#if panelType === 'bases'}
			<BasesManagment groupBases={group?.knowledgeBases || []} allBases={$knowledge} {group} on:update={update}/>
		{:else if panelType === 'assistants'}
			<AssistantsManagment groupAssistants={group?.assistants || []} allAssistants={$models} {group} on:update={update}/>
		{:else if panelType === 'members'}
			<MembersManagment groupMembers={group?.members || []} allMembers={$members} {group} on:update={update}/>
		{/if}
	</div>
</aside>