import { createRouter, createWebHistory } from 'vue-router';
const router = createRouter({
    history: createWebHistory(),
    routes : [
        {
            path: '/',
            redirect: '/home',
        },
        {
            path: '/home',
            name: 'home',
            component: ()=>
                import(
                    '@/components/home.vue'
                ),
        },
        {
            path: '/console',
            component: ()=>
                import(
                    '@/components/console.vue'
                ),
        },
        {
            path: '/recycle',
            component: ()=>
                import(
                    '@/components/recycleSite.vue'
                ),
        },
        {
            path: '/plaza',
            component: ()=>
                import(
                    '@/components/plaza.vue'
                ),
        },
        {
            path: '/analyse',
            component: ()=>
                import(
                    '@/view/BasicAnalysis.vue'
                ),
        },
        {
            path: '/plaza/search',
            component: ()=>
                import(
                    '@/view/PlazaSearch.vue'
                ),
        },
        {
            path: '/edit',
            component: ()=>
                import(
                    '@/view/editQ.vue'
                ),
        },
        {
            path: '/answer',
            name: 'answer',
            component: ()=>
                import(
                    '@/view/answerQ.vue'
                ),
        },
        {
            path: '/changePw',
            name: 'changePw',
            component: ()=>
                import(
                    '@/view/pwChange.vue'
                ),
        },
        {
            path: '/login',
            name: 'login',
            component: ()=>
                import(
                    '@/view/LoginRegister.vue'
                ),
        },
        {
            path: '/create',
            name: 'create',
            component: ()=>
                import(
                    '@/view/createQ.vue'
                ),
        },
        {
            path: '/person',
            name: 'person',
            component: ()=>
                import(
                    '@/view/PersonCenter.vue'
                ),
        },
        {
            path: '/collection',
            name: 'collection',
            component: ()=>
                import(
                    '@/view/myCollection.vue'
                ),
        },
        {
            path: '/buy',
            name: 'buy',
            component: ()=>
                import(
                    '@/view/myBuy.vue'
                ),
        },
        {
            path: '/crossAnalysis',
            name: 'crossAnalysis',
            component: ()=>
                import(
                    '@/view/crossAnalysis.vue'
                ),
        },
        {
            path: '/history',
            name: 'history',
            component: ()=>
                import(
                    '@/view/myHistory.vue'
                ),
        },
    ],
})

export default router;
