/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Design tokens structure for SaaS Enterprise Aesthetic (Dark Mode)
        brand: {
          50: '#f4f6ff',
          100: '#ebf0ff',
          200: '#d9e2ff',
          300: '#b8caff',
          400: '#94abff',
          500: '#5c7cff', // Primary blue (Linear style)
          600: '#4361ee',
          700: '#344bc7',
          800: '#28389c',
          900: '#1d2770',
          950: '#111645',
        },
        ui: {
          bg: '#090a0f',        // Darkest background
          surface: '#11131c',   // Elevated surface container
          surfaceHover: '#1a1d29',
          border: '#1f2433',    // Border default
          borderHover: '#2e354a',
          divider: '#161924',
          
          text: {
            primary: '#f8fafc',
            secondary: '#94a3b8',
            tertiary: '#64748b',
            disabled: '#475569',
          },
          
          success: {
            bg: '#064e3b',
            border: '#047857',
            text: '#34d399',
            solid: '#10b981',
          },
          warning: {
            bg: '#78350f',
            border: '#b45309',
            text: '#fbbf24',
            solid: '#f59e0b',
          },
          danger: {
            bg: '#4c0519',
            border: '#9f1239',
            text: '#fda4af',
            solid: '#f43f5e',
          },
          info: {
            bg: '#0c4a6e',
            border: '#0369a1',
            text: '#7dd3fc',
            solid: '#0ea5e9',
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '4': '4px',
        '8': '8px',
        '12': '12px',
        '16': '16px',
        '20': '20px',
        '24': '24px',
        '32': '32px',
        '40': '40px',
        '48': '48px',
      }
    },
  },
  plugins: [],
}
