<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher } from 'svelte';
	import { onMount, getContext } from 'svelte';
	import { addUser } from '$lib/apis/auths';

	import { WEBUI_BASE_URL } from '$lib/constants';

	import Modal from '$lib/components/common/Modal.svelte';
	import { X } from 'lucide-svelte';
	import Textarea from '$lib/components/common/Textarea.svelte';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	let inputClasses =
		'w-full rounded-sm p-sm ' +
		'text-black dark:text-slate-50 text-markdown-base placeholder:text-placeholder placeholder:text-slate-500 ' +
		'bg-white dark:bg-slate-950 ' +
		'border border-slate-300 outline-none resize-none h-full dark:border-slate-700 dark:bg-slate-950';

	export let show = false;

	let loading = false;
	let tab = '';
	let inputFiles;

	let _user = {
		name: '',
		email: '',
		password: '',
		role: 'user'
	};

	$: if (show) {
		_user = {
			name: '',
			email: '',
			password: '',
			role: 'user'
		};
	}

	const submitHandler = async () => {
		const stopLoading = () => {
			dispatch('save');
			loading = false;
		};

		if (tab === '') {
			loading = true;

			const res = await addUser(
				localStorage.token,
				_user.name,
				_user.email,
				_user.password,
				_user.role
			).catch((error) => {
				toast.error(error);
			});

			if (res) {
				stopLoading();
				show = false;
			}
		} else {
			if (inputFiles) {
				loading = true;

				const file = inputFiles[0];
				const reader = new FileReader();

				reader.onload = async (e) => {
					const csv = e.target.result;
					const rows = csv.split('\n');

					let userCount = 0;

					for (const [idx, row] of rows.entries()) {
						const columns = row.split(',').map((col) => col.trim());
						console.log(idx, columns);

						if (idx > 0) {
							if (
								columns.length === 4 &&
								['admin', 'user', 'pending'].includes(columns[3].toLowerCase())
							) {
								const res = await addUser(
									localStorage.token,
									columns[0],
									columns[1],
									columns[2],
									columns[3].toLowerCase()
								).catch((error) => {
									toast.error(`Row ${idx + 1}: ${error}`);
									return null;
								});

								if (res) {
									userCount = userCount + 1;
								}
							} else {
								toast.error(`Row ${idx + 1}: invalid format.`);
							}
						}
					}

					toast.success(`Successfully imported ${userCount} users.`);
					inputFiles = null;
					const uploadInputElement = document.getElementById('upload-user-csv-input');

					if (uploadInputElement) {
						uploadInputElement.value = null;
					}

					stopLoading();
				};

				reader.readAsText(file);
			} else {
				toast.error($i18n.t('File not found.'));
			}
		}
	};
	let invitationMessage = '';
</script>

