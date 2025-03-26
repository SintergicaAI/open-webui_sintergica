<!-- ActionPanel.svelte -->
<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import { X } from 'lucide-svelte';
	import BasesManagment from '$lib/components/admin/Users/Groups/BasesManagment.svelte';
	import AssistantsManagment from '$lib/components/admin/Users/Groups/AssistantsManagment.svelte';
	import MembersManagment from '$lib/components/admin/Users/Groups/MembersManagment.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let panelType: 'bases' | 'assistants' | 'members';

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
</script>

<aside class="sidebar flex flex-shrink-0 flex-col flex-1 p-lg gap-lg">
	<header class="self-stretch flex justify-between items-center">
		<h1 class="text-subtitle">{getPanelTitle()}</h1>
		<button class="cursor-pointer" on:click={closePanel}>
			<X />
		</button>
	</header>

	<div class="self-stretch flex flex-col items-start justify-center gap-sm">
		<p class="text-label text-slate-500">{$i18n.t(`Manage ${getPanelTitle()}`)}</p>

		<!-- Contenido específico según el tipo de panel -->
		{#if panelType === 'bases'}
			<BasesManagment />
		{:else if panelType === 'assistants'}
			<AssistantsManagment />
		{:else if panelType === 'members'}
			<MembersManagment />
		{/if}
	</div>
</aside>