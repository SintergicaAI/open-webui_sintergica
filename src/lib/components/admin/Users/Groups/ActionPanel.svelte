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

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	type Group = {
		id: string;
		name: string;
		knowledgeBases: string[];
		assistants: string[];
		members: string[];
	}

	export let panelType: 'bases' | 'assistants' | 'members';
	export let group: Group;

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
		dispatch('update', {type:event.type, ids:event.ids});

	}
</script>

<aside class="border-l border-slate-700 dark:bg-slate-950 flex flex-shrink-0 flex-col flex-1 p-lg gap-lg">
	<header class="self-stretch flex justify-between items-center">
		<h1 class="text-subtitle text-black dark:text-white">{getPanelTitle()}</h1>
		<button class="cursor-pointer" on:click={closePanel}>
			<X />
		</button>
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