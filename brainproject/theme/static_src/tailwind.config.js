/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
          colors: {
            'navColor': '#1D1D1D',
            'navColor2': '#0F0F0F',
            'iblue':'#037Ef3',
            'ired':'#F85A40',
            'iorange':"#F48924",
            'idarkblue':'#0A8EA0',
            'iwhite':'#F3F4F7',
            'iblack':'#52565E',
            'ilightblue':'#0CB9C1',
          },
          linearGradientColors: {
            'custom-gradient': ['#0F0F0F', '#1D1D1D'],
            'igblue':['var(--color-iblue)', 'var(--color-ilightblue)'],
            'igred':['var(--color-ired)', 'var(--color-iorange)'],
          },
          borderColor: {
            'nav1': 'rgba(29, 29, 29, 1)',
          },
          borderRadius: {
            'ibtn': '29px',
          },
          fontFamily: {
            'poppins': ['Poppins', 'sans-serif'],
          },
          fontSize: {
            '23': '23px',
          },
          margin: {
            '1/2': '30%',
          },
        },
      },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        function ({ addUtilities }) {
            const gradients = {
              '.text-igred': {
                'background': 'linear-gradient(to right, #F48924, #F85A40)',
                '-webkit-background-clip': 'text',
                'color': 'transparent',
                'position': 'relative',
                'display': 'inline-block',
              },
              '.text-igred::before': {
                'content': 'attr(data-content)',
                'position': 'absolute',
                'top': '0',
                'left': '0',
                'z-index': '-1',
                'background': 'linear-gradient(to right, #F48924, #F85A40)',
                '-webkit-background-clip': 'text',
                'color': 'transparent',
                'width': '100%',
                'height': '100%',
              },
              '.text-igblue': {
                'background': 'linear-gradient(to right, #037Ef3, #0A8EA0)',
                '-webkit-background-clip': 'text',
                'color': 'transparent',
                'position': 'relative',
                'display': 'inline-block',
              },
              '.text-igblue::before': {
                'content': 'attr(data-content)',
                'position': 'absolute',
                'top': '0',
                'left': '0',
                'z-index': '-1',
                'background': 'linear-gradient(to right, #037Ef3, #0A8EA0)',
                '-webkit-background-clip': 'text',
                'color': 'transparent',
                'width': '100%',
                'height': '100%',
              },
            };
            addUtilities(gradients, ['responsive', 'hover']);
          },
    ],
}
