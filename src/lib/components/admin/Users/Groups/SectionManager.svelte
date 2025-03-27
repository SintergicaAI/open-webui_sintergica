<!-- SectionManager.svelte -->
<script lang="ts">
	import { createEventDispatcher, getContext, onMount } from 'svelte';
	import { LibraryBig, Square, SquareCheckBig, Users } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import TuringFace from '$lib/components/icons/TuringFace.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let type: 'bases' | 'assistants' | 'members';
	export let title: string;
	export let items = [];
	export let buttonText: string;


	let selectedItems = new Set(items)

	$: selectedItems = new Set(items);

	const getIcon = () => {
		switch (type) {
			case 'bases': return LibraryBig;
			case 'assistants': return TuringFace;
			case 'members': return Users;
			default: return LibraryBig;
		}
	};

	const icon = getIcon();

	function handleAction() {
		dispatch('action');
	}

</script>

<section class="w-full max-w-screen-xl flex flex-col gap-sm">
	<header class="self-stretch flex justify-between items-center">
		<p class="text-label text-slate-400">{title}</p>
		<Button
			variant="outline-primary"
			icon={icon}
			iconSize="lg"
			onClick={handleAction}
		>
			{buttonText}
		</Button>
	</header>

	{#if type === 'members' && items.length > 0}
		<div class="self-stretch p-base rounded-md flex-col gap-sm bg-slate-200 dark:bg-slate-950 flex justify-center">
			{#each selectedItems as member}
				<article class="bg-slate-50 dark:bg-slate-800 border boder-slate-200 dark:border-slate-800 p-base rounded-sm flex items-center gap-sm">
					<Avatar name={member.name}/>
					{member.name}
				</article>
			{/each}
		</div>

	{:else if type === 'assistants' && items.length > 0}
		<div class="self-stretch p-base rounded-md flex-col gap-sm bg-slate-200 dark:bg-slate-950 flex justify-center">
			{#each selectedItems as assistant}
				<article class="bg-slate-50 dark:bg-slate-800 p-lg gap-lg border boder-slate-200 dark:border-slate-700 rounded-md flex flex-col">
					<header class="self-stretch flex items-start gap-sm">
						<TuringFace/>
						<p class="text-title text-black dark:text-white">{assistant.name}</p>
					</header>
					<p class="line-clamp-1 overflow-hidden text-ellipsis text-base text-slate-950 dark:text-slate-50">{assistant.description}</p>
				</article>
			{/each}
		</div>
	{:else if (type === 'bases' && items.length > 0)}
		<div class="self-stretch p-base rounded-md bg-slate-200 dark:bg-slate-950 flex ">
			{#each selectedItems as assistant}
				<Pill pillColor="purple" text={assistant.name}/>
			{/each}
		</div>
	{:else}
		<div class="self-stretch py-2xl rounded-md bg-slate-200 dark:bg-slate-950 flex justify-center">
			<p class="text-base text-slate-900 dark:text-slate-50">
				{$i18n.t('There are no associated {{association}}, click on',
					{association: $i18n.t(type === 'bases' ? 'knowledge bases' : type === 'assistants' ? 'assistants' : 'members')}
				)}
				<b class="text-brand-500">{buttonText}</b>
				{$i18n.t('to link them')}
			</p>
		</div>
	{/if}
</section>