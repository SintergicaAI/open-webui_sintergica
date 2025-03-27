<script lang="ts">
	import { onMount, getContext, createEventDispatcher } from 'svelte';
	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	import { fade } from 'svelte/transition';
	import { flyAndScale } from '$lib/utils/transitions';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Trash2, X } from 'lucide-svelte';

	export let title = '';
	export let message = '';

	export let cancelLabel = $i18n.t('Cancel');
	export let confirmLabel = $i18n.t('Confirm');

	export let onConfirm = () => {};

	export let input = false;
	export let inputPlaceholder = '';
	export let inputValue = '';

	export let show = false;

	let modalElement = null;
	let mounted = false;

	const handleKeyDown = (event: KeyboardEvent) => {
		if (event.key === 'Escape') {
			console.log('Escape');
			show = false;
		}

		if (event.key === 'Enter') {
			console.log('Enter');
			confirmHandler();
		}
	};

	const confirmHandler = async () => {
		show = false;
		await onConfirm();
		dispatch('confirm', inputValue);
	};

	onMount(() => {
		mounted = true;
	});

	$: if (mounted) {
		if (show && modalElement) {
			document.body.appendChild(modalElement);

			window.addEventListener('keydown', handleKeyDown);
			document.body.style.overflow = 'hidden';
		} else if (modalElement) {
			window.removeEventListener('keydown', handleKeyDown);
			document.body.removeChild(modalElement);

			document.body.style.overflow = 'unset';
		}
	}
</script>

{#if show}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		bind:this={modalElement}
		class=" fixed top-0 right-0 left-0 bottom-0 bg-[rgba(100,116,139,0.50)] dark:bg-[rgba(17,30,45,0.90)]	 backdrop-blur-[2px] w-full h-screen max-h-[100dvh] flex justify-center z-[99999999] overflow-hidden overscroll-contain"
		in:fade={{ duration: 10 }}
		on:mousedown={() => {
			show = false;
		}}
	>
		<div
			class=" m-auto rounded-xl max-w-full w-[32rem] mx-2 bg-slate-100 dark:bg-slate-950 max-h-[100dvh] shadow-3xl"
			in:flyAndScale
			on:mousedown={(e) => {
				e.stopPropagation();
			}}
		>
			<header class="p-lg flex justify-between items-center border-b border-slate-300 dark:border-slate-700">
				<h2 class="text-subtitle text-black dark:text-white">
					{#if title !== ''}
						{title}
					{:else}
						{$i18n.t('Confirm your action')}
					{/if}
				</h2>
				<Button variant="icon" icon={X} buttonClasses="text-slate-500" />
			</header>
			<div class="self-stretch px-2xl py-lg flex flex-col justify-center content-center items-center gap-y-2xl ">
				<slot>
				</slot>
				<div class=" text-base text-center text-slate-400 flex-1">
					{#if message !== ''}
						{message}
					{:else}
						{$i18n.t('This action cannot be undone. Do you wish to continue?')}
					{/if}

					{#if input}
							<textarea
								bind:value={inputValue}
								placeholder={inputPlaceholder ? inputPlaceholder : $i18n.t('Enter your message')}
								class="w-full mt-2 rounded-lg px-4 py-2 text-sm dark:text-gray-300 dark:bg-gray-900 outline-none resize-none"
								rows="3"
								required
							/>
					{/if}
				</div>

				<div class="mt-6 flex justify-between gap-sm">
					<Button variant="outline-primary" buttonClasses="w-full" icon={X} onClick={()=>{show = false; dispatch('cancel');}}>
						{cancelLabel}
					</Button>
					<Button variant="danger" buttonClasses="w-full" icon={Trash2} onClick={()=>{confirmHandler()}}>
						{confirmLabel}
					</Button>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-content {
		animation: scaleUp 0.1s ease-out forwards;
	}

	@keyframes scaleUp {
		from {
			transform: scale(0.985);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
