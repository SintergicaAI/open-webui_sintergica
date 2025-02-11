<script lang="ts">
	import { AudioLines, Globe, Mic, Paperclip } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import Switch from '$lib/components/chat/Switch.svelte';

	const inputPlaceholder = 'Escriba aquí';

	function toggleSwitchActive(event: Event) {
		const target = event.currentTarget as HTMLElement;
		target.classList.toggle('active');
	}
</script>

<!-- Componente -->
<div class="input-chat">
	<div class="flex-grow flex justify-between align-center self-stretch">
		<input
			class="flex flex-grow text-slate-400 outline-transparent p-base"
			type="text"
			placeholder={inputPlaceholder}
		/>
	</div>

	<div class="flex-grow flex justify-between w-full">
		<div class="input-chat__actions">
			<Button variant="icon" size="sm" icon={Paperclip} iconSize="base"/>
			<Switch
				icon={Globe}
				activeLabel="on"
				inactiveLabel="off"
				initialActive={true}
				onToggle={toggleSwitchActive}
				isDisabled={false}

			/>
		</div>
		<div class="input-chat__actions">
			<Button variant="icon" size="sm" icon={Mic} iconSize="base"/>
			<Button variant="primary" size="sm" icon={AudioLines} iconSize="base"/>
		</div>
	</div>
</div>

<style lang="scss">
  // Variables para estilos reutilizables
  $padding-sm: 8px;
  $padding-xs: 4px;
  $gap-sm: 8px;

  .input-chat {
    display: flex;
    flex-direction: column;
		align-items: center;
		gap:4px;
		width: 640px;
    max-width: 692px;
    background-color: #fff;

    @apply p-base rounded-sm space-y-xs shadow-sm;
  }

  .input-chat__actions {
    display: flex;
    align-items: center;

    @apply gap-x-sm;
  }

  .switch {
    @apply py-xs px-xs rounded-sm flex align-baseline gap-xs bg-slate-100;
    &:hover {
      @apply text-brand-500;
    }

    &.active {
      @apply text-brand-500 bg-brand-100;
    }
  }
</style>