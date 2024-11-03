/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./static/scripts/*.js"],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [],
}

