process.env.NODE_ENV = 'production';

module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [
      'about.html',
      'base.html',
      'demo.html',
      'gallery.html',
      'home.html',
      'imgview.html',
      'nav.html',
      'nav_bottom.html',
      'privacy.html',
  ],
  theme: {
    extend: {
      spacing: {
        '9/16': '56.25%',
      }
    },
  },
  variants: {},
  plugins: [],
}
