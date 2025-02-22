const { defineConfig } = require('@vue/cli-service')
const path = require('path');

const webpack = require('webpack')
const CompressionPlugin = require('compression-webpack-plugin')
const zlib = require('zlib')

// vue.config.js
// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');



module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    open: false, //运行项目后是否自动打开
    // port: 10001,
    proxy: {
      '/api': {
        target: 'http://101.200.29.174:30000', //接口地址
        ws: true, //是否开启websockets
        changeOrigin: true, //是否开启跨域
        secure: false,
        // pathRewrite: {
        //   '^/api': '' //查找开头为 /api 的字符，替换成空字符串
        // }
      }
    },
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@i': path.resolve(__dirname, './src/assets'),
      }
    },
    plugins: [
      new webpack.IgnorePlugin({
        resourceRegExp: /^\.\/locale$/,
        contextRegExp: /moment$/,
      }),
      // 压缩成 .gz 文件
      new CompressionPlugin({
        filename: '[path][base].gz',
        algorithm: 'gzip',
        test: /\.js$|\.css$|\.html$/,
        threshold: 10240,
        minRatio: 0.8
      }),
      // 压缩成 .br 文件
      new CompressionPlugin({
        filename: '[path][base].br',
        algorithm: 'brotliCompress',
        test: /\.(js|css|html|svg)$/,
        compressionOptions: {
          params: {
            [zlib.constants.BROTLI_PARAM_QUALITY]: 11
          }
        },
        threshold: 10240,
        minRatio: 0.8
      }),
      // new BundleAnalyzerPlugin()
    ],
    optimization: {
      runtimeChunk: 'single',
      splitChunks: {
        chunks: 'all',
        maxInitialRequests: Infinity,
        minSize: 20000,
        cacheGroups: {
          vendors: {
            test: /[\\/]node_modules[\\/]/, // 使用正则匹配node_modules中引入的模块
            priority: -10, // 优先级值越大优先级越高，默认-10，不用修改
            name(module) {
              // 设定分包以后的文件模块名字，按照包名字替换拼接一下
                
              if (!module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)) return;
              const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
              return `npm.${packageName.replace('@', '')}`;
            }
          }
        }
      }
    },
  },
})
