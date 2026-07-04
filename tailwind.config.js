/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f7ff',
          100: '#ebf0ff',
          200: '#d6e0ff',
          300: '#b3c7ff',
          400: '#85a3ff',
          550: '#4d70ff',
          500: '#3b5beb',
          600: '#253ee0',
          700: '#1b2bc2',
          800: '#17229e',
          900: '#151f7e',
        }
      }
    },
  },
  plugins: [],
}
