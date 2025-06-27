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
        logo: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
          950: '#500724'
        },
        btns: {
          primary: '#61459e',
          secondary: '#3d2c64',
          50: '#f6f4fa',
          100: '#e4def0',
          200: '#d1c8e7',
          300: '#bfb1dd',
          400: '#ad9bd3',
          500: '#9b85ca',
          600: '#886fc0',
          700: '#7659b6',
          800: '#6649a6',
          900: '#593f90',
          950: '#4b357a'
        },
        textCl: {
          primary: '#080121',
          secondary: '#22048b',
          50: '#f3f0ff',
          100: '#dad1fe',
          200: '#c2b2fd',
          300: '#aa93fc',
          400: '#9174fb',
          500: '#7955fa',
          600: '#6136f9',
          700: '#4817f8',
          800: '#3807e8',
          900: '#3106c9',
          950: '#2905aa'
        },
        primary: {
          50: '#f6f1fe',
          100: '#e5d5fc',
          200: '#d3b9fa',
          300: '#c19df8',
          400: '#b081f6',
          500: '#9e65f4',
          600: '#8d49f2',
          700: '#7b2df0',
          800: '#6911ee',
          900: '#5d0fd2',
          950: '#510db6'
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
      body: ['Inter', 'sans-serif'],
      sans: ['Inter', 'sans-serif']
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
