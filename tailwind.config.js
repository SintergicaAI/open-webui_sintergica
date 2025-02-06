import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				gray: {
					50: '#f9f9f9',
					100: '#ececec',
					200: '#e3e3e3',
					300: '#cdcdcd',
					400: '#b4b4b4',
					500: '#9b9b9b',
					600: '#676767',
					700: '#4e4e4e',
					800: 'var(--color-gray-800, #333)',
					850: 'var(--color-gray-850, #262626)',
					900: 'var(--color-gray-900, #171717)',
					950: 'var(--color-gray-950, #0d0d0d)'
				},
				brand:{
					50: '#F9F9FC',
					100: '#B4E0F7',
					200: '#89CAF5',
					300: '#5DB0F5',
					400: '#3092F7',
					500: '#006EFA',
					600: '#005ACD',
					700: '#0046A0',
					800: '#003373',
					900: '#001F46',
					950: '#000B19'
				},
				primary: {
					50: '#e6f3ff',
					100: '#cce7ff',
					200: '#99ceff',
					300: '#66b5ff',
					400: '#339cff',
					500: '#0070f3',
					600: '#005acc',
					700: '#004599',
					800: '#003066',
					900: '#001a33'
				}
			},
			spacing: {
				none: '0.0rem',
				xs: '0.25rem',
				sm: '0.5rem',
				base: '0.75rem',
				lg: '1rem',
				xl: '1.25rem',
				'2xl': '1.5rem',
				'3xl': '2rem',
				'4xl': '2.5rem',
				'5xl': '4rem',
				'6xl': '8rem',
			},
			borderRadius: {
				sm: '8px',
			},
			typography: {
				DEFAULT: {
					css: {
						pre: false,
						code: false,
						'pre code': false,
						'code::before': false,
						'code::after': false
					}
				}
			},
			fontFamily: {
				archivo: ['Archivo', 'sans-serif'],
			},
			padding: {
				'safe-bottom': 'env(safe-area-inset-bottom)'
			}
		}
	},
	plugins: [typography]
};
