<script>
	import { toast } from 'svelte-sonner';
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');

	import { deleteGroupById, updateGroupById } from '$lib/apis/groups';

	import Pencil from '$lib/components/icons/Pencil.svelte';
	import User from '$lib/components/icons/User.svelte';
	import UserCircleSolid from '$lib/components/icons/UserCircleSolid.svelte';
	import GroupModal from './EditGroupModal.svelte';
	import Pill from '$lib/components/common/Pill/Pill.svelte';
	import Card from '$lib/components/workspace/common/Card.svelte';

	export let users = [];
	export let group = {
		name: 'Admins',
		user_ids: [1, 2, 3]
	};

	export let setGroups = () => {};

	let showEdit = false;

	const updateHandler = async (_group) => {
		const res = await updateGroupById(localStorage.token, group.id, _group).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			toast.success($i18n.t('Group updated successfully'));
			setGroups();
		}
	};

	const deleteHandler = async () => {
		const res = await deleteGroupById(localStorage.token, group.id).catch((error) => {
			toast.error(error);
			return null;
		});

		if (res) {
			toast.success($i18n.t('Group deleted successfully'));
			setGroups();
		}
	};
</script>

<GroupModal
	bind:show={showEdit}
	edit
	{users}
	{group}
	onSubmit={updateHandler}
	onDelete={deleteHandler}
/>

<button
	class="rounded-md flex flex-col items-center gap-base justify-between  w-full bg-slate-50 dark:bg-slate-800 transition"
	on:click={() => {
		showEdit = true;
	}}
>
	<Card pillText={group.name} pillColor="brand" headerContent={`${group.user_ids.length} ${$i18n.t('members')}`} footerInfo={{updatedText: 'Created by', userName:group?.author.name, deletedUserText: "Deleted"}}/>
</button>

