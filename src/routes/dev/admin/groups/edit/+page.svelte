<script lang="ts">

	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getGroupById, updateGroupById } from '$lib/apis/groups';
	import { page } from '$app/stores';
	import GroupEditor from '$lib/components/admin/Users/Groups/GroupEditor.svelte';
	import { toast } from 'svelte-sonner';
	import { getUserById } from '$lib/apis/users';


	let group: any = null;

	const onSubmit = async (groupInfo) => {
		const res = await updateGroupById(localStorage.token, group.id, groupInfo).catch(e => {
			console.log(e);
		});

		if (res.ok){
			toast.success('Group updated successfully');
			await goto(`/dev/admin/groups`);
		}
		return null;
	};

	onMount(async () => {
		const _id = $page.url.searchParams.get('id');
		if (_id) {
			group = await getGroupById(localStorage.token, _id).catch((e) => {
				return null;
			});

			group.members = await Promise.all(group.user_ids.map(user_id => {
				return getUserById(localStorage.token, user_id);
			})).catch(e => {
				toast.error('Error fetching users');
			})

			console.log(
				'group with users',
				group
			);

			if (!group) {
				goto(`/dev/admin/groups`);

			}
		} else {
			goto(`/dev/admin/groups`);
		}
	});

	$: console.log('group fetched',group);
</script>

{#if group}
	<GroupEditor edit={true} {group} {onSubmit}/>
{/if}