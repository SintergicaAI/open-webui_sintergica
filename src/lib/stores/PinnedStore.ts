import { writable } from "svelte/store";

export function createPinnedStore(items: string[]) {
	const { subscribe, update } = writable(items.map(() => false));

	function togglePinned(index: number) {
		update((pinned) => {
			console.log(
				`Pinned: ${pinned[index] ? 'Despin' : 'Pin'} ${items[index]}`
			);
			pinned[index] = !pinned[index];
			return [...pinned];
		});
	}

	return { subscribe, togglePinned };
}