/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#050a14',
          900: '#0a0f1e',
          800: '#0d1428',
          700: '#111d36',
          600: '#1a2a4a',
        },
        jade: {
          400: '#4ade9a',
          500: '#22c55e',
          600: '#16a34a',
          DEFAULT: '#00a36c',
        },
        gold: {
          300: '#fde68a',
          400: '#fbbf24',
          500: '#d4af37',
          600: '#b8960c',
          DEFAULT: '#d4af37',
        },
      },
      fontFamily: {
        display: ['Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
