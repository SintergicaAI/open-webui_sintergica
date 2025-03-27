<script lang="ts">
	export let id:string, src:string, heading, description;
	// on:click={(e)=>{console.log('Hola', e.target.id); info.base_model_id = model.id}}
	export let selected = false;

	function handleClick() {
		selected = !selected;
		const event = new CustomEvent('change', {
			detail:{id, value: selected}
		});
		dispatchEvent(event);
	}

</script>

<li class="list-none self-stretch">
	<button {id} class="self-stretch w-full {selected? 'bg-brand-50 dark:bg-brand-800' : 'bg-slate-50 hover:bg-white dark:hover:bg-slate-900  dark:bg-slate-800 disabled:opacity-40 disabled:bg-white disabled:dark:bg-slate-950'} gap-sm p-base flex
							border border-slate-300 dark:border-slate-700
						rounded-sm" on:click|stopPropagation={handleClick}>
		<div class="flex items-start">
			<slot name="image">
				<img sizes="100vw" {src} alt="splash" class="size-6 object-cover" />
			</slot>
		</div>
		<div class=" flex flex-col items-start flex-1 gap-sm">
			<h2 class="self-stretch text-subtitle text-start text-slate-950 dark:text-slate-50">{heading}</h2>
			<p class="self-stretch text-label text-start text-slate-500 dark:text-slate-500">
				{description}
			</p>
		</div>
	</button>
</li>