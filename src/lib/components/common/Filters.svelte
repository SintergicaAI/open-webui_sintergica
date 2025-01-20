<script lang="ts">
	import { Icon } from 'svelte-sonner';
	import { getContext, tick } from 'svelte';
	import Filter from '$lib/components/common/Filter.svelte';
	import Markdown from '$lib/components/icons/Markdown.svelte';
	import DocumentDuplicate from '$lib/components/icons/DocumentDuplicate.svelte';
	import Bookmark from '$lib/components/icons/Bookmark.svelte';
	const i18n = getContext('i18n');

	let show = false;
	let searchData = []
	let visibleTabs = searchData.map((tab) => tab.id);
	let selectedTab = 'general';

	const scrollHandler = (event) => {
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			event.preventDefault(); // Prevent default vertical scrolling
			settingsTabsContainer.scrollLeft += event.deltaY; // Scroll sideways
		}
	};

	const addScrollListener = async () => {
		await tick();
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			settingsTabsContainer.addEventListener('wheel', scrollHandler);
		}
	};

	const removeScrollListener = async () => {
		await tick();
		const settingsTabsContainer = document.getElementById('settings-tabs-container');
		if (settingsTabsContainer) {
			settingsTabsContainer.removeEventListener('wheel', scrollHandler);
		}
	};

	$: if (show) {
		addScrollListener();
	} else {
		removeScrollListener();
	}
</script>

<div class="flex flex-col md:flex-row w-full px-4 pt-1 pb-4 md:space-x-4">
	<div
		class="tabs flex flex-row overflow-x-auto gap-2.5 md:gap-1 flex-1 md:w-40 dark:text-gray-200 text-sm font-medium text-left mb-1 md:mb-0 -translate-y-1"
	>
			<Filter text="All" color="gray">
				<Icon slot="icon" />
			</Filter>
			<Filter text="documents" color="blue">
				<DocumentDuplicate slot="icon" />
			</Filter>
			<Filter text="tablas" color="teal">
				<Bookmark slot="icon" />
			</Filter>
			<Filter text="website" color="pink">
				<Markdown slot="icon" />
			</Filter>
			<Filter text="rich text" color="blue">
				<Markdown slot="icon" />
			</Filter>

	</div>
</div>

<style>
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        /* display: none; <- Crashes Chrome on hover */
        -webkit-appearance: none;
        margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
    }

    .tabs::-webkit-scrollbar {
        display: none; /* for Chrome, Safari and Opera */
    }

    .tabs {
        -ms-overflow-style: none; /* IE and Edge */
        scrollbar-width: none; /* Firefox */
    }

    input[type='number'] {
        -moz-appearance: textfield; /* Firefox */
    }
</style>