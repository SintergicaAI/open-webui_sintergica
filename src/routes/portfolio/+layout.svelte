<script>
	import '../../tailwind.css';
	import '../../app.css';
	import 'tippy.js/dist/tippy.css';
	export let title = 'Catálogo de Componentes';
</script>
<div class="layout">
	<header>{title}</header>

	<main class="content">
		<slot />
	</main>
</div>
<style>
    .layout {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 1fr;
        height: 100vh;
    }

    header {
        grid-column: 1 / -1;
        background: #4a90e2;
        color: white;
        padding: 1rem;
        font-size: 1.25rem;
        font-weight: bold;
    }

    .content {
        padding: 1rem;
    }
</style>