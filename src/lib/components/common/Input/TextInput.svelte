<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Eye, EyeClosed } from 'lucide-svelte';

	export let id;
	export let type = 'text';
	export let value = '';
	export let placeholder = 'Enter text';
	export let disabled = false;
	export let required = false;
	export let label = ''; // Optional label
	export let icon = undefined; // Optional icon
	let isPasswordVisible = false;
	export let showPasswordIcon = Eye; // Dynamic icon for show password
	export let hidePasswordIcon = EyeClosed;

	const dispatch = createEventDispatcher();

	function togglePasswordVisibility() {

		isPasswordVisible = !isPasswordVisible;
		dispatch('toggled', { value });
	}


	function handleInput(event) {
		value = event.target.value;
		dispatch('input', { value });
	}

	function handleBlur() {
		dispatch('blur', { value });
	}

	function handleFocus() {
		dispatch('focus', { value });
	}

</script>

<div>
	{#if label}
		<label class="text-label text-slate-500" for={id}>{label}</label>
	{/if}
	<div class=" group
	bg-white dark:bg-slate-800
	border border-slate-300 dark:border-slate-700
	text-base text-slate-950 dark:text-white
	flex items-center p-base
	 focus-within:ring-2 focus-within:ring-brand-300 focus-within:dark:ring-brand-700 rounded-sm">

		{#if type === 'text'}
			<input id={id} type="text" bind:value {placeholder} {disabled} {required} on:input={handleInput} on:blur={handleBlur}
						 on:focus={handleFocus}
						 class="bg-transparent placeholder:text-placeholder placeholder:text-slate-500 flex-grow outline-none border-slate-300 dark:border-slate-700" />
		{:else if type === 'password'}
				{#if isPasswordVisible}
					<input id={id} type="text" bind:value {placeholder} {disabled} {required} on:input={handleInput} on:blur={handleBlur}
							 class="bg-transparent placeholder:text-placeholder placeholder:text-slate-500 flex-grow outline-none border-slate-300 dark:border-slate-700" />
				{:else}
						<input id={id} type="password" bind:value {placeholder} {disabled} {required} on:input={handleInput} on:blur={handleBlur}
							 on:focus={handleFocus}
							 class="bg-transparent placeholder:text-placeholder placeholder:text-slate-500 flex-grow outline-none border-slate-300 dark:border-slate-700" />
				{/if}
		{:else if type === 'email'}
			<input id={id} type="email" bind:value {placeholder} {disabled} {required} on:input={handleInput} on:blur={handleBlur}
						 on:focus={handleFocus}
						 class="bg-transparent placeholder:text-placeholder placeholder:text-slate-500 flex-grow outline-none border-slate-300 dark:border-slate-700" />
		{:else}
			<input id={id} type='text' bind:value {placeholder} {disabled} {required} on:input={handleInput} on:blur={handleBlur}
						 on:focus={handleFocus}
						 class="bg-transparent placeholder:text-placeholder placeholder:text-slate-500 flex-grow outline-none border-slate-300 dark:border-slate-700" />
		{/if}

		<div class="text-slate-500">
			{#if type === 'password'}
				{#if isPasswordVisible}
					<button type="button" on:click={togglePasswordVisibility}>
						<svelte:component this={hidePasswordIcon} class="text-slate-500 cursor-pointer" />
					</button>
				{:else}
					<button type="button" on:click={togglePasswordVisibility}>
						<svelte:component this={showPasswordIcon} class="text-slate-500 cursor-pointer" />

					</button>
				{/if}
			{:else}
				<slot name="icon" class="text-slate-500"></slot>
			{/if}
		</div>
	</div>

</div>


<style lang="scss">
  .label {
    @apply block mb-2 text-gray-700 font-medium;
  }

	.icon-container {
		@apply flex items-center justify-center
	}
</style>