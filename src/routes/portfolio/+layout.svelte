<script>
	import '../../tailwind.css';
	import '../../app.css';
	import 'tippy.js/dist/tippy.css';

	export let title = 'Catálogo de Componentes';
</script>
<div class="layout">
	<header>{title}</header>

	<main class="content overflow-y-auto">
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

    @media (prefers-color-scheme: dark) {
        .layout {
            background: #121212;
            color: #e0e0e0;
        }

        header {
            background: #1e88e5;
            color: white;
        }

        .content {
            color: #e0e0e0;
        }
    }
</style>