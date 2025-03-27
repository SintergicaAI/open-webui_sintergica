<script lang="ts">
	import { writable } from 'svelte/store';
	import { DropdownMenu, Select } from 'bits-ui';
	const dropdownOpen = writable(false);
	import { fly } from "svelte/transition";

	import { toast } from 'svelte-sonner';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { getLanguages } from '$lib/i18n';
	const dispatch = createEventDispatcher();

	import { models, settings, theme, user } from '$lib/stores';

	const i18n = getContext('i18n');

	import AdvancedParams from './Advanced/AdvancedParams.svelte';
	import { Check, ChevronDown, ChevronsDown, CircleCheckBig } from 'lucide-svelte';
	import { flyAndScale } from '$lib/utils/transitions';
	import Switch from '$lib/components/chat/Switch.svelte';
	export let saveSettings: Function;
	export let getModels: Function;

	// General
	let themes = ['dark', 'light'];
	let themesRefactored = [
		{value: 'dark', label: 'Dark'},
		{value: 'light', label: 'Light'},
	]
	let selectedTheme = 'system';
	let selectedLanguage: string | null = null;

	let languages: Awaited<ReturnType<typeof getLanguages>> = [];
	let lang = $i18n.language;
	let notificationEnabled = false;
	let system = '';

	let showAdvanced = false;

	const toggleNotification = async () => {
		const permission = await Notification.requestPermission();

		if (permission === 'granted') {
			notificationEnabled = !notificationEnabled;
			saveSettings({ notificationEnabled: notificationEnabled });
		} else {
			toast.error(
				$i18n.t(
					'Response notifications cannot be activated as the website permissions have been denied. Please visit your browser settings to grant the necessary access.'
				)
			);
		}
	};

	let knowledgeColor = '';

	// Advanced
	let requestFormat = '';
	let keepAlive: string | null = null;

	let params = {
		// Advanced
		stream_response: null,
		seed: null,
		temperature: null,
		frequency_penalty: null,
		repeat_last_n: null,
		mirostat: null,
		mirostat_eta: null,
		mirostat_tau: null,
		top_k: null,
		top_p: null,
		min_p: null,
		stop: null,
		tfs_z: null,
		num_ctx: null,
		num_batch: null,
		num_keep: null,
		max_tokens: null,
		num_gpu: null
	};

	const toggleRequestFormat = async () => {
		if (requestFormat === '') {
			requestFormat = 'json';
		} else {
			requestFormat = '';
		}

		saveSettings({ requestFormat: requestFormat !== '' ? requestFormat : undefined });
	};

	const colorChangeHandler = (color) => {
		 saveSettings({ knowledgeColor: color });
	}

	onMount(async () => {
		selectedTheme = localStorage.theme ?? 'system';

		languages = await getLanguages();

		notificationEnabled = $settings.notificationEnabled ?? false;
		system = $settings.system ?? '';

		requestFormat = $settings.requestFormat ?? '';
		keepAlive = $settings.keepAlive ?? null;

		params = { ...params, ...$settings.params };
		params.stop = $settings?.params?.stop ? ($settings?.params?.stop ?? []).join(',') : null;
	});

	const changeLanguage = (code: string) => {
		$i18n.changeLanguage(code);
	}

	const applyTheme = (_theme: string) => {
		let themeToApply = _theme === 'oled-dark' ? 'dark' : _theme;

		if (_theme === 'system') {
			themeToApply = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
		}

		if (themeToApply === 'dark' && !_theme.includes('oled')) {
			document.documentElement.style.setProperty('--color-gray-800', '#333');
			document.documentElement.style.setProperty('--color-gray-850', '#262626');
			document.documentElement.style.setProperty('--color-gray-900', '#171717');
			document.documentElement.style.setProperty('--color-gray-950', '#0d0d0d');
		}

		themes
			.filter((e) => e !== themeToApply)
			.forEach((e) => {
				e.split(' ').forEach((e) => {
					document.documentElement.classList.remove(e);
				});
			});

		themeToApply.split(' ').forEach((e) => {
			document.documentElement.classList.add(e);
		});

		const metaThemeColor = document.querySelector('meta[name="theme-color"]');
		if (metaThemeColor) {
			if (_theme.includes('system')) {
				const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
					? 'dark'
					: 'light';
				console.log('Setting system meta theme color: ' + systemTheme);
				metaThemeColor.setAttribute('content', systemTheme === 'light' ? '#ffffff' : '#171717');
			} else {
				console.log('Setting meta theme color: ' + _theme);
				metaThemeColor.setAttribute(
					'content',
					_theme === 'dark'
						? '#171717'
						: _theme === 'oled-dark'
							? '#000000'
							: _theme === 'her'
								? '#983724'
								: '#ffffff'
				);
			}
		}

		console.log(_theme);
	};

	const themeChangeHandler = (_theme: string) => {
		theme.set(_theme);
		localStorage.setItem('theme', _theme);
		if (_theme.includes('oled')) {
			document.documentElement.style.setProperty('--color-gray-800', '#101010');
			document.documentElement.style.setProperty('--color-gray-850', '#050505');
			document.documentElement.style.setProperty('--color-gray-900', '#000000');
			document.documentElement.style.setProperty('--color-gray-950', '#000000');
			document.documentElement.classList.add('dark');
		}
		applyTheme(_theme);
		dropdownOpen.set(false); // Cierra el dropdown al seleccionar.

	};

