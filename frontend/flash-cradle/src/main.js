import { createApp } from 'vue'
//重点 样式必须要加
import App from './App.vue'
import router from './router/index'
import router_mobile from './router/mobileIndex'
import './router/permit'

//text-editor-------markdown render

import { isMobile } from './utils/device';

import VueLazyload from 'vue-lazyload'

const app = createApp(App);

app.use(VueLazyload, {
  preLoad: 1.3,
  error: '路径/to/error.png',  // 错误占位图
  loading: '路径/to/loading.gif',  // 加载时占位图
  attempt: 1
})

if (isMobile()) {
  app.use(router_mobile);
} else {
  app.use(router);
}
app.mount('#app')