<script lang="ts">
	export let text: string;
	export let pillColor: string = 'red';
	const COLORS = ['red', 'blue', 'green', 'yellow', 'purple'];

	$: safeColor = COLORS.includes(pillColor) ? pillColor : 'red';
</script>
<p class={`pill ${safeColor} text-subtitles`} role="status" aria-live="polite">
  {text}
</p>

<style>
    .pill {
        @apply flex flex-nowrap items-center justify-center gap-[10px] rounded-md py-sm px-base border;
      white-space: nowrap;
      text-overflow: ellipsis;
      max-width: 100%;

    }

    .red {
      @apply text-red-600 bg-red-200 border-red-600;
    }

    .blue {
      @apply text-blue-600 bg-blue-200 border-blue-600;
    }

    .green {
      @apply text-green-600 bg-green-200 border-green-600;
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
</style>