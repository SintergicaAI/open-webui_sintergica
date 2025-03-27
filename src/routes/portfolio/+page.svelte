<script lang="ts">
	import List from '$lib/components/common/List/List.svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { ChevronDown, CircleCheck, CircleCheckBig, Search } from 'lucide-svelte';
	import Accordeon from '$lib/components/common/List/Accordeon.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import { Select } from "bits-ui";
	import { flyAndScale } from '$lib/utils/transitions';
	import { toast, Toaster } from 'svelte-sonner';
	import TextInput from '$lib/components/common/Input/TextInput.svelte';

	const themes = [
		{ value: "light-monochrome", label: "Light Monochrome" },
		{ value: "dark-green", label: "Dark Green" },
		{ value: "svelte-orange", label: "Svelte Orange" },
		{ value: "punk-pink", label: "Punk Pink" }
	];

	let description = '';
	let search = '';

	function handleOnToggled(event: CustomEvent) {
		console.log(event.detail);
	}
</script>


<div class="catalog overflow-y-auto">
	<h1>Catálogo de Componentes</h1>
	<div class="preview-section">
		<div class="preview-area">
			<div class="p-md shadow-base">
				Box
			</div>
			<TextInput id="password" type="password" placeholder="Texto" bind:value={description} on:toggled={handleOnToggled}/>
			<TextInput id="search" type="text" placeholder="Search" bind:value={search} on:toggled={handleOnToggled}>
				<Search size="20" slot="icon"/>
			</TextInput>

			<TextInput id="search" type="password" placeholder="Search" bind:value={search} on:toggled={handleOnToggled}></TextInput>
		</div>
	</div>
	<div class="preview-section">
		<div class="preview-area">
			<Select.Root items={themes}>
				<Select.Trigger
					class=" dark:text-white inline-flex h-input w-[296px] items-center rounded-sm border border-border-input bg-background px-base py-sm text-sm transition-colors placeholder:text-foreground-alt/50  focus:outline-none focus:ring-2 focus:ring-foreground focus:ring-offset-2 focus:ring-offset-background"
					aria-label="Select a theme"
				>
					<Select.Value class="text-sm dark:text-slate-500" placeholder="Select a theme" />
					<ChevronDown class="w-5 h-5 ml-auto dark:text-slate-500" />
				</Select.Trigger>
				<Select.Content
					class="bg-white dark:bg-slate-800 dark:text-white w-full rounded-xl border border-muted p-base shadow-popover outline-none"
					sideOffset={8}
					transition={flyAndScale}
				>
					{#each themes as theme}
						<Select.Item
							class="dark:hover:text-brand-500 flex h-10 w-full select-none items-center rounded-button p-base text-sm outline-none transition-all duration-75 data-[highlighted]:bg-muted"
							value={theme.value}
							label={theme.label}
						>
							<span class=" flex-1 text-base dark:text-white hover:text-brand-500 text-slate-950 line-clamp-1 overflow-hidden">{theme.label}</span>
							<Select.ItemIndicator class="ml-auto text-brand-500" asChild={false}>
								<CircleCheckBig size="20"/>
							</Select.ItemIndicator>
						</Select.Item>
					{/each}
				</Select.Content>
				<Select.Input name="favoriteFruit" />
			</Select.Root>
		</div>
	</div>
	<div class="preview-section">
		<div class="preview-area">
			<div class=" flex flex-col gap-sm ">
				<div class="flex flex-col justify-center items-center gap-sm">
					<Button variant="primary">Button</Button>
					<Button variant="primary" size="base" icon={Search}>Button</Button>
					<Button variant="primary" icon={Search} isDisabled={true}>Button</Button>
				</div>
				<div class="flex flex-col justify-center items-center gap-sm">
					<Button variant="outline-primary" >Outline</Button>
					<Button variant="outline-primary" isDisabled={true}>Outline</Button>

				</div>

				<div class="flex flex-col justify-center items-center gap-sm ">
					<Button variant="icon" icon={Search} color="danger"/>
					<Button variant="icon" color="danger" icon={Search} isDisabled="true"/>
				</div>

				<div class="flex flex-col justify-center items-center gap-sm ">
					<Button variant="danger" icon={Search}/>
				</div>

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

		<div class="preview-area">
			<Button onClick={() => toast.success('Success custom')}>Success toast</Button>
			<Button onClick={() => toast.warning('Warning custom')}>Warning toast</Button>
			<Button onClick={() => toast.error('Error custom')}>Error toast</Button>
			<Button onClick={() => toast('Success', {
	unstyled: true,
	classes: {
		toast: 'inline-flex max-w-[320px] gap-sm justify-center items-center p-sm bg-green-100 dark:bg-green-600 rounded-sm',
		title: 'text-base text-green-600 dark:text-green-100',
		description: 'text-red-400',
		actionButton: 'bg-zinc-400',
		cancelButton: 'bg-orange-400',
		closeButton: 'bg-lime-400'
	},
	icon: CircleCheck,
})}>Error</Button>
		</div>

		<article class="preview-area max-h-[100px] overflow-y-auto ">
			<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Repudiandae ab alias provident illo rerum incidunt, dolorum quam, corporis quos, deleniti unde. Officiis magni quia laudantium quod, voluptatum sint minus deleniti!</p>
			<p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Recusandae asperiores rerum officia sunt vero tenetur cupiditate eligendi neque animi quae. Suscipit voluptates eum placeat error excepturi veniam ipsa rerum consectetur!</p>

		</article>
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