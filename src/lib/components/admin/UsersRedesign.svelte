<script lang="ts">
	import { getContext, tick, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	import { goto } from '$app/navigation';
	import { user } from '$lib/stores';

	import { deleteUserById, getUsers, updateUserRole } from '$lib/apis/users';

	import UserList from './Users/UserList.svelte';
	import Groups from './Users/Groups.svelte';
	import UserListRedesign from '$lib/components/admin/Users/UserListRedesign.svelte';
	import { getGroups } from '$lib/apis/groups';
	import UserDetail from '$lib/components/admin/Users/UserDetail.svelte';

	const i18n = getContext('i18n');

	let users = [];
	let groups = [];
	let usersWithGroups = [];

	let selectedTab = 'overview';
	let loaded = false;

	$: if (selectedTab) {
		getUsersHandler();
	}

	const getUsersHandler = async () => {
		users = await getUsers(localStorage.token);
	};

	let selectedUser = null;

	const handleSelectedUser = (user) => {
		selectedUser = user;
	}

	const updateRoleHandler = async (id, role) => {
		const res = await updateUserRole(localStorage.token, id, role).catch((error) => {
			toast.error(error);
			console.log(error);
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

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
		} else {
			users = await getUsers(localStorage.token);
			groups = await getGroups(localStorage.token);


			usersWithGroups = users.map((user) => {
				const userGroups = groups.filter((group) => group.user_ids.includes(user.id));
				return {
					...user,
					groups: userGroups.map((group) =>
						({
							id: group.id,
							name: group.name,
							description: group.description,
							members: group.user_ids,
						})
					)
				};
			});

			console.log('Users with groups', usersWithGroups);

		}
		loaded = true;

		const containerElement = document.getElementById('users-tabs-container');

		if (containerElement) {
			containerElement.addEventListener('wheel', function (event) {
				if (event.deltaY !== 0) {
					// Adjust horizontal scroll position based on vertical scroll
					containerElement.scrollLeft += event.deltaY;
				}
			});
		}
	});
</script>

<div class="flex flex-col lg:flex-row w-full h-full ">
<!--	overflow-y-scroll-->
	<div class="flex-1 flex ">
		{#if selectedTab === 'overview'}
			<div class="py-[24px] px-[16px] w-full">
				<UserListRedesign users={usersWithGroups} groups={groups} handleSelectedUser={handleSelectedUser}/>
			</div>
			{#if selectedUser}
				<div class="p-base w-[437px] bg-slate-50 bg-lvl-3 border-l border-slate-300 dark:border-slate-700">
					<UserDetail user={selectedUser} handleRoleUpdate={updateRoleHandler} handleUserDelete={deleteUserHandler} groups={groups}/>
				</div>
			{/if}
		{:else if selectedTab === 'groups'}
			<Groups {users} />
		{/if}
	</div>
</div>