<Modal size="md" bind:show>
	<div class="bg-slate-50 dark:bg-slate-950 rounded-xl shadow-lg w-full overflow-hidden">
		<header class=" flex justify-between dark:text-gray-300 p-2xl border-b border-slate-500">
			<h1 class=" text-title text-black dark:text-white self-center">{$i18n.t('Invite new user')}</h1>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<X size={20} class="text-slate-500"/>
			</button>
		</header>

		<section class="flex flex-col md:flex-row w-full py-lg px-2xl md:space-x-4 dark:text-gray-200">
			<div class=" flex flex-col w-full sm:flex-row sm:justify-center sm:space-x-6">
				<form
					class="flex flex-col w-full"
					on:submit|preventDefault={() => {
						submitHandler();
					}}
				>
					<div class="px-1">
						{#if tab === ''}
							<div class="flex flex-col w-full">
								<div class=" mb-1 text-label text-slate-400">{$i18n.t('Role')}</div>

								<div class="flex-1">
									<select
										class="{inputClasses} w-full capitalize disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
										bind:value={_user.role}
										placeholder={$i18n.t('Enter Your Role')}
										required
									>
										<option value="pending"> {$i18n.t('pending')} </option>
										<option value="user"> {$i18n.t('user')} </option>
										<option value="admin"> {$i18n.t('admin')} </option>
									</select>
								</div>
							</div>

							<div class="flex flex-col w-full mt-1">
								<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Name')}</div>

								<div class="flex-1">
									<input
										class="{inputClasses} w-full disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
										type="text"
										bind:value={_user.name}
										placeholder={$i18n.t('Enter Your Full Name')}
										autocomplete="off"
										required
									/>
								</div>
							</div>

							<hr class=" border-gray-50 dark:border-gray-850 my-2.5 w-full" />

							<div class="flex flex-col w-full">
								<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Email')}</div>

								<div class="flex-1">
									<input
										class="{inputClasses} w-full disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
										type="email"
										bind:value={_user.email}
										placeholder={$i18n.t('Enter Your Email')}
										required
									/>
								</div>
							</div>

							<div class="">
								<label class="text-label text-slate-400">{$i18n.t('Invitation message')}</label>

								<div class="flex-1">
									<Textarea
										placeholder={$i18n.t('Add a short description about what this model does')}
										rows={3}
										bind:value={invitationMessage}
									/>
								</div>

							</div>

							<div class="flex flex-col w-full mt-1">
								<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Password')}</div>

								<div class="flex-1">
									<input
										class="{inputClasses} w-full disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
										type="password"
										bind:value={_user.password}
										placeholder={$i18n.t('Enter Your Password')}
										autocomplete="off"
									/>
								</div>
							</div>
						{:else if tab === 'import'}
							<div>
								<div class="mb-3 w-full">
									<input
										id="upload-user-csv-input"
										hidden
										bind:files={inputFiles}
										type="file"
										accept=".csv"
									/>

									<button
										class="w-full text-sm font-medium py-3 bg-transparent hover:bg-gray-100 border border-dashed dark:border-gray-800 dark:hover:bg-gray-850 text-center rounded-xl"
										type="button"
										on:click={() => {
											document.getElementById('upload-user-csv-input')?.click();
										}}
									>
										{#if inputFiles}
											{inputFiles.length > 0 ? `${inputFiles.length}` : ''} document(s) selected.
										{:else}
											{$i18n.t('Click here to select a csv file.')}
										{/if}
									</button>
								</div>

								<div class=" text-xs text-gray-500">
									ⓘ {$i18n.t(
										'Ensure your CSV file includes 4 columns in this order: Name, Email, Password, Role.'
									)}
									<a
										class="underline dark:text-gray-200"
										href="{WEBUI_BASE_URL}/static/user-import.csv"
									>
										{$i18n.t('Click here to download user import template file.')}
									</a>
								</div>
							</div>
						{/if}
					</div>

					<div class="flex justify-end pt-3 text-sm font-medium">
						<button
							class="px-3.5 py-1.5 text-sm font-medium bg-primary-500 hover:bg-primary-700 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full flex flex-row space-x-1 items-center {loading
								? ' cursor-not-allowed'
								: ''}"
							type="submit"
							disabled={loading}
						>
							{$i18n.t('Save')}

							{#if loading}
								<div class="ml-2 self-center">
									<svg
										class=" w-4 h-4"
										viewBox="0 0 24 24"
										fill="currentColor"
										xmlns="http://www.w3.org/2000/svg"
										><style>
											.spinner_ajPY {
												transform-origin: center;
												animation: spinner_AtaB 0.75s infinite linear;
											}
											@keyframes spinner_AtaB {
												100% {
													transform: rotate(360deg);
												}
											}
										</style><path
											d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
											opacity=".25"
										/><path
											d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
											class="spinner_ajPY"
										/></svg
									>
								</div>
							{/if}
						</button>
					</div>
				</form>
			</div>
		</section>
	</div>
</Modal>

<style>
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		/* display: none; <- Crashes Chrome on hover */
		-webkit-appearance: none;
		margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
	}

	.tabs::-webkit-scrollbar {
		display: none; /* for Chrome, Safari and Opera */
	}

	.tabs {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	input[type='number'] {
		-moz-appearance: textfield; /* Firefox */
	}
</style>
