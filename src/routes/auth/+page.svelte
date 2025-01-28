<script>
	import { toast } from 'svelte-sonner';

	import { getContext, onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { getBackendConfig } from '$lib/apis';
	import { getSessionUser, ldapUserSignIn, userSignIn, userSignUp } from '$lib/apis/auths';

	import { WEBUI_BASE_URL } from '$lib/constants';
	import { config, socket, user, WEBUI_NAME } from '$lib/stores';

	import { generateInitialsImage } from '$lib/utils';
	import OnBoarding from '$lib/components/OnBoarding.svelte';
	import Carousel from '$lib/components/common/Carousel.svelte';


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




	const checkDarkMode = () => {
		return document.documentElement.classList.contains('dark');
	}

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
	}

	window.addEventListener('beforeinstallprompt', (e) => {
		e.preventDefault();
		installPromptEvent = e;
		showInstallButton = true;
	})

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

		const observer = new MutationObserver(()=>{
			isDarkMode = checkDarkMode();
			updateVideoSrc()
		})

		observer.observe(document.documentElement, {
			attributes: true,
			attributeFilter: ['class']
		})

		isDarkMode = checkDarkMode();
		updateVideoSrc();
		await checkOauthCallback();

		loaded = true;
		if (($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false) {
			await signInHandler();
		} else {
			onboarding = $config?.onboarding ?? false;
		}

		onDestroy(()=>{
			observer.disconnect();
		})
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
		'/assets/images/slides_vertical_4.jpg',
	];

	const horizontalSlides = [
		'/assets/images/slides_horizontal_1.jpg',
		'/assets/images/slides_horizontal_2.jpg',
		'/assets/images/slides_horizontal_3.jpg',
	]
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

<div class="w-full h-screen max-h-[100dvh] text-white relative">
	<div
		class="w-full h-full absolute top-0 left-0 dark:from-gray-900 dark:to-gray-800"></div>

	{#if loaded}
		<div class="fixed top-5 left-5 z-50">
			<div class="flex space-x-2 items-center">
				<img
					crossorigin="anonymous"
					src="/static/favicon.png"
					class="w-8 rounded-full"
					alt="logo"
				/>
				<span class="text-xl font-bold text-gray-700 dark:text-white">
					{$WEBUI_NAME}
				</span>
			</div>
		</div>

		<div class="flex justify-center items-center h-screen dark:bg-[#14171B]">
				<div class="w-full h-full relative z-999 bg-[#e0e5ec] dark:bg-gray-800 dark:shadow-lg bg-opacity-90 neumorphic flex">
				<div class="w-full sm:w-2/3 min-h-[600px] flex flex-col justify-center items-center">
					<h2 class="text-2xl font-bold text-gray-700 dark:text-white mb-4">
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

					<form
						class="flex flex-col space-y-4"
						on:submit={(e) => {
					e.preventDefault();
					submitHandler();
				}}
					>
						{#if mode === 'signup'}
							<div>

								<label class="block text-sm font-medium text-gray-600">{$i18n.t('Name')}</label>
								<input
									bind:value={name}
									type="text"
									class="mt-1 w-full p-3 bg-white rounded-md neumorphic-inner neumorphic focus:outline-none"
									placeholder={$i18n.t('Enter Your Full Name')}
									required
								/>
							</div>
						{/if}


						{#if mode === 'ldap'}
							<div>
								<label
									class="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">{$i18n.t('Username')}</label>
								<input
									bind:value={ldapUsername}
									type="text"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
									required
								/>
							</div>
						{:else}
							<div>
								<label
									class="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">{$i18n.t('Email')}</label>
								<input
									bind:value={email}
									type="email"
									class="w-full px-3 py-2 border text-gray-600 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
									required
									placeholder={$i18n.t('user@example.com')}
								/>
							</div>
						{/if}

						<div>
							<label
								class="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">{$i18n.t('Password')}</label>
							<input
								bind:value={password}
								type="password"
								class="w-full px-3 py-2 border text-gray-600 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
								required
								placeholder={$i18n.t('Enter you password')}
							/>
						</div>

						<button
							class="bg-primary-500 hover:bg-primary-700 text-white py-2 px-4 rounded-lg font-medium transition dark:bg-blue-600 dark:hover:bg-blue-700"
							type="submit"
						>
							{mode === 'signin'
								? $i18n.t('Sign in')
								: ($config?.onboarding ?? false)
									? $i18n.t('Create Admin Account')
									: $i18n.t('Create Account')}
						</button>

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
					</form>

					<div class="text-sm text-gray-600 dark:text-gray-300 text-center mt-4">
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
						<span class="mx-2">|</span>
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
					</div>
				</div>

				<div class="hidden sm:w-1/2 md:1/3 min-h-[100vh] bg-[#f0f2f5] dark:bg-[#14171B] sm:flex">
					<Carousel slides={slides} autoplay={true} interval={5000} showArrows={true} showDots={true}/>
				</div>

			</div>

		</div>
	{/if}
</div>