const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: false,
  configureWebpack: {
    cache: true
  },
  chainWebpack: config => {
    config.module
      .rule('css')
      .oneOf('normal')
      .use('css-loader')
      .tap(options => {
        options.url = false;
        return options;
      });

    config.module
      .rule('scss')
      .oneOf('normal')
      .use('css-loader')
      .tap(options => {
        options.url = false;
        return options;
      });
  }
})