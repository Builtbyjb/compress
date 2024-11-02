/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./static/*.js"],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [],
}

