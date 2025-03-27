<script>
	import { config, user } from '$lib/stores';
	import { onMount, getContext } from 'svelte';

	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	dayjs.extend(relativeTime);

	import { toast } from 'svelte-sonner';

	import { updateUserRole, getUsers, deleteUserById } from '$lib/apis/users';

	import Pagination from '$lib/components/common/Pagination.svelte';
	import ChatBubbles from '$lib/components/icons/ChatBubbles.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	import EditUserModal from '$lib/components/admin/Users/UserList/EditUserModal.svelte';
	import UserChatsModal from '$lib/components/admin/Users/UserList/UserChatsModal.svelte';
	import AddUserModal from '$lib/components/admin/Users/UserList/AddUserModal.svelte';

	import ConfirmDialog from '$lib/components/common/ConfirmDialog.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import { Toggle, ToggleGroup, Popover, Checkbox, Label } from 'bits-ui';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import { Search, Send, Square, SquareCheckBig, SquarePlus } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import Avatar from '$lib/components/common/Avatar.svelte';
	import InviteUserModal from '$lib/components/admin/Users/UserList/InviteUserModal.svelte';
	import Switch from '$lib/components/chat/Switch.svelte';

	const i18n = getContext('i18n');

	// Constants
	const DEFAULT_SORT_KEY = 'created_at';
	const DEFAULT_SORT_ORDER = 'asc';

	// Props
	export let users = [];
	export let groups = [];
	export let invitedUsers = [];
	export let handleSelectedUser = (user) => {};


	let filters = [];

	let selectedTab = 'users'
	let selectedGroupFilters = [];

	onMount(async () => {
		groups.forEach(filter => {
			selectedGroupFilters[filter.id] = false;
		})
	})

	$: applyFilters = () => {
		const activeFilters = Object.keys(selectedGroupFilters).filter(key => selectedGroupFilters[key]);
		console.log('Filtros aplicados', activeFilters);
	}

	let search = '';
	let selectedUser = null;
	let popoverOpen = false;

	let page = 1;

	let showDeleteConfirmDialog = false;
	let showAddUserModal = false;
	let showInviteUserModal = false;

	let showUserChatsModal = false;
	let showEditUserModal = false;

	const updateRoleHandler = async (id, role) => {
		const res = await updateUserRole(localStorage.token, id, role).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			users = await getUsers(localStorage.token);
		}
	};

	const deleteUserHandler = async (id) => {
		const res = await deleteUserById(localStorage.token, id).catch((error) => {
			toast.error(error);
			return null;
		});
		if (res) {
			users = await getUsers(localStorage.token);
		}
	};

	let sortKey = 'created_at'; // default sort key
	let sortOrder = 'asc'; // default sort order

	function setSortKey(key) {
		if (sortKey === key) {
			sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortOrder = 'asc';
		}
	}

	let filteredUsers;

	$: filteredUsers = users
		.filter((user) => {
			if (search !== '') {
				const name = user.name.toLowerCase();
				const query = search.toLowerCase();
				if (!name.includes(query)) {
					return false;
				}
			}

			// FILTRO POR GRUPOS
			const activeFilters = Object.keys(selectedGroupFilters).filter(
				(key) => selectedGroupFilters[key]
			);

			if (activeFilters.length > 0) {
				// Comprueba si el usuario tiene algún grupo con un ID en `activeFilters`
				const hasMatchingGroup = user.groups.some((group) =>
					activeFilters.includes(String(group.id))
				);
				if (!hasMatchingGroup) {
					return false;
				}
			}

			return true;
		})
		.sort((a, b) => {
			if (a[sortKey] < b[sortKey]) return sortOrder === 'asc' ? -1 : 1;
			if (a[sortKey] > b[sortKey]) return sortOrder === 'asc' ? 1 : -1;
			return 0;
		})
		.slice((page - 1) * 20, page * 20);

	$: invitedUsers = users
		.filter((user) => {
			if (search !== '') {
				const name = user.name.toLowerCase();
				const query = search.toLowerCase();
				if (!name.includes(query)) {
					return false;
				}
			}

			// FILTRO POR GRUPOS
			const activeFilters = Object.keys(selectedGroupFilters).filter(
				(key) => selectedGroupFilters[key]
			);

			if (user.role !== 'pending') {
				return false;
			}

			if (activeFilters.length > 0) {
				// Comprueba si el usuario tiene algún grupo con un ID en `activeFilters`
				const hasMatchingGroup = user.groups.some((group) =>
					activeFilters.includes(String(group.id))
				);
				if (!hasMatchingGroup) {
					return false;
				}
			}

			return true;
		})
		.sort((a, b) => {
			if (a[sortKey] < b[sortKey]) return sortOrder === 'asc' ? -1 : 1;
			if (a[sortKey] > b[sortKey]) return sortOrder === 'asc' ? 1 : -1;
			return 0;
		})
		.slice((page - 1) * 20, page * 20);
