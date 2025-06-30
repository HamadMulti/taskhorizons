module.exports = {
  darkMode: 'class',
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50:'#fefce8',
          100:'#fef9c3',
          200:'#fef08a',
          300:'#fde047',
          400:'#facc15',
          500:'#eab308',
          600:'#ca8a04',
          700:'#a16207',
          800:'#854d0e',
          900:'#713f12',
          950:'#422006'
        },
        secondary: {
          50:'#f8fafc',
          100:'#f1f5f9',
          200:'#e2e8f0',
          300:'#cbd5e1',
          400:'#94a3b8',
          500:'#64748b',
          600:'#475569',
          700:'#334155',
          800:'#1e293b',
          900:'#0f172a',
          950:'#020617'
        },
        btns: {
          primary: '#eab308',
          secondary: '#ca8a04',
          50:'#fefce8',
          100:'#fef9c3',
          200:'#fef08a',
          300:'#fde047',
          400:'#facc15',
          500:'#eab308',
          600:'#ca8a04',
          700:'#a16207',
          800:'#854d0e',
          900:'#713f12',
          950:'#422006'
        },
        textCl: {
          primary: '#020617',
          secondary: '#0f172a',
          50:'#f8fafc',
          100:'#f1f5f9',
          200:'#e2e8f0',
          300:'#cbd5e1',
          400:'#94a3b8',
          500:'#64748b',
          600:'#475569',
          700:'#334155',
          800:'#1e293b',
          900:'#0f172a',
          950:'#020617'
        },
        backgrounds: {
          DEFAULT: '#C8A2C8',
          50: '#f7f2fd',
          100: '#f7f2fd',
          200: '#d7c0f3',
          300: '#c7a7ee',
          400: '#b78dea',
          500: '#a774e5',
          600: '#975be0',
          700: '#8742db',
          800: '#7728d7',
          900: '#6924bd',
          950: '#5b1fa4'
        }
      }
    },
    fontFamily: {
      body: ['Poppins', 'sans-serif'],
      sans: ['Poppins', 'sans-serif']
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
    require('flowbite/plugin')
  ]
};
