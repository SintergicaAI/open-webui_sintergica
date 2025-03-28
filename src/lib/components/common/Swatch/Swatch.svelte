<script lang="ts">

	export let color = 'red';
	export let isSelected = false;

	const COLORS = ['red', 'orange', 'yellow', 'lime', 'green', 'sky', 'blue', 'purple', 'pink', 'brand'];


	$: containerClass = `inline-flex p-xs rounded-sm hover:bg-brand-100 cursor-pointer ${
		isSelected ? 'bg-brand-200' : ''
	}`;

	$: circleClass = `w-6 h-6 rounded-full border-2 ${safeColor}`;

	$: safeColor = COLORS.includes(color) ? color : 'red';
</script>
<div class={`${containerClass}`}>
	<div class={circleClass}></div>
</div>

<style>
    .red {
        @apply text-red-600 bg-red-200 border-red-600;
    }

    .blue {
        @apply text-blue-600 bg-blue-200 border-blue-600;
    }

    .green {
        @apply text-green-600 bg-green-200 border-green-600;
    }

		.lime {
				@apply text-lime-600 bg-lime-200 border-lime-600;
		}

		.sky {
				@apply text-sky-600 bg-sky-200 border-sky-600;
		}

    .yellow {
        @apply text-yellow-600 bg-yellow-200 border-yellow-600;
    }

    .purple {
        @apply text-purple-600 bg-purple-200 border-purple-600;
    }

    .orange {
        @apply text-orange-600 bg-orange-200 border-orange-600;
    }

    .pink {
        @apply text-pink-600 bg-pink-200 border-pink-600;
    }

    .teal {
        @apply text-teal-600 bg-teal-200 border-teal-600;
    }

    .indigo {
        @apply text-indigo-600 bg-indigo-200 border-indigo-600;
    }

    .gray {
        @apply text-gray-600 bg-gray-200 border-gray-600;
    }

    .slate {
        @apply text-slate-600 bg-slate-200 border-slate-600;
    }

    .brand {
        @apply text-brand-200 bg-brand-900 border-brand-200;
    }
</style>