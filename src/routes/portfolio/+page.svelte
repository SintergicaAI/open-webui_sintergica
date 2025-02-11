<script lang="ts">
	import List from '$lib/components/common/List/List.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Search } from 'lucide-svelte';
	import Accordeon from '$lib/components/common/List/Accordeon.svelte';

</script>

<div class="catalog">
	<h1>Catálogo de Componentes</h1>
	<div class="preview-section">
		<div class="preview-area">
			<Button variant="primary" icon={Search}>Button</Button>
		</div>
	</div>
	<div class="preview-section">
		<div class="preview-area">
			<List items={['Item 1', 'Item 2', 'Item 3']}/>
		</div>

		<div class="preview-area">
			<Accordeon>
				<List items={['Item 1', 'Item 2', 'Item 3']}/>
			</Accordeon>
		</div>
	</div>
</div>

<style>
    .catalog {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 2rem;
        background-color: #f4f4f9;
        min-height: 100vh;
        box-sizing: border-box;
    }

    .catalog h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #333;
    }

    .preview-section {
        display: flex;
        gap: 2rem;
				justify-content: center;
        align-items: center;
				width: 100%;
    }

    .preview-area {
        width: 100%;
        max-width: 500px;
        border: 2px dashed #ccc;
        padding: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
        border-radius: 0.5rem;
        min-height: 300px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: border-color 0.3s;
    }

    .preview-area:hover {
        border-color: #999;
    }
</style>