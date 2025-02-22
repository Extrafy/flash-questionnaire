<template>
    <div style="width: 100%; height: 100%; background: rgb(249, 251, 255);">
        <ConsoleHeader></ConsoleHeader>
        <div class="from-span">
            <span style="position: absolute; top:20px; right: 50%; transform: translate(50%, 0);
            font-size: 20px; font-weight: 600;">从空白创建{{ choose_list[create_id].name }}</span>
            <span v-if="title_warning==1" class="title-warning">*标题不能为空</span>
            <span v-if="title_warning==2" class="title-warning">*标题最长为20个字符</span>
            <input type="text" placeholder="请输入标题" style="position: absolute; font-size: 20px;
            top:75px;left:50%; transform: translate(-50%,  0); width: 320px; height: 40px" v-model="q_name" >
            <span @click="startCreate" style="position: absolute; top:140px; right: 50%; transform: translate(50%, 0);
            font-size: 18px; font-weight: 500; background-color: blue; color: whitesmoke;
            width: 120px; height: 40px; border-radius: 5px;display: flex;align-items: center; justify-content: center; cursor: pointer;">立即创建</span>
        </div>
        <div class="from-former">
            <div>
                <span style="position: absolute; font-size: 18px; font-weight: 600; top: 3px; left: 5px;">从模板创建</span>
                <div style="position: absolute; left: 125px; height: 30px; width: 200px; top:3px;
                background: white; box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2); border-radius: 15px;">
                    <input type="text" id="screen" placeholder="请输入模板名" style="position: absolute; font-size: 14px;outline: none;
                    border:none;top:6px;left:5px;" v-model="m_name" @keydown.enter.prevent="search_name">
                    <font-awesome-icon :icon="['fas', 'magnifying-glass']" style="position: absolute; right: 5px; top:7px; height: 20px; width: 20px; cursor: pointer;"
                    @click="search_name"/>
                </div>
                <div v-for="hang in 4" :style="{'--y': hang-0.5}" class="hang" :key="hang">
                    <div v-for="lie in 5" :style="{'--x': lie-1}" class="lie" :key="hang*4+lie">
                        <div  v-if="curmoban[currentPage*20+hang*5+lie-26]" style="background-color: white; border-radius: 5px;
                         box-shadow: 0 0 0px .5px rgba(100, 100, 100, 0.5); width: 180px; height: 80px;">
                            <span style="position: absolute; top:5px; left:10px;
                            font-size: 16px; color: rgba(10, 10, 10, 1); " @click="goEdit(curmoban[currentPage*20+hang*5+lie-26].id)">{{ curmoban[currentPage*20+hang*5+lie-26].name }}</span>
                            <span class="yulan" @click="goEdit(curmoban[currentPage*20+hang*5+lie-26].id)">预览</span>
                        </div>
                    </div>
                </div>
                <el-pagination
                        v-model:current-page="currentPage"
                        v-model:page-size="pageSize"
                        :hide-on-single-page="false"
                        :total="curmoban.length"
                        layout="prev, pager, next,jumper,total"
                        @current-change="handleCurrentChange"
                        style="position: absolute; top:450px; right: 50%; transform: translate(50%, 0)"
                    />
            </div>
        </div>
    </div>
</template>

