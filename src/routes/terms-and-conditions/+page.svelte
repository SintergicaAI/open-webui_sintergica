<script>
	import { getContext, onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';

	import { config, socket, user, WEBUI_NAME } from '$lib/stores';


	const i18n = getContext('i18n');

	let isDarkMode = localStorage.getItem('theme');


	const checkDarkMode = () => {
		return document.documentElement.classList.contains('dark');
	}

	let onboarding = false;

	onMount(async () => {
		const observer = new MutationObserver(()=>{
			isDarkMode = checkDarkMode();
		})

		observer.observe(document.documentElement, {
			attributes: true,
			attributeFilter: ['class']
		})

		isDarkMode = checkDarkMode();

		loaded = true;

		onDestroy(()=>{
			observer.disconnect();
		})
	});

</script>
<svelte:head>
	<title>Términos y Condiciones | {`${$WEBUI_NAME}`}</title>
</svelte:head>

<div class="overflow-auto w-full h-screen bg-[#e0e5ec] dark:bg-gray-800">
	<div class="container">
		<h1>Términos y Condiciones</h1>
		<p>Última actualización: 3 de Diciembre de 2024</p>

		<h2>Introducción</h2>
		<p>
			Bienvenido a Sintergica.ai, un sitio web operado por MDA Startup Labs Solutions S.A.P.I. de C.V. (en adelante, “Sintergica”).
			Al acceder y utilizar nuestro sitio web, usted acepta estar sujeto a los siguientes términos y condiciones. Si no está de
			acuerdo con alguno de estos términos, le recomendamos no utilizar este sitio.
		</p>

		<h2>Uso del Sitio</h2>
		<p>
			El uso del sitio web www.sintergica.ai está condicionado al cumplimiento de las siguientes disposiciones:
		</p>
		<ul>
			<li>Usted acepta utilizar este sitio solo con fines lícitos y de manera que no infrinja los derechos de terceros ni limite o impida el uso y disfrute del sitio por parte de otros usuarios.</li>
			<li>El contenido de este sitio es proporcionado “tal cual” y puede estar sujeto a cambios sin previo aviso.</li>
		</ul>

		<h2>Propiedad Intelectual</h2>
		<p>
			Todos los derechos de propiedad intelectual del contenido disponible en este sitio, incluidos textos, imágenes, logotipos,
			gráficos y software, son propiedad de Sintergica o se utilizan con la debida autorización. Queda prohibido:
		</p>
		<ul>
			<li>Reproducir, distribuir o modificar cualquier contenido sin nuestro consentimiento por escrito.</li>
			<li>Utilizar el contenido con fines comerciales no autorizados.</li>
		</ul>

		<h2>Privacidad y Uso de Datos</h2>
		<p>
			El uso de nuestro sitio está sujeto a nuestro Aviso de Privacidad, el cual describe cómo recopilamos, utilizamos y protegemos su información personal. Al utilizar este sitio, usted consiente el uso de sus datos personales conforme a dicho aviso.
		</p>

		<h2>Responsabilidad Limitada</h2>
		<p>
			Sintergica no garantiza que el sitio web funcione sin interrupciones ni errores. En la medida permitida por la ley, no
			asumimos responsabilidad por:
		</p>
		<ul>
			<li>Daños directos, indirectos o consecuentes derivados del uso o incapacidad de uso de este sitio.</li>
			<li>Pérdida de datos o ingresos ocasionada por la utilización del contenido del sitio.</li>
		</ul>

		<h2>Enlaces a Terceros</h2>
		<p>
			Nuestro sitio puede contener enlaces a sitios web de terceros que están fuera de nuestro control. No somos responsables
			del contenido o las prácticas de privacidad de dichos sitios y el acceso a ellos es bajo su propio riesgo.
		</p>

		<h2>Modificaciones</h2>
		<p>
			Sintergica se reserva el derecho de modificar estos términos y condiciones en cualquier momento. Cualquier cambio será
			publicado en esta página, por lo que le recomendamos revisarla periódicamente. El uso continuado del sitio web implica la
			aceptación de dichos cambios.
		</p>

		<h2>Ley Aplicable</h2>
		<p>
			Estos términos y condiciones se rigen por las leyes de los Estados Unidos Mexicanos. En caso de controversia, usted y
			Sintergica aceptan someterse a la jurisdicción de los tribunales competentes en el estado de Veracruz.
		</p>

		<h2>Contacto</h2>
		<p>
			Si tiene alguna pregunta sobre estos términos y condiciones, puede comunicarse con nosotros a través de:
		</p>
		<ul>
			<li>Correo electrónico: <a href="mailto:hola@sintergica.ai">hola@sintergica.ai</a></li>
			<li>Teléfono: 56 5922 7340</li>
		</ul>
	</div>
</div>

<style>
    :root {
        --color-background-light: #e0e5ec;
        --color-background-dark: #1a202c;
        --color-container-light: #ffffff;
        --color-container-dark: #2d3748;
        --color-border-light: #ddd;
        --color-border-dark: #4a5568;
        --color-text-light: #5a5a5a;
        --color-text-dark: #e2e8f0;
        --color-primary: #007bff;
        --shadow-light: rgba(0, 0, 0, 0.1);
        --shadow-dark: rgba(0, 0, 0, 0.4);
    }

    .container {
        max-width: 760px;
        margin: 2rem auto;
        padding: 1.5rem;
        background: var(--color-container-light);
        color: var(--color-text-light);
        border: 1px solid var(--color-border-light);
        border-radius: 10px;
        box-shadow: 0 4px 10px var(--shadow-light);
        transition: all 0.3s ease;
    }

    .dark .container {
        background: var(--color-container-dark);
        color: var(--color-text-dark);
        border: 1px solid var(--color-border-dark);
        box-shadow: 0 4px 10px var(--shadow-dark);
    }

    h1, h2 {
        color: var(--color-text-light);
        margin-bottom: 1rem;
    }

    .dark h1, .dark h2 {
        color: var(--color-text-dark);
    }

    h1 {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1.2rem;
    }

    h2 {
        margin-top: 1.5rem;
        font-size: 1.5rem;
    }

    p {
        margin: 0.8rem 0;
        text-align: justify;
    }

    ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }

    li {
        margin: 0.5rem 0;
    }

    a {
        color: var(--color-primary);
        text-decoration: none;
        transition: color 0.2s ease, text-decoration 0.2s ease;
    }

    a:hover,
    a:focus {
        color: darken(var(--color-primary), 10%);
        text-decoration: underline;
    }

    /* Responsividad */
    @media (max-width: 768px) {
        .container {
            padding: 1rem;
        }

        h1 {
            font-size: 1.6rem;
        }

        h2 {
            font-size: 1.3rem;
        }

        body {
            font-size: 15px;
        }
    }

    @media (max-width: 480px) {
        .container {
            padding: 0.8rem;
        }

        h1 {
            font-size: 1.4rem;
        }

        h2 {
            font-size: 1.2rem;
        }

        body {
            font-size: 14px;
        }
    }
</style>