<script lang="ts">
	import InputChat from '$lib/components/chat/InputChat.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import Search from '$lib/components/icons/Search.svelte';
	import {Button as BitsUIButton} from 'bits-ui'

	const slides = [
		'/assets/images/galaxy.jpg',
		'/assets/images/space_horizontal_2.jpg',
		'/assets/images/earth.jpg',
		'/assets/images/adam.jpg'
	];
</script>

<main class="p-xl space-y-8 bg-gray-100 min-h-screen">
	<div class="card p-6 border-[1px] border-gray-300 shadow rounded bg-white">
		<h1 class="font-archivo text-3xl text-brand-500 mb-4">Chat</h1>
		<div class="p-4 border-[1px] border-dashed border-gray-300 rounded bg-gray-50">
			<InputChat />
		</div>
	</div>

	<div class="card p-6 border-[1px] border-gray-300 shadow rounded bg-white">
		<h2 class="font-archivo text-2xl text-brand-600 mb-4">Buttons</h2>
		<div class="flex flex-wrap gap-4">
			<Button variant="danger-outlined" isDisabled={false}>Testing</Button>
			<Button variant="danger-outlined" isDisabled={true} icon={Search}>Testing</Button>
			<Button variant="primary" isDisabled={false}>Primary</Button>
			<Button variant="primary-outlined" isDisabled={false} icon={Search}>Primary</Button>
		</div>
	</div>

	<div class="card p-6 border-[1px] border-gray-300 shadow rounded bg-white">
		<h2 class="font-archivo text-2xl text-brand-600 mb-4">Bits UI Button</h2>
		<div class="flex justify-center items-center p-4 border-[1px] border-dashed border-gray-300 rounded bg-gray-50">
			<BitsUIButton.Root class="inline-flex h-12 items-center justify-center rounded-xl bg-brand-500
		px-[21px] text-[15px] font-semibold text-background shadow-mini
		hover:bg-dark/95 active:scale-98 active:transition-all">
				Aceptar
			</BitsUIButton.Root>
		</div>
	</div>
</main>

<style>
    main {
        font-family: sans-serif;
    }

    .card {
        max-width: 800px;
        margin: 0 auto;
    }
</style>