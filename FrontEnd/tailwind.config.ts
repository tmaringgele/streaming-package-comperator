import type { Config } from 'tailwindcss';
import flowbitePlugin from 'flowbite/plugin'

export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],
  darkMode: 'selector',
  theme: {
    extend: {
      colors: {
        // flowbite-svelte
        primary: {
			DEFAULT: '#4B94E3',
			50: '#EAF2FC',
			100: '#D8E8F9',
			200: '#B5D3F3',
			300: '#92BEEE',
			400: '#6EA9E8',
			500: '#4B94E3',
			600: '#2177D5',
			700: '#1A5CA4',
			800: '#124174',
			900: '#0A2643',
			950: '#07182B'
        }
      }
    }
  },
  plugins: [flowbitePlugin]
} as Config;