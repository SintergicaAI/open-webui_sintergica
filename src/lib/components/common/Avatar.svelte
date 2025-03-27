<script lang="ts">
	export let type: 'button' | 'user' | 'assistant' = 'user';
	export let initials = '';        // Avatar initials
	export let name: string = ''
	export let size: 'sm' | 'base' | 'lg' = 'base';

	let active = false;
	let hovering = false;


	const SIZE_CLASSES = {
		sm: 'w-4 h-4',
		base: 'w-8 h-8',
		lg: 'w-12 h-12'
	};

	function getInitials(name: string): string {
		return name
			.split(' ') // Divide el nombre por espacios
			.map(word => word[0]?.toUpperCase() || '') // Toma la primera letra de cada palabra en mayúsculas
			.join('') // Une las iniciales
			.slice(0, 2); // Limita a 2 iniciales
	}

	// Si no hay iniciales definidas, calcula las iniciales del nombre
	$: initials = initials || name.split(' ').length > 1 ? getInitials(name) : name[0];



	function getSizeClass(): string {
		return SIZE_CLASSES[size];
	}

	function handleHover(state: boolean) {
		hovering = state;
		active = state ? active : false;
	}


	function handleMouseDown() {
		active = true;
	}

	function handleMouseUp() {
		active = false;
	}
</script>

<style>
    .avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 40px;
        width: 40px;
        font-size: 14px;
        font-weight: bold;
        color: #fff;
        @apply flex bg-brand-100 text-brand-500 rounded-full;
        user-select: none;
        transition: all 0.2s ease-in-out;
    }

    .avatar.hover {
        @apply bg-brand-500 text-white;
    }

    .avatar.active {
        background-color: #cce4ff;
        border-radius: 4px;
    }

    .avatar.button {
        cursor: pointer;
    }

    .avatar:disabled {
        background-color: #e0e0e0;
        opacity: 0.5;
    }
</style>

{#if type === 'button'}
	<button
		class={`avatar ${type} ${getSizeClass()} ${active ? 'active' : ''} ${!active && hovering ? 'hover' : ''}`}
		on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp}
		on:mouseenter={() => handleHover(true)}
		on:mouseleave={() => handleHover(false)}
	>
		{initials}
	</button>
{:else}
	<div class={`avatar ${type} ${getSizeClass()}`}>
		{initials}
	</div>
{/if}