<script>
import UsersRedesign from '$lib/components/admin/UsersRedesign.svelte';
import { onMount } from 'svelte';
import { activeHeader } from '$lib/stores';

onMount(() => {
	activeHeader.set('members');
})
</script>
<UsersRedesign />
