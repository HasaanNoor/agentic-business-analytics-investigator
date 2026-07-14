/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#172033',
        muted: '#5d667a',
        panel: '#ffffff',
        line: '#d9dee8',
        canvas: '#f5f7fb',
        accent: '#246b73',
        warning: '#a45f00',
        danger: '#b42318',
        success: '#16794c',
      },
      boxShadow: {
        soft: '0 1px 2px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
};
