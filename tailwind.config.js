/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}", 
    "./templates/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      fontSize: {
        xs: '0.6rem',
      },
      colors : {
        'lakeBlue': '#5C8BC1',
        'bgLakeBlue': '#e2eaf3',
        'honeydew': '#f3ffeb',
        'darkNavy': '#17183a',
        'redLight': '#FDE8E8',
        'redDark': '#9B1C1C',
        'success': '#03543F',
        'successBg': '#F3FAF7',
      },
      backgroundImage: {
        'flowerBg': "url('../static/img/bgimg.jpg')",
      }
    },
  },
  plugins: [
    require('flowbite/plugin', '@tailwindcss/forms')
  ],
}

