<script lang="ts">
	// Props
	export let isChecked = false; // Estado del botón
	export let text = 'Botón'; // Texto del botón
	export let color = 'muted';

	// Constants
	const DEFAULT_CLASS = 'bg-gray-500/20 text-gray-700 dark:text-gray-200';

	const classNames: Record<string, { base: string; active: string }> = {
		info: {
			base: 'bg-blue-500/20 text-blue-700 dark:text-blue-200',
			active: 'bg-blue-500 text-white border-blue-500 dark:bg-blue-600 dark:border-blue-600 dark:text-white'
		},
		success: {
			base: 'bg-green-500/20 text-green-700 dark:text-green-200',
			active: 'bg-green-500 text-white border-green-500 dark:bg-green-600 dark:border-green-600 dark:text-white'
		},
		warning: {
			base: 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-200',
			active: 'bg-yellow-500 text-white border-yellow-500 dark:bg-yellow-600 dark:border-yellow-600 dark:text-white'
		},
		error: {
			base: 'bg-red-500/20 text-red-700 dark:text-red-200',
			active: 'bg-red-500 text-white border-red-500 dark:bg-red-600 dark:border-red-600 dark:text-white'
		},
		muted: {
			base: DEFAULT_CLASS,
			active: 'bg-gray-700 text-white border-gray-700 dark:bg-gray-600 dark:text-white'
		},
		yellow: {
			base: 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-200',
			active: 'bg-yellow-500 text-white border-yellow-500 dark:bg-yellow-600 dark:border-yellow-600 dark:text-white'
		},
		blue: {
			base: 'bg-blue-500/20 text-blue-700 dark:text-blue-200',
			active: 'bg-blue-500 text-white border-blue-500 dark:bg-blue-600 dark:border-blue-600 dark:text-white'
		},
		pink: {
			base: 'bg-pink-500/20 text-pink-700 dark:text-pink-200',
			active: 'bg-pink-500 text-white border-pink-500 dark:bg-pink-600 dark:border-pink-600 dark:text-white'
		},
		green: {
			base: 'bg-green-500/20 text-green-700 dark:text-green-200',
			active: 'bg-green-500 text-white border-green-500 dark:bg-green-600 dark:border-green-600 dark:text-white'
		},
		purple: {
			base: 'bg-purple-500/20 text-purple-700 dark:text-purple-200',
			active: 'bg-purple-500 text-white border-purple-500 dark:bg-purple-600 dark:border-purple-600 dark:text-white'
		},
		orange: {
			base: 'bg-orange-500/20 text-orange-700 dark:text-orange-200',
			active: 'bg-orange-500 text-white border-orange-500 dark:bg-orange-600 dark:border-orange-600 dark:text-white'
		},
		red: {
			base: 'bg-red-500/20 text-red-700 dark:text-red-200',
			active: 'bg-red-500 text-white border-red-500 dark:bg-red-600 dark:border-red-600 dark:text-white'
		},
		gray: {
			base: DEFAULT_CLASS,
			active: 'bg-gray-700 text-white border-gray-700 dark:bg-gray-600 dark:text-white'
		},
		indigo: {
			base: 'bg-indigo-500/20 text-indigo-700 dark:text-indigo-200',
			active: 'bg-indigo-500 text-white border-indigo-500 dark:bg-indigo-600 dark:border-indigo-600 dark:text-white'
		},
		teal: {
			base: 'bg-teal-500/20 text-teal-700 dark:text-teal-200',
			active: 'bg-teal-500 text-white border-teal-500 dark:bg-teal-600 dark:border-teal-600 dark:text-white'
		}
	};
	

	function toggleChecked() {
		isChecked = !isChecked;
	}

	function getClassName(): string {
		if (isChecked) {
			return classNames[color]?.active ?? classNames.muted.active;
		}
		return classNames[color]?.base ?? classNames.muted.base;
	}
</script>

<button
	on:click={toggleChecked}
	class="rounded font-semibold uppercase text-sm px-2 flex-shrink-0 flex items-center space-x-1 transition-all select-none {getClassName()} {isChecked ? 'bg-blue-500 text-white border-blue-500' : ''}"
	aria-pressed={isChecked}
>
	<slot name="icon" />
	<span>{text}</span>
</button>