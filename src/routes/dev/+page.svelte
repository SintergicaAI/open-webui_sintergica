<script lang="ts">
	import InputChat from '$lib/components/chat/InputChat.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';

	const slides = [
		'/assets/images/galaxy.jpg',
		'/assets/images/space_horizontal_2.jpg',
		'/assets/images/earth.jpg',
		'/assets/images/adam.jpg',
	];
</script>

<main class="p-xl">
<!--	<div class="w-[500px] h-[500px]">-->
<!--&lt;!&ndash;		<Carousel {slides} autoplay={true} interval={5000} showDots={true} showArrows={true}/>&ndash;&gt;-->
<!--	</div>-->
	<div class="card">
		<h1 class="font-archivo text-3xl text-brand-500 ">Chat</h1>
		<InputChat />
	</div>
	<div class="card">
		<Button variant="danger-outline" isDisabled={false}>Testing</Button>
	</div>
</main>

<style>
</style>