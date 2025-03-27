<script>
	import { toast } from 'svelte-sonner';

	import { getContext, onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { getBackendConfig } from '$lib/apis';
	import { getSessionUser, ldapUserSignIn, userSignIn, userSignUp } from '$lib/apis/auths';

	import { WEBUI_BASE_URL } from '$lib/constants';
	import { config, mobile, socket, user, WEBUI_NAME } from '$lib/stores';

	import { generateInitialsImage } from '$lib/utils';
	import OnBoarding from '$lib/components/OnBoarding.svelte';
	import TextInput from '$lib/components/common/Input/TextInput.svelte';
	import { Eye, EyeClosed, LucideMail } from 'lucide-svelte';
	import Button from '$lib/components/common/Button/Button.svelte';
	import TuringFace from '$lib/components/icons/TuringFace.svelte';


	const i18n = getContext('i18n');

	let loaded = false;

	let mode = $config?.features.enable_ldap ? 'ldap' : 'signin';

	let name = '';
	let email = '';
	let password = '';

	let ldapUsername = '';

	let isDarkMode = localStorage.getItem('theme');
	let videoSrc = '';

	let installPromptEvent = null;
	let showInstallButton = false;


	// Add these new variables to capture the input
	let firstName = '';
	let lastName = '';

	// Update the `name` variable to compute its value based on `firstName` and `lastName`
	$: name = `${firstName.trim()} ${lastName.trim()}`.trim();


	const checkDarkMode = () => {
		return document.documentElement.classList.contains('dark');
	};

	const installApp = async () => {
		if (installPromptEvent) {
			installPromptEvent.prompt();
			const choiceResult = await installPromptEvent.userChoice;
			if (choiceResult.outcome === 'accepted') {
				console.log('User accepted the A2HS prompt');
			} else {
				console.log('User dismissed the A2HS prompt');
			}
			installPromptEvent = null;
			showInstallButton = false;
		}
	};

	window.addEventListener('beforeinstallprompt', (e) => {
		e.preventDefault();
		installPromptEvent = e;
		showInstallButton = true;
	});

	const setSessionUser = async (sessionUser) => {
		if (sessionUser) {
			console.log(sessionUser);
			toast.success($i18n.t(`You're now logged in.`));
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}

			$socket.emit('user-join', { auth: { token: sessionUser.token } });
			await user.set(sessionUser);
			await config.set(await getBackendConfig());
			goto('/');
		}
	};

	const signInHandler = async () => {
		const sessionUser = await userSignIn(email, password).catch((error) => {
			toast.error(error);
			return null;
		});

		await setSessionUser(sessionUser);
	};

	const signUpHandler = async () => {
		const sessionUser = await userSignUp(name, email, password, generateInitialsImage(name)).catch(
			(error) => {
				toast.error(error);
				return null;
			}
		);

		await setSessionUser(sessionUser);
	};

	const ldapSignInHandler = async () => {
		const sessionUser = await ldapUserSignIn(ldapUsername, password).catch((error) => {
			toast.error(error);
			return null;
		});
		await setSessionUser(sessionUser);
	};

	const submitHandler = async () => {
		if (mode === 'ldap') {
			await ldapSignInHandler();
		} else if (mode === 'signin') {
			await signInHandler();
		} else {
			await signUpHandler();
		}
	};

	const checkOauthCallback = async () => {
		if (!$page.url.hash) {
			return;
		}
		const hash = $page.url.hash.substring(1);
		if (!hash) {
			return;
		}
		const params = new URLSearchParams(hash);
		const token = params.get('token');
		if (!token) {
			return;
		}
		const sessionUser = await getSessionUser(token).catch((error) => {
			toast.error(error);
			return null;
		});
		if (!sessionUser) {
			return;
		}
		localStorage.token = token;
		await setSessionUser(sessionUser);
	};

	let onboarding = false;

	onMount(async () => {
		if ($user !== undefined) {
			await goto('/');
		}

		const observer = new MutationObserver(() => {
			isDarkMode = checkDarkMode();
			updateVideoSrc();
		});

		observer.observe(document.documentElement, {
			attributes: true,
			attributeFilter: ['class']
		});

		isDarkMode = checkDarkMode();
		updateVideoSrc();
		await checkOauthCallback();

		loaded = true;
		if (($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false) {
			await signInHandler();
		} else {
			onboarding = $config?.onboarding ?? false;
		}

		onDestroy(() => {
			observer.disconnect();
		});
	});
	const updateVideoSrc = () => {
		videoSrc = isDarkMode
			? `${WEBUI_BASE_URL}/static/2.0.mp4`
			: `${WEBUI_BASE_URL}/static/1.0.mp4`;
	};

	const slides = [
		'/assets/images/slides_vertical_1.jpg',
		'/assets/images/slides_vertical_2.jpg',
		'/assets/images/slides_vertical_3.jpg',
		'/assets/images/slides_vertical_4.jpg'
	];

	const horizontalSlides = [
		'/assets/images/slides_horizontal_1.jpg',
		'/assets/images/slides_horizontal_2.jpg',
		'/assets/images/slides_horizontal_3.jpg'
	];
</script>

<svelte:head>
	<title>
		{`${$WEBUI_NAME}`}
	</title>
</svelte:head>

<OnBoarding
	bind:show={onboarding}
	getStartedHandler={() => {
		onboarding = false;
		mode = $config?.features.enable_ldap ? 'ldap' : 'signup';
	}}
/>

<div class="p-sm flex w-full h-screen max-h-[100dvh] bg-slate-50 dark:bg-slate-950 text-black dark:text-white relative">
	{#if loaded}
	<div class="flex w-full md:w-2/4 lg:w-[33%] h-screen p-8">
		{#if !$mobile}
			<div class="fixed top-5 left-8">
				<div class="flex space-x-3 items-center">
					<img
						crossorigin="anonymous"
						src="/static/favicon.png"
						class="w-9 h-9 rounded-sm"
						alt="logo"
					/>
					<span class="text-[2rem] font-bold font-[Archivo] text-black dark:text-white">
						{$WEBUI_NAME}
					</span>
				</div>
			</div>
		{/if}
		<div class="mx-auto sm:m-auto">
			{#if $mobile}
				<div class=" z-50 top-10 left-10 mb-base">
					<div class="flex space-x-3 items-center">
						<img
							crossorigin="anonymous"
							src="/static/favicon.png"
							class="w-9 h-9 rounded-sm"
							alt="logo"
						/>
						<span class="text-[2rem] font-bold font-[Archivo] text-black dark:text-white">
							{$WEBUI_NAME}
						</span>
					</div>
				</div>
			{/if}
			<h2 class="font-bold text-title text-black dark:text-white mb-2">
				{#if $config?.onboarding ?? false}
					{$i18n.t(`Get started with {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
				{:else if mode === 'ldap'}
					{$i18n.t(`Sign in to {{WEBUI_NAME}} with LDAP`, { WEBUI_NAME: $WEBUI_NAME })}
				{:else if mode === 'signin'}
					{$i18n.t(`Sign in to {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
				{:else}
					{$i18n.t(`Sign up to {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
				{/if}
			</h2>
			<p class="mb-8">Inicia sesión con tus credenciales para continuar</p>
			<form
				class="mb-10"
				on:submit={(e) => {
					e.preventDefault();
					submitHandler();
				}}
			>
				{#if mode === 'signup'}
					<div class="mb-4">
						<!--								<label class="block text-sm font-medium text-gray-600">{$i18n.t('Name')}</label>-->
						<!--								<input-->
						<!--									bind:value={name}-->
						<!--									type="text"-->
						<!--									class="mt-1 w-full p-3 bg-white rounded-md neumorphic-inner neumorphic focus:outline-none"-->
						<!--									placeholder={$i18n.t('Enter Your Full Name')}-->
						<!--									required-->
						<!--								/>-->
						<TextInput id="firstName" bind:value={firstName} on:input={(e)=>console.log(e.detail.value)}
											 label={$i18n.t('Name')}/>
						<TextInput id="lastname" bind:value={lastName} on:input={(e)=>console.log(e.detail.value)}
											 label={$i18n.t('Last name')} />
					</div>
				{/if}
				{#if mode === 'ldap'}
					<div class="mb-4">
						<label
							for="username"
							class="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">{$i18n.t('Username')}
						</label>
						<input
							id="username"
							bind:value={ldapUsername}
							type="text"
							class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
							required
						/>
					</div>
				{:else}
					<div class="mb-4">
						<TextInput id="email" type="email" placeholder={$i18n.t('user@example.com')} bind:value={email}
											 required={true} icon={LucideMail} on:input={(e)=>console.log(e.detail.value)}
											 label={$i18n.t('Email')} />
					</div>

					<div class="mb-4">
						<TextInput id="password" type="password" icon={Eye} hidePasswordIcon={EyeClosed} showPasswordIcon={Eye} placeholder={$i18n.t('Enter you password')}
											 bind:value={password} on:input={(e)=>console.log(e.detail.value)} label={$i18n.t('Password')}
											 required />
					</div>

					<div class="mb-4">
						<a href="/forgot-password" class="text-blue-500">¿Olvidaste tu contraseña?</a>
					</div>

					<div class="w-full">
						<Button type="submit" variant="primary" size="base" buttonClasses="w-full">{mode === 'signin'
							? $i18n.t('Sign in')
							: ($config?.onboarding ?? false)
								? $i18n.t('Create Admin Account')
								: $i18n.t('Create Account')}
						</Button>
					</div>

					{#if $config?.features.enable_signup && !($config?.onboarding ?? false)}
						<div class="text-sm text-gray-600 dark:text-gray-300 text-center mt-4">
							{mode === 'signin'
								? $i18n.t("Don't have an account?")
								: $i18n.t('Already have an account?')}
							<button
								class="font-medium text-blue-500 underline hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-600 ml-1"
								type="button"
								on:click={() => {
										if (mode === 'signin') {
											mode = 'signup';
										} else {
											mode = 'signin';
										}
									}}
							>
								{mode === 'signin' ? $i18n.t('Sign up') : $i18n.t('Sign in')}
							</button>
						</div>
					{/if}
				{/if}
			</form>
			<section class="mt-4">
				<a
					href="/terms-and-conditions"
					class="font-medium text-blue-500 underline hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-600 ml-2"
					rel="noopener noreferrer"
					on:click={async () => {
								await goto('/terms-and-conditions');
							}}
				>
					{$i18n.t('Terms and conditions')}
				</a>
				<span class="mx-2 text-slate-500">|</span>
				<a
					href="/privacy-policy"
					class="font-medium text-blue-500 underline hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-600 mr-2"
					rel="noopener noreferrer"
					on:click={async ()=> {
								await goto('/privacy-policy')
							}}
				>
					{$i18n.t('Privacy policy')}
				</a>
			</section>
		</div>
	</div>
	{#if !$mobile}
		<article class=" md:w-2/4 lg:w-[69%] rounded-lg h-full flex justify-center items-center bg-brand-500 dark:bg-brand-900">
			<div class="inline-block mx-auto text-white dark:text-brand-700">
				<svg xmlns="http://www.w3.org/2000/svg" width="376" height="333" viewBox="0 0 376 333" fill="currentColor" class="fill-current">
					<path fill-rule="evenodd" clip-rule="evenodd" d="M5.81424 8.98956C13.7652 -0.551581 27.9453 -1.84068 37.4865 6.11026L127.438 81.0703C132.889 85.6124 135.876 92.4605 135.498 99.5456C135.119 106.631 131.42 113.121 125.516 117.057L35.5641 177.025C25.2302 183.914 11.2681 181.122 4.37885 170.788C-2.5104 160.454 0.28202 146.492 10.6159 139.603L75.5086 96.341L8.69353 40.6618C-0.847606 32.7108 -2.13671 18.5307 5.81424 8.98956ZM285.449 143.319C310.289 143.319 330.425 123.182 330.425 98.3426C330.425 73.503 310.289 53.3666 285.449 53.3666C260.61 53.3666 240.473 73.503 240.473 98.3426C240.473 123.182 260.61 143.319 285.449 143.319ZM285.449 188.295C335.128 188.295 375.401 148.022 375.401 98.3426C375.401 48.6635 335.128 8.39061 285.449 8.39061C235.77 8.39061 195.497 48.6635 195.497 98.3426C195.497 148.022 235.77 188.295 285.449 188.295ZM100.134 248.621C92.0514 239.191 77.8547 238.099 68.4249 246.182C58.9951 254.264 57.9031 268.461 65.9858 277.891C83.3428 298.141 114.971 322.682 154.71 329.975C196.258 337.6 243.18 325.683 286.939 278.558C295.39 269.457 294.863 255.228 285.762 246.777C276.661 238.326 262.432 238.853 253.981 247.954C219.782 284.784 187.995 290.357 162.829 285.738C135.854 280.788 112.761 263.352 100.134 248.621Z" fill="currentColor"/>
				</svg>
			</div>
		</article>
	{/if}
	{/if}
</div>