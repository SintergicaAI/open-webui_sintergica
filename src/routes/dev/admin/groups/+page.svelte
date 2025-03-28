<script>
	import GroupsRedesign from '$lib/components/admin/Users/GroupsRedesign.svelte';
	import { onMount } from 'svelte';
	import { activeHeader } from '$lib/stores';

	onMount(() => {
		activeHeader.set('groups');
	})
</script>

<GroupsRedesign />