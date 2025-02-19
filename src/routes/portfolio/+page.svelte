<script lang="ts">
	import List from '$lib/components/common/List/List.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Search } from 'lucide-svelte';
	import Accordeon from '$lib/components/common/List/Accordeon.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
</script>

<div class="catalog">
	<h1>Catálogo de Componentes</h1>
	<div class="preview-section">
		<div class="preview-area">
			<div>
			<Button variant="primary">Button</Button>
			<Button variant="primary" icon={Search}>Button</Button>
			<Button variant="primary" icon={Search} isDisabled={true}>Button</Button>
			<Button variant="icon" icon={Search} />
			<Button variant="outline-primary" >Outline</Button>
			<Button variant="outline-primary" isDisabled={true}>Outline</Button>
			</div>
			<div>
				<Button variant="danger" icon={Search}>Button</Button>
			</div>
		</div>
	</div>
	<div class="preview-section">
		<div class="preview-area">
			<List items={['Item 1', 'Item 2', 'Item 3']} />
		</div>

		<div class="preview-area">
			<Accordeon title="Title" icon={Search}>
				<List items={['Item 1', 'Item 2', 'Item 3']} />
			</Accordeon>
		</div>

		<div class="preview-area">
			<p>
				Default
				<Avatar type="button" initials="AB" size="sm"/>
			</p>
			<p>
				User
				<Avatar type="user" initials="AB" size="base"/>
			</p>

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
        color: #333;
        min-height: 100vh;
        box-sizing: border-box;
    }

    .catalog h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .preview-section {
        display: flex;
        gap: 3rem;
        justify-content: space-around;
        align-items: flex-start;
        width: 100%;
        margin-bottom: 2rem;
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
        gap: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: border-color 0.3s, background-color 0.3s, color 0.3s;
    }

    .preview-area:hover {
        border-color: #999;
    }

    @media (prefers-color-scheme: dark) {
        .catalog {
            background-color: #121212;
            color: #e0e0e0;
        }

        .preview-area {
            background-color: #1e1e1e;
            border-color: #555;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
						display: flex;
						flex-wrap: wrap;
        }



        .preview-area:hover {
            border-color: #888;
        }
    }
</style>