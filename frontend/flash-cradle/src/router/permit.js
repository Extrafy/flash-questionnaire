import router from './index'
import router_mobile from './mobileIndex'
//导入cookies
import { getUserId } from '../../http/cookies'
let answer_id = -1;

// 前置路由
router.beforeEach((to, from, next) => {
    if (!getUserId()) {
        console.log("from.name", from.name);
        if (to.name === 'answer') {
            answer_id = to.query.q_id;
        }
        if (
            to.name === 'login' ||
            to.name === 'home' ||
            to.name === 'changePw'
        ) {
            next() //确认进入
        } else {
            next({ name: 'login', query: { answer_id: answer_id } })
        }
    }
    else {
        next()
    }
})

router_mobile.beforeEach((to, from, next) => {
    if (!getUserId()) {
        console.log("from.name", from.name);
        if (to.name === 'answer') {
            answer_id = to.query.q_id;
        }
        if (
            to.name === 'login' ||
            to.name === 'home' ||
            to.name === 'changePw'
        ) {
            next() //确认进入
        } else {
            next({ name: 'login', query: { answer_id: answer_id } })
        }
    }
    else {
        next()
    }
})
