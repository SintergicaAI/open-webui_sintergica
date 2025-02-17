<script lang="ts">
	import { page } from '$app/stores';

	import Help from '$lib/components/layout/Help.svelte';
	import ChatRedesign from '$lib/components/chat/ChatRedesign.svelte';
</script>

<Help />
<ChatRedesign chatIdProp={$page.params.id} />
