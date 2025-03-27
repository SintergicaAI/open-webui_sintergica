<script>
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	dayjs.extend(relativeTime);

	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';

	import { WEBUI_NAME, config, user, showSidebar, knowledge } from '$lib/stores';
	import { WEBUI_BASE_URL } from '$lib/constants';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Plus from '$lib/components/icons/Plus.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import UsersSolid from '$lib/components/icons/UsersSolid.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';
	import User from '$lib/components/icons/User.svelte';
	import UserCircleSolid from '$lib/components/icons/UserCircleSolid.svelte';
	import GroupModal from './Groups/EditGroupModal.svelte';
	import Pencil from '$lib/components/icons/Pencil.svelte';
	import GroupItem from './Groups/GroupItem.svelte';
	import AddGroupModal from './Groups/AddGroupModal.svelte';
	import { createNewGroup, getGroups } from '$lib/apis/groups';
	import { getUserDefaultPermissions, updateUserDefaultPermissions } from '$lib/apis/users';
	import GroupItemRedesign from '$lib/components/admin/Users/Groups/GroupItemRedesign.svelte';
	import { getUserById } from '$lib/apis/users';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Search, SquarePlus } from 'lucide-svelte';
	import TuringFaceOpenMouth from '$lib/components/icons/TuringFaceOpenMouth.svelte';
	import TuringFaceWinkyX from '$lib/components/icons/TuringFaceWinkyX.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	export let users = [];

	let groups = [];
	let filteredGroups;

	$: filteredGroups = groups.filter((user) => {
		if (search === '') {
			return true;
		} else {
			let name = user.name.toLowerCase();
			const query = search.toLowerCase();
			return name.includes(query);
		}
	});

	let search = '';
	let defaultPermissions = {
		workspace: {
			models: false,
			knowledge: false,
			prompts: false,
			tools: false
		},
		chat: {
			file_upload: true,
			delete: true,
			edit: true,
			temporary: true
		}
	};

	let showCreateGroupModal = false;
	let showDefaultPermissionsModal = false;

	const setGroups = async () => {
		groups = await getGroups(localStorage.token);
		groups = await Promise.all(
			groups.map(async (group) => {
				const author = await getUserById(localStorage.token, group.user_id);
				return { ...group, author };
			})
		);
		console.log('Groups', groups);
	};

	const addGroupHandler = async (group) => {
		const res = await createNewGroup(localStorage.token, group).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			toast.success($i18n.t('Group created successfully'));
			groups = await getGroups(localStorage.token);
		}
	};

	const updateDefaultPermissionsHandler = async (group) => {
		console.log(group.permissions);

		const res = await updateUserDefaultPermissions(localStorage.token, group.permissions).catch(
			(error) => {
				toast.error(error);
				return null;
			}
		);

		if (res) {
			toast.success($i18n.t('Default permissions updated successfully'));
			defaultPermissions = await getUserDefaultPermissions(localStorage.token);
		}
	};

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
		} else {
			await setGroups();
			defaultPermissions = await getUserDefaultPermissions(localStorage.token);
		}
		loaded = true;
	});
</script>

{#if loaded}
	<AddGroupModal bind:show={showCreateGroupModal} onSubmit={addGroupHandler} />
	<div class="flex ">
		<div class=" flex-grow py-2xl px-lg flex flex-col items-center gap-sm">
			<header class="w-full max-w-screen-xl flex flex-col md:flex-row justify-between ">
				<div>
					<Tooltip content={$i18n.t('New group')}>
						<Button variant="primary" icon={SquarePlus} onClick={()=>{showCreateGroupModal = !showCreateGroupModal;}}>{$i18n.t('New group')}</Button>
					</Tooltip>
				</div>


				<div class="flex ">
					<div class=" flex w-full space-x-2">
						<div class="flex md:self-center text-lg font-medium px-0.5">
							<span class="text-label text-gray-500 dark:text-gray-300">{groups.length} {$i18n.t('groups')}</span>
						</div>

						<div class="hidden md:flex w-full rounded-xl -mb-1 px-0.5 gap-2" id="settings-search">
							<div class="self-center rounded-l-xl bg-transparent">
								<Search className="size-3.5" />
							</div>
							<input
								class="w-full py-1.5 text-sm bg-transparent dark:text-gray-300 outline-none"
								bind:value={search}
								placeholder={$i18n.t('Search')}
							/>
						</div>

					</div>
				</div>
			</header>

			<section class="w-full max-w-screen-xl">
				{#if filteredGroups.length === 0}
					<div class="flex-1 flex flex-col items-center justify-center gap-2xl ">

						<div
							class=" flex flex-col items-center self-stretch flex-1  h-full ">
							<TuringFaceWinkyX />
						</div>

						<p class=" text-title text-brand-500 ">
							{$i18n.t('You do not have any groups yet')}
						</p>

						<p class="text-base text-slate-900 dark:text-slate-600">
							{$i18n.t('Create a')} <b class="text-brand-500">{$i18n.t('New group')}</b> {$i18n.t('to start adding users to it')}
						</p>
					</div>
				{:else}
					<div class="">
						<section class="grid grid-cols-2 gap-sm ">
							{#each filteredGroups as group}
								<a class="" href={`/dev/admin/groups/edit?id=${encodeURIComponent(group.id)}`}>
									<GroupItemRedesign {group} {users} {setGroups} />
								</a>
							{/each}

						</section>
					</div>
				{/if}


				<GroupModal
					bind:show={showDefaultPermissionsModal}
					tabs={['permissions']}
					bind:permissions={defaultPermissions}
					custom={false}
					onSubmit={updateDefaultPermissionsHandler}
				/>

				<button
					class="flex items-center justify-between rounded-lg w-full transition pt-1"
					on:click={() => {
				showDefaultPermissionsModal = true;
			}}
				>
					<div class="flex items-center gap-2.5">
						<div class="p-1.5 bg-black/5 dark:bg-white/10 rounded-full">
							<UsersSolid className="size-4" />
						</div>

						<div class="text-left">
							<div class=" text-sm font-medium">{$i18n.t('Default permissions')}</div>

							<div class="flex text-xs mt-0.5">
								{$i18n.t('applies to all users with the "user" role')}
							</div>
						</div>
					</div>

					<div>
						<ChevronRight strokeWidth="2.5" />
					</div>
				</button>
			</section>
		</div>
	</div>


{/if}
