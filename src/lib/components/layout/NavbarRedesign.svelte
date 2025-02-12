<script>
	import { ChevronDown, CircleHelp, Package, Share2, SidebarClose } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import { Settings } from 'lucide-svelte';
	import { Clipboard } from 'lucide-svelte';
	import { DropdownMenu } from 'bits-ui';
	export let title = '';
</script>
<header class="border-b border-slate-300 flex justify-between items-center p-base">
			<div class="flex gap-x-base items-center">
				<SidebarClose class="icon icon--lg text-slate-500" />
				<DropdownMenu.Root>
					<DropdownMenu.Trigger>
						<div class="flex gap-x-base items-center">
							<div class="flex flex-col justify-center align-center rounded-full bg-orange-400 w-8 h-8 gap-sm ">
							</div>
							<h2 class="text-title">Model name</h2>
							<ChevronDown class="text-slate-500"/>
						</div>
					</DropdownMenu.Trigger>
					<DropdownMenu.Content>
						<DropdownMenu.Item class="text-label cursor-pointer hover:bg-slate-100">
							Model 1
						</DropdownMenu.Item>
						<DropdownMenu.Item class="text-label">
							Model 2
						</DropdownMenu.Item>
					</DropdownMenu.Content>
				</DropdownMenu.Root>
				<span class="text-slate-500">|</span>
				<h2 class="text-subtitle">{title}</h2>
			</div>

			<div class="flex gap-x-sm">
				<Button variant="icon" size="sm" icon={Package} buttonClasses="text-slate-500"/>
				<Button variant="icon" size="sm" icon={Clipboard} buttonClasses="text-slate-500"/>
				<Button variant="icon" size="sm" icon={Share2} buttonClasses="text-slate-500"/>
				<Button variant="icon" size="sm" icon={CircleHelp} buttonClasses="text-slate-500"/>
				<Button variant="icon" size="sm" icon={Settings} buttonClasses="text-slate-500"/>
			</div>
		</header>