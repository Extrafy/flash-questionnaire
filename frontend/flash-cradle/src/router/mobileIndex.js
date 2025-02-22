import { createRouter, createWebHistory } from 'vue-router';
import HomeItem from "@/mobile/home.vue";
import ConsoleItem from '@/components/console.vue';
import AnswerQ from '@/mobile/answerQ.vue';

const router_mobile = createRouter({
    history: createWebHistory(),
    routes : [
        {
            path: '/',
            redirect: '/home',
        },
        {
            path: '/home',
            name: 'home',
            component: HomeItem,
        },
        {
            path: '/answer',
            name: 'answer',
            component: AnswerQ,
        },
        {
            path: '/console',
            component: ConsoleItem,
        },
        {
            path: '/login',
            name: 'login',
            component: ()=>
                import(
                    '@/mobile/LoginRegister.vue'
                ),
        },
        {
            path: '/person',
            name: 'person',
            component: ()=>
                import(
                    '@/mobile/PersonCenter.vue'
                ),
        },
    ],
})

export default router_mobile;
