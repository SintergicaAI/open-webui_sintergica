<script lang="ts">
	import { AudioLines, Globe, Icon as IconType, Paperclip } from 'lucide-svelte';
	import Mic from '$lib/components/icons/Mic.svelte';
	import { Button } from 'bits-ui';

	type Icons = {
		icon: IconType
	}


</script>

<div class="input-chat rounded-xl space-y-xs">
	<div class="flex-grow">
		<input class="text-gray-400 w-full outline-transparent" type="text" value="Hola" />
	</div>
	<div class="flex-grow flex justify-between w-full">
		<div class="input-chat__actions space-x-xs">
			<Paperclip className="paddings-xs" size="20"/>
			<div class="flex bg-slate-100 rounded-sm paddings-xs">
				<Globe size="20"/>
				<span class="bg-slate-100">Inactivo</span>
			</div>

		</div>
		<div class="input-chat__actions">
			<Mic />
			<AudioLines size="20" class="color-slate-500"/>
		</div>

	</div>
</div>

<style lang="postcss">
		:root {
				--rounder-sm: 8px;
				--rounder-base: 12px;
				--rounder-lg: 16px;

				--space-none: 0.0rem;
				--space-xs: 0.25rem;
				--space-sm: 0.5rem;
				--space-base: 0.75rem;
				--space-lg: 1rem;
				--space-xl: 1.25rem;
				--space-2xl: 1.5rem;
				--space-3xl: 2rem;
				--space-4xl: 2.5rem;
				--space-5xl: 4rem;
				--space-6xl: 8rem;

				--font-archivo: 'Archivo', sans-serif;
		}

		.text-title {
				font-family: var(--font-archivo);
				font-weight: bold;
				font-size: 20pt;
		}

		.text-subtitle {
				font-family: var(--font-archivo);
				font-weight: 600;
				font-size: 16pt;
		}

		.text-base {
				font-family: var(--font-archivo);
				font-weight: 400;
				font-size: 16pt;
		}

		.text-avatar {
				font-family: var(--font-archivo);
				font-size: 12pt;
				text-transform: uppercase;
				font-weight: 600;
		}

    .input-chat {
        display: flex;
        align-items: center;
        flex-flow: row wrap;
        padding: 0.5rem;
        border: 1px solid #e2e8f0;
				max-width: 692px;
        background-color: #fff;
    }
		.input-chat__actions {
				display: flex;
				align-items: center;
				gap: 0.5rem;

		}
</style>