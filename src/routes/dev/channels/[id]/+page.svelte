<script lang="ts">
	import { page } from '$app/stores';
	import ChannelRedesign from '$lib/components/channel/ChannelRedesign.svelte';
</script>

<ChannelRedesign id={$page.params.id} />
