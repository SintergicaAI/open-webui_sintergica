<script lang="ts">
	import Avatar from '$lib/components/common/Avatar.svelte';
	import {
		Circle,
		CircleCheck,
		CircleCheckBig,
		Search,
		Square,
		SquareCheck,
		SquareCheckBig,
		Trash2,
		X
	} from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { RadioGroup, Label, Checkbox } from 'bits-ui';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import { getContext } from 'svelte';
	import ConfirmDialog from '$lib/components/common/ConfirmDialog.svelte';
	const i18n = getContext('i18n');


	export let user = null;
	export let groups = [];
	export let handleRoleUpdate = (id:string, role:string) => {};
	export let handleUserDelete = (id:string) => {};

	let filteredGroups;
	let search = '';

	let isChecked = false;
	$: filteredGroups = groups
		.filter((group) => {
			if (search === '') {
				return true;
			} else {
				let name = group.name.toLowerCase();
				const query = search.toLowerCase();
				return name.includes(query);
			}
		});

	let showDeleteConfirmDialog = false;
</script>

{#if user}
	<ConfirmDialog
		bind:show={showDeleteConfirmDialog}
		on:confirm={() => {
		handleUserDelete(user.id);
	}}
	/>
	<div class="w-full h-full flex flex-col gap-base">
		<header class=" flex items-center gap-base self-stretch">
			<Avatar name={user.name} />
			<h2 class="text-subtitle text-black dark:text-white flex-1">{user.name}</h2>
			<Button icon={Trash2} iconSize="base" variant="icon" onClick={()=>{showDeleteConfirmDialog = !showDeleteConfirmDialog;}}/>
			<Button icon={X} size="base" variant="icon" iconSize="base" buttonClasses="text-slate-500"/>
		</header>

		<section class="flex flex-col items-start gap-sm self-stretch">
			<p class="text-label text-slate-500">Rol</p>
				<div class="self-stretch">
					<RadioGroup.Root bind:value={user.role} onValueChange={(role) => {
					handleRoleUpdate(user.id, role)
				}}>
						<div class="self-stretch gap-xs grid grid-cols-2 items-start">
							<div class="flex-1 flex-shrink-0 rounded-md p-sm flex h-4xl text-base text-slate-500 justify-between {user.role === 'user' ? 'bg-brand-100 dark:bg-brand-900' : 'bg-slate-100 dark:bg-slate-900'}">
								<Label.Root for="user">User</Label.Root>
								<RadioGroup.Item id="user" value="user" class=" cursor-default bg-background transition-all duration-100 ease-in-out hover:border-brand-500 " >
									<Circle size="20" class="text-slate-500 {user.role === 'user' ? 'hidden' : ''}"/>
									<RadioGroup.ItemIndicator>
										<CircleCheckBig size="20" class="text-brand-500"/>
									</RadioGroup.ItemIndicator>
								</RadioGroup.Item>
							</div>
							<div class="flex-1 flex-shrink-0 rounded-md p-sm flex h-4xl text-base text-slate-500 justify-between {user.role === 'admin' ? 'bg-brand-100 dark:bg-brand-900' : 'bg-slate-100 dark:bg-slate-900'}">
								<Label.Root for="admin" class="  overflow-hidden text-ellipsis line-clamp-1">Administrador</Label.Root>
								<RadioGroup.Item id="admin" value="admin" class=" cursor-default bg-background transition-all duration-100 ease-in-out hover:border-brand-500 " >
									<Circle size="20" class="text-slate-500 {user.role === 'admin' ? 'hidden' : ''}"/>
									<RadioGroup.ItemIndicator>
										<CircleCheckBig size="20" class="text-brand-500"/>
									</RadioGroup.ItemIndicator>
								</RadioGroup.Item>
							</div>
							<div class="flex-1 flex-shrink-0 rounded-md p-sm h-4xl flex text-base text-slate-500 justify-between {user.role === 'pending' ? 'bg-brand-100 dark:bg-brand-900' : 'bg-slate-100 dark:bg-slate-900'}">
								<Label.Root for="pending">Pending</Label.Root>
								<RadioGroup.Item id="pending" value="pending" class=" cursor-default bg-background transition-all duration-100 ease-in-out hover:border-brand-500 " >
									<Circle size="20" class="text-slate-500 {user.role === 'pending' ? 'hidden':''}"/>
									<RadioGroup.ItemIndicator>
										<CircleCheckBig size="20" class="text-brand-500"/>
									</RadioGroup.ItemIndicator>
								</RadioGroup.Item>
							</div>
						</div>
					</RadioGroup.Root>

				</div>


		</section>

		<section class="flex flex-col items-start gap-sm self-stretch">

			<h4 class="text-label text-slate-500">Grupos a los que pertenece</h4>
			<div class="self-stretch p-base inline-flex justify-center rounded-sm items-center border bg-white dark:bg-brand-950 dark:border-slate-700">
				<input
					class=" flex-1 text-base text-slate-500 placeholder:text-slate-500 placeholder:text-placeholder text-sm w-full outline-none bg-transparent"
					bind:value={search}
					placeholder={$i18n.t('Search')}
				/>
				<Search size="20" class="text-slate-500" />
			</div>

			<div class="flex flex-col self-stretch gap-sm ">

				{#each filteredGroups as group}
					<div class="flex justify-between items-center rounded-sm p-sm self-stretch gap-sm {group.user_ids.includes(user.id) ? 'bg-brand-100 dark:bg-brand-900' : 'bg-slate-100 dark:bg-slate-900'}">
						<Pill pillColor="brand" text={group.name}/>

						<div class="flex justify-end items-center gap-sm">
							<i class="text-label text-slate-500">{group.user_ids.length} miembros</i>
							<Checkbox.Root id={group.id} class="cursor-pointer" checked={group.user_ids.includes(user.id)}>
								<Checkbox.Input id={group.id} checked={group.user_ids.includes(user.id)} />
								<Checkbox.Indicator let:isChecked>
									{#if isChecked }
										<SquareCheckBig size="20" class="text-brand-500"/>
									{:else}
										<Square size="20" class="text-slate-500"/>
									{/if}
								</Checkbox.Indicator>
							</Checkbox.Root>
						</div>
					</div>
				{/each}
			</div>
		</section>
	</div>
{:else}
	<div class="user-detail">
		<p>Seleccione un usuario para ver detalles</p>
	</div>
{/if}

<style>

</style>