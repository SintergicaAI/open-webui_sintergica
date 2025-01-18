<script lang="ts">
	export let className = 'w-4 h-4';
	export let strokeWidth = '1.5';
</script>
<svg
	xmlns="http://www.w3.org/2000/svg"
	fill="none"
	viewBox="0 0 24 24"
	stroke-width={strokeWidth}
	stroke="currentColor"
	class={className}
>
	<rect x="3" y="3" width="18" height="14" rx="2" />
	<path d="M3 8h18" />
	<circle cx="6" cy="6" r="0.5" />
	<circle cx="9" cy="6" r="0.5" />
	<circle cx="12" cy="6" r="0.5" />
</svg>