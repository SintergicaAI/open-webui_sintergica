<script lang="ts">

	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getGroupById, updateGroupById } from '$lib/apis/groups';
	import { page } from '$app/stores';
	import GroupEditor from '$lib/components/admin/Users/Groups/GroupEditor.svelte';
	import { toast } from 'svelte-sonner';
	import { getUserById, getUsers } from '$lib/apis/users';
	import { knowledge, members, models } from '$lib/stores';
	import { getModels } from '$lib/apis/models';
	import { getKnowledgeBases } from '$lib/apis/knowledge';

	interface Model {
		id: string;
		object: string;
		created: number;
		owned_by: string;
		name: string;
		openai?: {
			id: string;
			object: string;
			created: number;
			owned_by: string;
		};
		urlIdx?: number;
		arena?: boolean;
		preset?: boolean;
		info?: any;
		actions: any[];
	}

	interface Group {
		id: string;
		user_id: string;
		name: string;
		description: string;
		permissions: {
			workspace: {
				models: boolean;
				knowledge: boolean;
				prompts: boolean;
				tools: boolean;
			};
			chat: {
				file_upload: boolean;
				delete: boolean;
				edit: boolean;
				temporary: boolean;
			};
		};
		data: any;
		meta: any;
		user_ids: string[];
		created_at: number;
		updated_at: number;
		models?: Model[]; // Esta propiedad la agregaremos
	}


	let group: any = null;

	const onSubmit = async (groupInfo) => {
		console.log('groupInfo', groupInfo);

		//WIP: group changes submition
		return null;
	};


	function mapModelsToGroup(_models, group: Group) {
		const enhancedGroup = JSON.parse(JSON.stringify(group));

		// _models = assistants
		enhancedGroup.models = [];

		_models.forEach(model => {
			if (model.access_control && model.access_control.read && model.access_control.read.group_ids){
				model.access_control.read.group_ids.forEach(group_id => {
					const group = enhancedGroup;
					if (group_id === group.id){
						group.models.push(model);
					}
				})
			}
		})
		return enhancedGroup;
	}

	function mapKnowledgeBasesToGroup(_knowledge, group: Group) {
		const enhancedGroup = JSON.parse(JSON.stringify(group));

		enhancedGroup.knowledgeBases = [];

		_knowledge.forEach(knowledge => {
			if(knowledge.access_control && knowledge.access_control.read && knowledge.access_control.read.group_ids){
				knowledge.access_control.read.group_ids.forEach(group_id => {
					const group = enhancedGroup;
					if (group_id === group.id){
						group.knowledgeBases.push(knowledge);
					}
				})
			}
		})

		return enhancedGroup;
	}

	function mapMembersToGroup(_members, group: Group) {
		const enhancedGroup = JSON.parse(JSON.stringify(group));
		enhancedGroup.members = [];
		group.user_ids.forEach(user_id => {
			const member = _members.find(member => member.id === user_id);
			if (member){
				enhancedGroup.members.push(member);
			}
		})
		return enhancedGroup;
	}

	onMount(async () => {
		members.set(await getUsers(localStorage.token))
		models.set(await getModels(localStorage.token))
		knowledge.set(await getKnowledgeBases(localStorage.token))

		const _id = $page.url.searchParams.get('id');
		if (_id) {
			group = await getGroupById(localStorage.token, _id).catch((e) => {
				return null;
			});

			console.log('Knowledge', $knowledge);

			group = mapMembersToGroup($members, group);
			group = mapModelsToGroup($models, group);
			group = mapKnowledgeBasesToGroup($knowledge, group);

			console.log('Group after mapping', group);

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