</script>

<ConfirmDialog
	bind:show={showDeleteConfirmDialog}
	on:confirm={() => {
		deleteUserHandler(selectedUser.id);
	}}
/>

{#key selectedUser}
	<EditUserModal
		bind:show={showEditUserModal}
		{selectedUser}
		sessionUser={$user}
		on:save={async () => {
			users = await getUsers(localStorage.token);
		}}
	/>
{/key}

<AddUserModal
	bind:show={showAddUserModal}
	on:save={async () => {
		users = await getUsers(localStorage.token);
	}}
/>

<InviteUserModal
	bind:show={showInviteUserModal}
	on:save={async () => {
		users = await getUsers(localStorage.token);
	}}
/>
<UserChatsModal bind:show={showUserChatsModal} user={selectedUser} />

<header class="self-stretch flex flex-col md:flex-row justify-between ">
	<div class="flex gap-1">
		<Tooltip content={$i18n.t('Add User')}>
			<Button onClick={() => {
						showAddUserModal = !showAddUserModal;
					}} icon={SquarePlus}>
				Nuevo usuario
			</Button>
		</Tooltip>

		<Tooltip content={$i18n.t('Invite User')}>
			<Button onClick={() => {
				showInviteUserModal = !showInviteUserModal;
			}} variant="outline-primary" icon={Send}>
				Invitar usuario
			</Button>
		</Tooltip>
	</div>

	<div class="flex gap-1">
		<div class=" flex items-center gap-base w-full ">
			<span class="text-label text-slate-500 dark:text-gray-300">{users.length} {$i18n.t('users')}</span>

			<div class="self-stretch p-base inline-flex justify-center rounded-sm items-center border 	bg-white dark:bg-brand-950 dark:border-slate-700">
				<input
					class=" flex-1 text-base text-slate-500 placeholder:text-slate-500 placeholder:text-placeholder w-full outline-none bg-transparent"
					bind:value={search}
					placeholder={$i18n.t('Search')}
				/>
				<Search size="20" class="text-slate-500" />
			</div>
		</div>
	</div>
</header>
<!-- Filter per groups -->
<section class="flex flex-col justify-center items-start gap-sm self-stretch ">
	<p class="text-slate-400 text-label">Filtrar por grupos</p>
	<form on:change={applyFilters} class="flex flex-wrap items-center content-center self-stretch gap-sm">
		{#each groups as group}
			<Switch activeLabel={group.name} inactiveLabel={group.name} bind:state={selectedGroupFilters[group.id]}/>
		{/each}


	</form>
</section>
<section class="scrollbar-hidden relative whitespace-nowrap overflow-x-auto max-w-full rounded ">
	<header class="self-stretch flex items-center border-b border-slate-700">
		<button on:click={()=>{selectedTab='users'}} class="text-button {selectedTab === 'users'? 'text-brand-500' : 'text-slate-500'} border-b border-brand-500 flex px-lg py-sm ">
			Activos
		</button>
		<button on:click={()=>{selectedTab='invitations'}} class="text-button {selectedTab === 'invitations'? 'text-brand-500' : 'text-slate-500'} flex px-lg py-sm ">
			Invitados
		</button>
	</header>

	{#if selectedTab === 'users'}
	<table
		class="border-separate border-spacing-y-sm w-full text-label text-left text-slate-500 table-auto max-w-full rounded"
	>
		<thead
			class="text-label text-slate-500 bg-transparent "
		>
			<tr class="">
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('name')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Name')}

						{#if sortKey === 'name'}
							<span class="font-normal"
								>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('role')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Role')}

						{#if sortKey === 'role'}
							<span class="font-normal"
							>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('email')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Email')}

						{#if sortKey === 'email'}
							<span class="font-normal"
								>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>

				<th scope="col" class="px-3 py-1.5 cursor-pointer select-none">
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Groups')}
					</div>
				</th>

				<th scope="col" class="px-3 py-2 text-right" />
			</tr>
		</thead>
		<tbody class="space-y-1.5">
			{#each filteredUsers as user}
				<tr class="{selectedUser?.name === user.name ?
					(selectedUser?.name === 'Yaz'? 'bg-pink-50 text-pink-600' : 'bg-brand-50 dark:bg-brand-900 dark:border-brand-700 text-brand-500')
					:' bg-slate-50 dark:bg-slate-800 dark:border-slate-800'} p-base   " on:click={() => {selectedUser=user; handleSelectedUser(user)}}>
					<td class=" rounded-l-md border-l border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base dark:text-white w-max">
						<div class="flex flex-row w-max gap-base">
							<Avatar name={user.name}/>
							<div class=" font-medium self-center">{user.name}</div>
						</div>
					</td>
					<td class="border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base min-w-[7rem] w-44">
						<button
							class=" translate-y-0.5"
						>
							{$i18n.t(user.role).at(0).toUpperCase() + $i18n.t(user.role).slice(1)}
						</button>
					</td>
					<td class=" border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base"> {user.email} </td>

					<td class=" border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base w-20">
						{#if user.groups.length > 0}
								<Popover.Root bind:open={popoverOpen}>
								<Popover.Trigger class="inline-flex h-10
									items-center justify-center whitespace-nowrap rounded-input bg-transparent px-[21px] text-[15px] font-medium shadow-mini transition-all hover:cursor-pointer hover:bg-dark/95 active:scale-98">
									{`${user.groups.length} ${$i18n.t('groups')} `}
								</Popover.Trigger>
								<Popover.Content
									class="z-30 flex flex-col items-start rounded-lg gap-sm max-w-[420px] border border-slate-300 bg-white p-lg shadow-md"
									sideOffset={8}
								>
									<div class="self-stretch text-slate-500 text-label ">Grupos a los que pertenece</div>
									<div class="self-stretch flex flex-wrap items-center content-center gap-xs">
										{#each user.groups as group}
											<Pill text="{group.name}" pillColor="brand"/>
										{/each}
									</div>
								</Popover.Content>
							</Popover.Root>
						{:else}
							Sin grupos
						{/if}
					</td>

					<td class=" rounded-r-md border-r border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base text-right">
						<div class="flex justify-end w-full">
							{#if $config.features.enable_admin_chat_access && user.role !== 'admin'}
								<Tooltip content={$i18n.t('Chats')}>
									<button
										class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
										on:click={async () => {
											showUserChatsModal = !showUserChatsModal;
											selectedUser = user;
										}}
									>
										<ChatBubbles />
									</button>
								</Tooltip>
							{/if}

							<Tooltip content={$i18n.t('Edit User')}>
								<button
									class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
									on:click={async () => {
										showEditUserModal = !showEditUserModal;
										selectedUser = user;
									}}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-4 h-4"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
										/>
									</svg>
								</button>
							</Tooltip>

							{#if user.role !== 'admin'}
								<Tooltip content={$i18n.t('Delete User')}>
									<button
										class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
										on:click={async () => {
											showDeleteConfirmDialog = true;
											selectedUser = user;
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke-width="1.5"
											stroke="currentColor"
											class="w-4 h-4"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
											/>
										</svg>
									</button>
								</Tooltip>
							{/if}
						</div>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
	{:else if selectedTab  === 'invitations'}
		<table
			class="border-separate border-spacing-y-sm w-full text-label text-left text-slate-500 table-auto max-w-full rounded"
		>
			<thead
				class="text-label text-slate-500 bg-transparent "
			>
			<tr class="">
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('name')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Name')}

						{#if sortKey === 'name'}
							<span class="font-normal"
							>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('role')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Role')}

						{#if sortKey === 'role'}
							<span class="font-normal"
							>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>
				<th
					scope="col"
					class="px-3 py-1.5 cursor-pointer select-none"
					on:click={() => setSortKey('email')}
				>
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Email')}

						{#if sortKey === 'email'}
							<span class="font-normal"
							>{#if sortOrder === 'asc'}
									<ChevronUp className="size-2" />
								{:else}
									<ChevronDown className="size-2" />
								{/if}
							</span>
						{:else}
							<span class="invisible">
								<ChevronUp className="size-2" />
							</span>
						{/if}
					</div>
				</th>

				<th scope="col" class="px-3 py-1.5 cursor-pointer select-none">
					<div class="flex gap-1.5 items-center">
						{$i18n.t('Groups')}
					</div>
				</th>

				<th scope="col" class="px-3 py-2 text-right" />
			</tr>
			</thead>
			<tbody class="space-y-1.5">
			{#each invitedUsers as user}
				<tr class="{selectedUser?.name === user.name ?
					(selectedUser?.name === 'Yaz'? 'bg-pink-50 text-pink-600' : 'bg-brand-50 dark:bg-brand-900 dark:border-brand-700 text-brand-500')
					:' bg-slate-50 dark:bg-slate-800 dark:border-slate-800'} p-base   " on:click={() => {selectedUser=user; handleSelectedUser(user)}}>
					<td class=" rounded-l-md border-l border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base dark:text-white w-max">
						<div class="flex flex-row w-max gap-base">
							<Avatar name={user.name}/>
							<div class=" font-medium self-center">{user.name}</div>
						</div>
					</td>
					<td class="border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base min-w-[7rem] w-44">
						<button
							class=" translate-y-0.5"
						>
							{$i18n.t(user.role).at(0).toUpperCase() + $i18n.t(user.role).slice(1)}
						</button>
					</td>
					<td class=" border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base"> {user.email} </td>

					<td class=" border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base w-20">
						{#if user.groups.length > 0}
							<Popover.Root bind:open={popoverOpen}>
								<Popover.Trigger class="inline-flex h-10
									items-center justify-center whitespace-nowrap rounded-input bg-transparent px-[21px] text-[15px] font-medium shadow-mini transition-all hover:cursor-pointer hover:bg-dark/95 active:scale-98">
									{`${user.groups.length} ${$i18n.t('groups')} `}
								</Popover.Trigger>
								<Popover.Content
									class="z-30 flex flex-col items-start rounded-lg gap-sm max-w-[420px] border border-slate-300 bg-white p-lg shadow-md"
									sideOffset={8}
								>
									<div class="self-stretch text-slate-500 text-label ">Grupos a los que pertenece</div>
									<div class="self-stretch flex flex-wrap items-center content-center gap-xs">
										{#each user.groups as group}
											<Pill text="{group.name}" pillColor="brand"/>
										{/each}
									</div>
								</Popover.Content>
							</Popover.Root>
						{:else}
							Sin grupos
						{/if}
					</td>

					<td class=" rounded-r-md border-r border-y {selectedUser?.name === user.name ? selectedUser?.name === 'Yaz'? 'border-pink-600' :'border-brand-200 dark:border-brand-700':'border-slate-200 dark:border-slate-800'} px-3 py-base text-right">
						<div class="flex justify-end w-full">
							{#if $config.features.enable_admin_chat_access && user.role !== 'admin'}
								<Tooltip content={$i18n.t('Chats')}>
									<button
										class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
										on:click={async () => {
											showUserChatsModal = !showUserChatsModal;
											selectedUser = user;
										}}
									>
										<ChatBubbles />
									</button>
								</Tooltip>
							{/if}

							<Tooltip content={$i18n.t('Edit User')}>
								<button
									class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
									on:click={async () => {
										showEditUserModal = !showEditUserModal;
										selectedUser = user;
									}}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-4 h-4"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
										/>
									</svg>
								</button>
							</Tooltip>

							{#if user.role !== 'admin'}
								<Tooltip content={$i18n.t('Delete User')}>
									<button
										class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
										on:click={async () => {
											showDeleteConfirmDialog = true;
											selectedUser = user;
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke-width="1.5"
											stroke="currentColor"
											class="w-4 h-4"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
											/>
										</svg>
									</button>
								</Tooltip>
							{/if}
						</div>
					</td>
				</tr>
			{/each}
			</tbody>
		</table>
	{/if}
</section>

<div class="self-stretch">
	<Pagination bind:page count={users.length} />
</div>
