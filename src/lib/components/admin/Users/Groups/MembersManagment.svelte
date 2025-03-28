<!-- MembersManagement.svelte -->
<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { getContext } from 'svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import {Checkbox} from 'bits-ui';
	import { CircleCheckBig, Square, SquareCheckBig } from 'lucide-svelte';
	import Check from '$lib/components/common/Check/Check.svelte';


	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	// Recibir los miembros actuales del grupo y todos los miembros disponibles
	export let groupMembers = [];
	export let allMembers = [];
	export let group;

	// Crear un conjunto para determinar rápidamente cuáles están seleccionados
	let selectedMemberIds = new Set(groupMembers.map(member => member.id));

	onMount(() => {
		console.log('All members', allMembers);
		console.log('Group members', groupMembers);
		console.log('Selected members', selectedMemberIds);
	})
	// Función para actualizar los miembros seleccionados
	function toggleMember(memberId) {
		if (selectedMemberIds.has(memberId)) {
			selectedMemberIds.delete(memberId);
		} else {
			selectedMemberIds.add(memberId);
		}

		console.log(
			`Selected members: ${Array.from(selectedMemberIds).join(', ')}`
		);

		// Notificar cambios
		dispatch('update', {
			type: 'members',
			ids: Array.from(selectedMemberIds)
		});
	}
</script>

<div class="w-full">
	<h2 class="text-lg font-medium mb-3">{$i18n.t('Available Members')}</h2>

	{#if allMembers.length === 0}
		<p class="text-slate-500">{$i18n.t('Loading members...')}</p>
	{:else}
		<div class="space-y-2">
			{#each allMembers as member}
				<div class="">
					<Check id="member-{member.id}" label={member.name} avatar={member.name} on:change={() => toggleMember(member.id)} checked={selectedMemberIds.has(member.id)} />
				</div>
			{/each}
		</div>
	{/if}
</div>