<script setup>
    import { useRoute } from 'vue-router';
    import { ref, computed } from 'vue';
    import ConsoleHeader from '@/components/ConsoleHeader.vue';
    import router from '../router/index';
    import { imgUrl } from '../../http/cookies';
    import { ElPagination } from "element-plus";
    import { library } from '@fortawesome/fontawesome-svg-core'
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
    import { fas } from '@fortawesome/free-solid-svg-icons'
    library.add(fas)
    
    const route = useRoute();
    const create_id = route.query.create_id;

    const choose_list = [
        { id: 0, name: '调查', img_src: imgUrl + '/assets/search.png' },
        { id: 1, name: '考试', img_src: imgUrl + '/assets/exam.png' },
        { id: 2, name: '投票', img_src: imgUrl + '/assets/vote.png' },
        { id: 3, name: '报名', img_src: imgUrl + '/assets/gragon.png' },
    ];

    let title_warning = ref(0);
    const q_name = ref('');
    const m_name = ref('');

    const startCreate = ()=>{
        if(q_name.value.length == 0){
            title_warning.value = 1;
        }
        else if(q_name.value.length > 20){
            title_warning.value = 2;
        }
        else{
            title_warning.value = 0;
            router.push({path: '/edit', query: {model_id: 0, create_id: create_id, q_name: q_name.value}})
        }
        setTimeout(()=>title_warning.value=0, 3000);
    }

    const moban = ref([
        [{id: 1, name: "校园满意度调查"},
        {id: 3, name: "心理健康调查"},
        {id: 18, name: "软件工程进度调查"},
        {id: 3, name: "工作满意度调查"},
        {id: 3, name: "客户反馈问卷"},
        {id: 3, name: "学习习惯调查"},
        {id: 3, name: "健康状况调查"},
        {id: 3, name: "消费习惯调查"},
        {id: 3, name: "产品满意度调查"},
        {id: 3, name: "教育质量调查"},
        {id: 3, name: "餐饮服务调查"},
        {id: 3, name: "旅游体验调查"},
        {id: 3, name: "职场压力调查"},
        {id: 3, name: "网络购物调查"},
        {id: 3, name: "环保意识调查"},
        {id: 3, name: "运动习惯调查"},
        {id: 3, name: "家庭氛围调查"},
        {id: 3, name: "社交媒体调查"},
        {id: 3, name: "生活方式调查"},
        {id: 3, name: "金融服务调查"},],
        [{id: 2, name: "数学期末考试"},
        {id: 20, name: "化学期末考试"},
        {id: 21, name: "程序设计期末考试"},
        {id: 22, name: "算法期末考试"},
        {id: 23, name: "数据库期末考试"},
        {id: 24, name: "操作系统期末考试"},
        {id: 25, name: "软工期末考试"},
        {id: 25, name: "数学基础测验"},
        {id: 25, name: "英语语法测试"},
        {id: 25, name: "物理知识考核"},
        {id: 25, name: "化学理论测验"},
        {id: 25, name: "历史知识测试"},
        {id: 25, name: "地理常识测验"},
        {id: 25, name: "生物学考试"},
        {id: 25, name: "文学作品测验"},
        {id: 25, name: "政治理论测试"},
        {id: 25, name: "经济学原理考核"},
        {id: 25, name: "计算机基础测验"},
        {id: 25, name: "统计学测试"},
        {id: 25, name: "哲学原理测验"},
        {id: 25, name: "心理学基础考核"},
        {id: 25, name: "社会学知识测试"},
        {id: 25, name: "艺术鉴赏考试"},
        {id: 25, name: "音乐理论测验"},
        {id: 25, name: "体育知识测试"},
        {id: 25, name: "法律常识测验"},
        {id: 25, name: "商业管理考试"},],
        [{id: 10, name: "班委选举"},
        {id: 12, name: "冯如杯一等奖投票"},
        {id: 14, name: "入党推优"},
        {id: 10, name: "最喜爱的电影"},
        {id: 10, name: "最爱的音乐类型"},
        {id: 10, name: "最喜欢的运动"},
        {id: 10, name: "最受欢迎的演员"},
        {id: 10, name: "最喜欢的书籍"},],
        [{id: 11, name: "班委选举报名"},
        {id: 15, name: "志愿者报名"},
        {id: 19, name: "球赛报名"},
        {id: 19, name: "夏令营报名表"},
        {id: 19, name: "篮球训练营报名"},
        {id: 19, name: "英语口语班报名"},
        {id: 19, name: "烘焙课程报名"},
        {id: 19, name: "摄影工作坊报名"},
        {id: 19, name: "编程入门班报名"},
        {id: 19, name: "艺术绘画班报名"},],
    ]);

    const curmoban = computed(() => {
        return moban.value[create_id].filter((item) => {
            return item.name.includes(m_name.value);
        })
    })

    let currentPage = ref(1);
    const pageSize = 20;

    const handleCurrentChange = (newPage) => {
        currentPage.value = newPage;
    }

    const goEdit = (edit_id) => {
        router.push({ path: "/edit", query: { edit_id: edit_id } });
    }

</script>

<style scoped>
.top_lan {
    width: 100%;
    height: 8vh;
    position: absolute;
    background-color: white;
    box-shadow: 0px 0px 2px 2px rgba(0, 0, 0, 0.5);
}

.top_biao {
    color: rgb(158, 166, 172);
    transition: all 0.3s ease;
}

.top_biao:hover {
    color: rgb(80, 71, 255);
}

.from-span{
    background-color: white;
    position: absolute;
    width: 500px;
    height: 200px;
    border-radius: 10px;
    box-shadow: 0 0 0px 1px rgba(100, 100, 100, 0.5);
    right: 50%;
    transform: translate(50%, 0);
    top:13%;
}

.title-warning{
    position: absolute;
    top:55px;
    right: 50%;
    transform: translate(50%, 0);
    color: red;
}

.from-former{
    position: absolute;
    top: 40%;
    right: 50%;
    transform: translate(50%, 0);
    width: 990px;
    height: 55%;
    overflow: scroll;
}

.from-former::-webkit-scrollbar {
  display: none;
}

.hang{
    position: absolute;
    top: calc(var(--y) * 100px);
    left: 5px;
    width: 980px;
    height: 80px;
}

.lie{
    position: absolute;
    left: calc(var(--x) * 200px);
}

.yulan{
    position: absolute; 
    bottom:5px; 
    right:10px;
    font-size: 14px; 
    color: rgba(100, 100, 100, 0.6);
    cursor: pointer;
}

.yulan:hover{
    color: rgb(22, 22, 255)
}
</style>