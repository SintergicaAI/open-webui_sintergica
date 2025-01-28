<script>
	import { WEBUI_NAME } from '$lib/stores';
</script>
<svelte:head>
	<title>Aviso de privacidad | {`${$WEBUI_NAME}`}</title>
</svelte:head>

<div class="overflow-auto w-full h-screen bg-[#e0e5ec] dark:bg-gray-800">
	<div class="container">
		<h1>Aviso de Privacidad</h1>
		<p>Última actualización: 3 de Diciembre de 2024</p>

		<h2>Finalidades Secundarias</h2>
		<p>
			Asimismo, sus datos podrán ser utilizados para las siguientes finalidades secundarias:
		</p>
		<ul>
			<li>Generar estadísticas y análisis para optimizar la experiencia de nuestros clientes.</li>
			<li>Entrenar modelos de inteligencia artificial destinados a mejorar la atención y los servicios proporcionados.</li>
			<li>Enviarle información promocional, publicitaria y de mercadotecnia, siempre que usted lo autorice.</li>
		</ul>

		<h2>Datos Recabados</h2>
		<p>Para cumplir con las finalidades descritas, podríamos recabar datos como:</p>
		<ul>
			<li>Nombre completo</li>
			<li>Correo electrónico</li>
			<li>Número telefónico</li>
			<li>Información proporcionada a través de formularios en nuestro sitio web u otros medios de contacto</li>
		</ul>
		<p>
			No recabamos datos personales sensibles salvo cuando sea estrictamente necesario y con su consentimiento explícito.
		</p>

		<h2>Transferencia de Datos</h2>
		<p>
			Sus datos personales no serán transferidos a terceros sin su consentimiento, salvo en los casos excepcionales previstos por la ley, tales como solicitudes de autoridades competentes o cumplimiento de obligaciones legales.
		</p>

		<h2>Derechos ARCO</h2>
		<p>
			Usted tiene derecho a acceder, rectificar, cancelar u oponerse (ARCO) al tratamiento de sus datos personales. Para ejercer estos derechos, puede enviar una solicitud al correo <a href="mailto:hola@sintergica.ai">hola@sintergica.ai</a>, indicando:
		</p>
		<ul>
			<li>Su nombre completo.</li>
			<li>Descripción clara de los datos sobre los que desea ejercer sus derechos.</li>
			<li>Cualquier documento o información adicional que facilite la localización de sus datos.</li>
		</ul>
		<p>
			Atenderemos su solicitud en un plazo máximo de 20 días hábiles a partir de su recepción.
		</p>

		<h2>Uso de Datos para Entrenamiento de Modelos de IA</h2>
		<p>
			Es importante señalar que parte de la información recabada podrá ser utilizada para entrenar y mejorar modelos de inteligencia artificial. Esta información será procesada de manera anónima y conforme a altos estándares de seguridad para garantizar la protección de su privacidad.
		</p>

		<h2>Modificaciones al Aviso de Privacidad</h2>
		<p>
			Nos reservamos el derecho de actualizar este aviso de privacidad para reflejar cambios en nuestras prácticas o en la legislación aplicable. Cualquier modificación será publicada en nuestro sitio web <a href="https://www.sintergica.ai">www.sintergica.ai</a>.
		</p>

		<h2>Contacto</h2>
		<p>
			Si tiene dudas sobre este aviso de privacidad o el tratamiento de sus datos personales, puede contactarnos al correo <a href="mailto:hola@sintergica.ai">hola@sintergica.ai</a> o al teléfono 56 5922 7340.
		</p>
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

    html {
        font-size: 16px;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        overflow-x: hidden;
    }

    .container {
        width: 100%;
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