</script>

<div class="flex flex-col h-full justify-between text-sm">
	<div class=" overflow-y-scroll max-h-[28rem] lg:max-h-full">
		<!-- Tab Content -->
		<div class="flex flex-col gap-sm md:gap-lg">
			<div class="flex w-full justify-between">
<!--				<div class=" self-center text-xs font-medium">{$i18n.t('Theme')}</div>-->
				<div class=" self-center text-slate-950 dark:text-white">{$i18n.t('Appearance')}</div>

				<Select.Root items={themesRefactored} onSelectedChange={({value})=>{themeChangeHandler(value)}}>
					<Select.Trigger
						class=" dark:text-white inline-flex h-input w-[296px] items-center rounded-sm bg-background px-base py-sm text-sm transition-colors
						 focus:outline-none focus:ring-2 focus:ring-foreground focus:ring-offset-2 focus:ring-offset-background"
						aria-label="Select a theme"
					>
						<Select.Value class="text-sm dark:text-slate-500" placeholder="Select a theme" />
						<ChevronDown class="w-5 h-5 ml-auto dark:text-slate-500" />
					</Select.Trigger>
					<Select.Content
						class="z-50 bg-white dark:bg-slate-800 dark:text-white w-full rounded-xl p-base outline-none relative"
						sideOffset={8}
						transition={flyAndScale}
					>
						{#each themesRefactored as theme}
							<Select.Item
								class=" flex h-10 w-full select-none items-center rounded-button p-base text-sm outline-none transition-all duration-75 data-[highlighted]:bg-muted"
								value={theme.value}
								label={theme.label}
							>
								<span class=" flex-1 text-base dark:text-white hover:text-brand-500 dark:hover:text-brand-500 text-slate-950 line-clamp-1 overflow-hidden">{theme.label}</span>
								<Select.ItemIndicator class="ml-auto text-brand-500" asChild={false}>
									<CircleCheckBig size="20"/>
								</Select.ItemIndicator>
							</Select.Item>
						{/each}
					</Select.Content>
					<Select.Input name="theme" />
				</Select.Root>
<!--				<div class="flex items-center ">-->
<!--&lt;!&ndash;					<button&ndash;&gt;-->
<!--&lt;!&ndash;						class="dropdown-button dark:bg-gray-900 w-fit pr-8 rounded py-2 px-2 text-xs bg-transparent outline-none text-right"&ndash;&gt;-->
<!--&lt;!&ndash;						on:click={() => dropdownOpen.update(open => !open)}&ndash;&gt;-->
<!--&lt;!&ndash;					>&ndash;&gt;-->
<!--&lt;!&ndash;						{selectedTheme} ▼&ndash;&gt;-->
<!--&lt;!&ndash;					</button>&ndash;&gt;-->

<!--&lt;!&ndash;					{#if $dropdownOpen}&ndash;&gt;-->
<!--&lt;!&ndash;						<ul&ndash;&gt;-->
<!--&lt;!&ndash;							class="dropdown-menu absolute right-0 z-10 bg-white dark:bg-gray-900 shadow-md rounded-md w-40 border"&ndash;&gt;-->
<!--&lt;!&ndash;						>&ndash;&gt;-->
<!--&lt;!&ndash;							{#each themesRefactored as theme}&ndash;&gt;-->
<!--&lt;!&ndash;								<li&ndash;&gt;-->
<!--&lt;!&ndash;									class="dropdown-item py-2 px-4 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"&ndash;&gt;-->
<!--&lt;!&ndash;									on:click={() => themeChangeHandler(theme.value)}&ndash;&gt;-->
<!--&lt;!&ndash;								>&ndash;&gt;-->
<!--&lt;!&ndash;									{theme.label}&ndash;&gt;-->
<!--&lt;!&ndash;								</li>&ndash;&gt;-->
<!--&lt;!&ndash;							{/each}&ndash;&gt;-->
<!--&lt;!&ndash;						</ul>&ndash;&gt;-->
<!--&lt;!&ndash;					{/if}&ndash;&gt;-->
<!--					<select-->
<!--						class=" dark:bg-gray-900 w-fit pr-8 rounded py-2 px-2 text-xs bg-transparent outline-none text-right"-->
<!--						bind:value={selectedTheme}-->
<!--						placeholder="Select a theme"-->
<!--						on:change={() => themeChangeHandler(selectedTheme)}-->
<!--					>-->
<!--						<option value="system">⚙️ {$i18n.t('System')}</option>-->
<!--						<option value="dark">🌑 {$i18n.t('Dark')}</option>-->
<!--						<option value="light">☀️ {$i18n.t('Light')}</option>-->
<!--					</select>-->
<!--				</div>-->
			</div>

			<hr class=" border-slate-300 dark:border-slate-700" />

			<div class=" flex w-full justify-between">
				<div class=" self-center text-xs font-medium">{$i18n.t('Language')}</div>

				<Select.Root preventScroll={false} items={languages} onSelectedChange={({ value }) => changeLanguage(value)}>
					<Select.Trigger
						class="dark:text-white inline-flex h-input w-[296px] items-center rounded-sm bg-background px-base py-sm text-sm transition-colors
					focus:outline-none focus:ring-2 focus:ring-foreground focus:ring-offset-2 focus:ring-offset-background"
						aria-label="Select a language"
					>
						<Select.Value
							class="text-sm dark:text-slate-500"
							placeholder={$i18n.t('Select a Language')}
						/>
					</Select.Trigger>
					<Select.Content
						class="z-50 bg-white dark:bg-slate-800 dark:text-white w-full rounded-xl p-base outline-none relative max-h-64 overflow-y-auto"
					>
						{#each languages as language}
							<Select.Item
								class="flex h-10 w-full select-none items-center rounded-sm px-base text-sm transition-all duration-75"
								value={language.code}
								label={language.title}
							>
						<span class="flex-1 text-base dark:text-white hover:text-brand-500 dark:hover:text-brand-500 overflow-hidden text-ellipsis">
							{language.title}
						</span>
							</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</div>

			<hr class=" border-slate-300 dark:border-slate-700" />

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs font-medium">{$i18n.t('Notifications')}</div>
					<Switch on:change={toggleNotification} />
				</div>
			</div>

			<div>
				<div class=" py-0.5 flex w-full justify-between">
					<div class=" self-center text-xs">{$i18n.t('Change knowledge color')}</div>

					<select
						class=" dark:bg-gray-900 w-fit pr-8 rounded py-2 px-2 text-xs bg-transparent outline-none text-right"
						bind:value={knowledgeColor}
						placeholder="Select a theme"
						on:change={() => colorChangeHandler(knowledgeColor)}
					>
						<option value="blue">⚙️ {$i18n.t('System')}</option>
						<option value="cyan">🌑 {$i18n.t('Dark')}</option>
						<option value="green">☀️ {$i18n.t('Light')}</option>
					</select>

				</div>
			</div>
		</div>
		<div>
			<div class=" my-2.5 text-sm font-medium">{$i18n.t('System Prompt')}</div>
			<textarea
				bind:value={system}
				class="w-full rounded-lg p-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none resize-none"
				rows="4"
			/>
		</div>

		<div class="mt-2 space-y-3 pr-1.5">
			<div class="flex justify-between items-center text-sm">
				<div class="  font-medium">{$i18n.t('Advanced Parameters')}</div>
				<button
					class=" text-xs font-medium text-gray-500"
					type="button"
					on:click={() => {
						showAdvanced = !showAdvanced;
					}}>{showAdvanced ? $i18n.t('Hide') : $i18n.t('Show')}</button
				>
			</div>

			{#if showAdvanced}
				<AdvancedParams admin={$user?.role === 'admin'} bind:params />
				<hr class=" dark:border-gray-850" />

				<div class=" py-1 w-full justify-between">
					<div class="flex w-full justify-between">
						<div class=" self-center text-xs font-medium">{$i18n.t('Keep Alive')}</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							type="button"
							on:click={() => {
								keepAlive = keepAlive === null ? '5m' : null;
							}}
						>
							{#if keepAlive === null}
								<span class="ml-2 self-center"> {$i18n.t('Default')} </span>
							{:else}
								<span class="ml-2 self-center"> {$i18n.t('Custom')} </span>
							{/if}
						</button>
					</div>

					{#if keepAlive !== null}
						<div class="flex mt-1 space-x-2">
							<input
								class="w-full rounded-lg py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
								type="text"
								placeholder={$i18n.t("e.g. '30s','10m'. Valid time units are 's', 'm', 'h'.")}
								bind:value={keepAlive}
							/>
						</div>
					{/if}
				</div>

				<div>
					<div class=" py-1 flex w-full justify-between">
						<div class=" self-center text-sm font-medium">{$i18n.t('Request Mode')}</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							on:click={() => {
								toggleRequestFormat();
							}}
						>
							{#if requestFormat === ''}
								<span class="ml-2 self-center"> {$i18n.t('Default')} </span>
							{:else if requestFormat === 'json'}
								<!-- <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            class="w-4 h-4 self-center"
                        >
                            <path
                                d="M10 2a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0110 2zM10 15a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0110 15zM10 7a3 3 0 100 6 3 3 0 000-6zM15.657 5.404a.75.75 0 10-1.06-1.06l-1.061 1.06a.75.75 0 001.06 1.06l1.06-1.06zM6.464 14.596a.75.75 0 10-1.06-1.06l-1.06 1.06a.75.75 0 001.06 1.06l1.06-1.06zM18 10a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 0118 10zM5 10a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 015 10zM14.596 15.657a.75.75 0 001.06-1.06l-1.06-1.061a.75.75 0 10-1.06 1.06l1.06 1.06zM5.404 6.464a.75.75 0 001.06-1.06l-1.06-1.06a.75.75 0 10-1.061 1.06l1.06 1.06z"
                            />
                        </svg> -->
								<span class="ml-2 self-center"> {$i18n.t('JSON')} </span>
							{/if}
						</button>
					</div>
				</div>
			{/if}
		</div>
	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class="px-3.5 py-1.5 text-sm font-medium bg-primary-500 hover:bg-primary-700 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
			on:click={() => {
				saveSettings({
					system: system !== '' ? system : undefined,
					params: {
						stream_response: params.stream_response !== null ? params.stream_response : undefined,
						seed: (params.seed !== null ? params.seed : undefined) ?? undefined,
						stop: params.stop ? params.stop.split(',').filter((e) => e) : undefined,
						temperature: params.temperature !== null ? params.temperature : undefined,
						frequency_penalty:
							params.frequency_penalty !== null ? params.frequency_penalty : undefined,
						repeat_last_n: params.repeat_last_n !== null ? params.repeat_last_n : undefined,
						mirostat: params.mirostat !== null ? params.mirostat : undefined,
						mirostat_eta: params.mirostat_eta !== null ? params.mirostat_eta : undefined,
						mirostat_tau: params.mirostat_tau !== null ? params.mirostat_tau : undefined,
						top_k: params.top_k !== null ? params.top_k : undefined,
						top_p: params.top_p !== null ? params.top_p : undefined,
						min_p: params.min_p !== null ? params.min_p : undefined,
						tfs_z: params.tfs_z !== null ? params.tfs_z : undefined,
						num_ctx: params.num_ctx !== null ? params.num_ctx : undefined,
						num_batch: params.num_batch !== null ? params.num_batch : undefined,
						num_keep: params.num_keep !== null ? params.num_keep : undefined,
						max_tokens: params.max_tokens !== null ? params.max_tokens : undefined,
						use_mmap: params.use_mmap !== null ? params.use_mmap : undefined,
						use_mlock: params.use_mlock !== null ? params.use_mlock : undefined,
						num_thread: params.num_thread !== null ? params.num_thread : undefined,
						num_gpu: params.num_gpu !== null ? params.num_gpu : undefined
					},
					keepAlive: keepAlive ? (isNaN(keepAlive) ? keepAlive : parseInt(keepAlive)) : undefined
				});
				dispatch('save');
			}}
		>
			{$i18n.t('Save')}
		</button>
	</div>
</div>

<style>
    .dropdown-button {
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-width: 120px;
        cursor: pointer;
    }

    .dropdown-menu {
        max-height: 200px;
        overflow-y: auto;
    }

    .dropdown-item {
        list-style: none;
    }
</style>
