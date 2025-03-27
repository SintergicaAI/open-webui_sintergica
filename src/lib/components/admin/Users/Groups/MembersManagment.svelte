<!-- MembersManagement.svelte -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { getContext } from 'svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	// Recibir los miembros actuales del grupo y todos los miembros disponibles
	export let groupMembers = [];
	export let allMembers = [];
	export let group;

	// Crear un conjunto para determinar rápidamente cuáles están seleccionados
	let selectedMemberIds = new Set(groupMembers.map(member => member.id));

	// Función para actualizar los miembros seleccionados
	function toggleMember(memberId) {
		if (selectedMemberIds.has(memberId)) {
			selectedMemberIds.delete(memberId);
		} else {
			selectedMemberIds.add(memberId);
		}

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
				<div class="flex items-center p-2 border rounded">
					<input
						type="checkbox"
						id="member-{member.id}"
						checked={selectedMemberIds.has(member.id)}
						on:change={() => toggleMember(member.id)}
						class="mr-2"
					/>
					<label for="member-{member.id}" class="flex items-center gap-2">
						<Avatar name={member.name} />
						<span>{member.name}</span>
					</label>
				</div>
			{/each}
		</div>
	{/if}
</div>