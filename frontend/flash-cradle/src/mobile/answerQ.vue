<template>
    <div class="container">
        <div class="outer" v-if="statu == 0" @click="tmpStore">
        <div style="position:fixed; width:100%; height: 100%; z-index:10000; color: rgba(0, 0, 0, 0); " v-if="abandon">

        </div>
            <div style="width: 100px; height:50px"></div>
            <div style="
                display: inline-block;
                width: 90%;
                margin-left: 3%;
                text-align: center;
              ">
                {{ title }}
            </div>
            <div style="width: 100px; height:30px"></div>
            <div style="display: inline-block; width: 90%; margin-left: 3%">
                <v-md-preview :text="jianjie" class="v-md-preview"></v-md-preview>
            </div>
            <div style="
              width: 100%;
              height: 1px;
              background-color: rgba(220, 220, 220, 1);">
            </div>
            <div v-for="(q, index) in list" :key="index" style="width: 92%; margin-left: 4%">
                <div style="width: 100%; height: 10px"></div>
                <div style="border: 1px solid rgba(200, 200, 200, 0.6); border-radius: 3px;">
                    <div class="kuang" style="margin-left: 2%;">
                        <div class="title_wrap">
                            <span style="font-size: 18px; margin-left: 15px;  padding-bottom: 12px; color: red;"
                                v-if="list[randomArray[index]].must">*</span>
                            <span style="font-size: 18px; margin-left: 10px;  padding-bottom: 14px;">{{ index + 1 }}.
                            </span>
                            <div style="display: inline-block; width: 60%; ">
                                <v-md-preview class="v-md-preview"
                                    :text="list[randomArray[index]].description"></v-md-preview>
                            </div>
                            <span
                                style="font-size: 14px; margin-left: 10px;  padding-bottom: 16px; color: rgba(50, 50, 50, 1);"
                                v-if="type == 1">分数：{{ list[randomArray[index]].img_url }}</span>
                        </div>
                        <div class="easy-answer" v-if="list[randomArray[index]].type === 3">
                            <textarea style="
                    width: 80%;
                    min-height: calc(2em + 2px);
                    padding: 8px;
                    font-size: 16px;
                    line-height: 1.5;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                    resize: vertical;
                    
                    margin-left: 24px;
                  " placeholder="请输入内容..." v-model="result[randomArray[index]]" v-on:input="tmpStore"></textarea>
                        </div>
                        <div class="item_wrap"
                            v-if="list[randomArray[index]].type == 0 || list[randomArray[index]].type == 1">
                            <div v-for="(item, index_item) in list[randomArray[index]].options" :key="index_item"
                                style="margin-left: 20px; display: flex; align-items: center; margin-bottom: 20px;">
                                <!-- <span v-if="index_item != 0" class="item-title">{{ index_item }}.</span> -->
                                <input type="radio" title="选中" :checked="item.choosed" class="checkedKuang" :class="{
            checked: item.choosed,
            multi: list[randomArray[index]].type === 1,
        }" @click="handleChoose(randomArray[index], index_item)" :disabled="type == 3 && item.left_num <= 0" />
                                <div style="display: inline-block; width: 60%;">
                                    {{ item.content }}
                                </div>
                                <div style="display: inline-block; width: 10%; font-size: 16px; font-weight: 500;"
                                    v-if="type == 3 && list[randomArray[index]].img_url">
                                    剩余{{ item.left_num }}人
                                </div>
                            </div>
                        </div>
                        <div class="rate-wrap" v-if="list[randomArray[index]].type === 2"
                            style="margin-top: 10px; margin-left: 30px">
                            <div class="rate-block">
                                <el-rate style="--el-rate-icon-size: 30px" show-score
                                    :max="list[randomArray[index]].arg2" :size="10"
                                    :void-icon="rateStyleList[list[randomArray[index]].arg1].icons[0]" :icons="{
            [list[randomArray[index]].arg2 / 3]: rateStyleList[list[randomArray[index]].arg1].icons[0],
            [(list[randomArray[index]].arg2 * 2) / 3]: rateStyleList[list[randomArray[index]].arg1].icons[1],
            [list[randomArray[index]].arg2]: rateStyleList[list[randomArray[index]].arg1].icons[2],
        }" :colors="{
            [list[randomArray[index]].arg2 / 3]: rateStyleList[list[randomArray[index]].arg1].colors[0],
            [(list[randomArray[index]].arg2 * 2) / 3]: rateStyleList[list[randomArray[index]].arg1].colors[1],
            [list[randomArray[index]].arg2]: rateStyleList[list[randomArray[index]].arg1].colors[2],
        }" v-model="list[randomArray[index]].options" />
                            </div>
                        </div>

                        <div v-if="list[randomArray[index]].type == 1"></div>
                    </div>
                    <div style="width: 100%; height: 5px"></div>
                </div>
                <div style="width: 100%; height: 10px"></div>
            </div>
            <button type="button" @click="error_lookup" id="createQsButton" v-if="statu == 0 && abandon == undefined">
                提交问卷
            </button>
            <div style="width: 100%; height: 5px"></div>
            <span class="error">{{ error_message }}</span>
            <div style="width: 100%; height: 10px"></div>
        </div>

        <div class="submit" v-if="statu == 0 && abandon == undefined">
            <span style="position: absolute; right: 50%; top:10px;transform: translate(-20%, 0); 
            font-size: 18px; font-weight: 600; color: #0095ff;">截止时间：</span>
            <el-countdown title="" :value="end_time" v-if="have_time" @finish="hilarity1" style="position: absolute; left: 50%; top:10px;transform: translate(20%, 0); 
            font-size: 16px; font-weight: 600; color: #0095ff;" value-style="font-size: 28px; font-weight: 600;" />
            <span style="position: absolute; left: 50%; top:10px;transform: translate(20%, 0); 
            font-size: 18px; font-weight: 600; color: #0095ff;" v-if="!have_time">不限时</span>
        </div>
    </div>

    <div class="failed" v-if="statu == 1 || statu == 2">
        <img :src="`${imgUrl}/assets/failed.png`" style="position: absolute; height: 20%; right: 50%; top:20%; 
        transform: translate(50%, 0);  " />
        <span style="position: absolute; right: 50%; transform: translate(50%, 0); font-size: 22px; font-weight: 600;
        top: 45%;" v-if="isRealsed && !isWrong">{{ statu == 1 ? '该问卷还未开始' : '该问卷已经结束' }}</span>
        <span style="position: absolute; right: 50%; transform: translate(50%, 0); font-size: 22px; font-weight: 600;
        top: 45%;" v-if="!isRealsed && !isWrong">问卷未发布</span>
        <span style="position: absolute; right: 50%; transform: translate(50%, 0); font-size: 22px; font-weight: 600;
        top: 45%;" v-if="isWrong">出现未知错误</span>
        <el-countdown title="" :value="start_time" v-if="statu == 1 && isRealsed && !isWrong" @finish="hilarity" style="position: absolute; right: 50%; top:50%; 
        transform: translate(50%, 0); font-size: 20px; font-weight: 600; text-align: center;"
            value-style="font-size: 28px; font-weight: 600;" />
    </div>

    <div v-if="statu == 3">
        <img :src="`${imgUrl}/assets/win.png`" class="win">
        <span class="success">问卷填写成功！</span>
        <span v-if="type == 1" class="score">你的成绩为： <span style="color: red; font-weight: 600;">{{ score }}</span></span>
        <div v-if="type == 2" class="toufen">
            <div class="question" v-for="(q, index) in list" :key="index">
                <div class="description">{{index + 1}}.{{q.description}}</div>
                <div v-if="q.img_url">
                    <VisualChoice :data="answer[index]"></VisualChoice>
                </div>
            </div>
            <div style="width: 100px;height:100px;"></div>
        </div>
    </div>
</template>

<script>
import {
    ChatDotRound,
    ChatLineRound,
    ChatRound,
    Watermelon,
    Pear,
    Apple,
    Star,
    Cloudy,
} from "@element-plus/icons-vue";
import VisualChoice from '@/components/VisualChoice.vue';
import { getQ, postQ } from "../../api/questionnaire/answerQ";
import { getUserId, getAnsweredQ, setAnsweredQ ,setUserMoney, getUserMoney,imgUrl} from "../../http/cookies";
import { getStatistic } from '../../api/questionnaire/analyse.js';
import { ElRate, ElCountdown } from "element-plus"

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// Introduce the theme you use. Take the github theme as an example here
import githubTheme from '@kangc/v-md-editor/lib/theme/github';
import '@kangc/v-md-editor/lib/theme/style/github.css';
// highlightjs
import hljs from 'highlight.js';
import { ElMessageBox } from "element-plus";
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
    components: {
        VisualChoice,
        ElRate, 
        ElCountdown,
        VMdPreview,
    },
    data() {
        return {
            imgUrl: imgUrl,
            abandon: false,
            randomArray: [],
            last_answer: [],
            title: '',
            jianjie: '',
            list: [],
            last_time: '不限',
            result: [],
            warning: [],
            rateValue: 0,
            rateStyleList: [
                {
                    colors: [],
                    icons: [Star, Star, Star],
                },
                {
                    colors: [],
                    icons: [Cloudy, Cloudy, Cloudy],
                },
                {
                    colors: ["#409eff", "#67c23a", "#FF9900"],

                    icons: [ChatRound, ChatLineRound, ChatDotRound],
                },
                {
                    colors: ["#409eff", "#67c23a", "#FF9900"],
                    icons: [Watermelon, Pear, Apple],
                },
            ],
            error_message: '',
            error_timer: '',
            statu: 1, //0为正常，1为未开始，2为还未结束, 3为填写完成
            start_time: new Date().getTime() + 5000,
            end_time: new Date().getTime() + 1000000,
            q_id: 0,
            type: 0,
            answers: [],
            have_time: true,
            isRealsed: true,
            isWrong: false,
            score: 0,
            answer: [],
        }
    },
    methods: {
        handleChoose(index, index_item) {
            let type = this.list[index].type;
            if (type === 0) {
                //单选题
                for (let i = 0; i < this.list[index].options.length; i++) {
                    this.list[index].options[i].choosed = false;
                }
                this.list[index].options[index_item].choosed = true;
            } else if (type === 1) {
                //多选题
                this.list[index].options[index_item].choosed = !this.list[index].options[index_item].choosed;
            }
            this.warning_lookup();
        },
        warning_init() {
            for (let i = 0; i < this.list.length; i++) {
                this.warning.push('');
            }
        },
        warning_lookup() {
            for (let i = 0; i < this.list.length; i++) {
                if (this.list[i].must) {
                    if (this.list[i].type === 0 || this.list[i].type === 1) {
                        let min = 1;
                        let max = 1;
                        if (this.list[i].type === 1) {
                            min = this.list[i].arg1;
                            max = this.list[i].arg2;
                        }
                        let num = 0;
                        for (let j = 0; j < this.list[i].options.length; j++) {
                            if (this.list[i].options[j].choosed == true) {
                                num++;
                            }
                        }
                        if (min > num || max < num) {
                            if (this.list[i].type === 0) {
                                this.warning[i] = '*该题目必选*';
                            }
                            else {
                                this.warning[i] = '*该题目最小选' + min + '个，最大选' + max + '个*'
                            }
                        }
                        else {
                            this.warning[i] = '';
                        }
                    }
                    else if (this.list[i].type === 2) {
                        if (this.list[i].options == '') {
                            this.warning[i] = '1';
                        }
                        else {
                            this.warning[i] = '';
                        }
                    }
                    else {
                        if (this.result[i] == '') {
                            this.warning[i] = '1';
                        }
                        else {
                            this.warning[i] = '';
                        }
                    }
                }
                if(this.list[i].type === 3){
                    if(this.result[i]){
                        if(this.result[i].length > 256){
                            this.warning[i] = '2';
                        }
                    }
                }
            }
        },
        result_init() {
            for (let i = 0; i < this.list.length; i++) {
                this.result.push('');
            }
        },
        submit() {
            let needPan = [];
            let tmpList = [];
            for (let i = 0; i < this.list.length; i++) {
                if (this.list[i].type === 0 || this.list[i].type === 1) {
                    let tmp = '';
                    let tmp2 = '';
                    for (let j = 0; j < this.list[i].options.length; j++) {
                        if (this.list[i].options[j].choosed == true) {
                            if (tmp == '') {
                                tmp = this.list[i].options[j].content;
                            }
                            else {
                                tmp = [tmp, this.list[i].options[j].content].join('%&%');
                            }
                            if (tmp2 == '') {
                                tmp2 = String(j);
                            }
                            else {
                                tmp2 = [tmp2, String(j)].join('%&%');
                            }
                        }
                    }
                    this.result[i] = tmp;
                    if (this.type == 1) {
                        this.answers[i] = tmp2;
                    }
                }
                else if (this.list[i].type === 2) {
                    this.result[i] = String(this.list[i].options);
                    if (this.type == 1) {
                        this.answers[i] = String(this.list[i].options);
                    }
                }
                if (this.type == 3 && (this.list[i].type == 1 || this.list[i].type == 0) && this.list[i].img_url) {
                    needPan.push(1);
                }
                else {
                    needPan.push(0);
                }
                tmpList.push({ans: this.result[i]})
            }
            let data = {
                q_id: this.q_id,
                user_name: getUserId(),
                answer_list: tmpList,
                isBao: needPan,
            }
            console.log("answer_list", data);
            postQ(data)
                .then((res) => {
                    console.log("res, ", res);
                    if (res.data.status_code == 1) {
                        this.getTouOut();
                        ElMessageBox.alert('问卷填写成功', 'Success!', {
                            confirmButtonText: '确定',
                            callback: () => {
                                this.statu = 3;
                                setUserMoney(1+ getUserMoney());
                                if (this.type == 1) {
                                    this.computeScore();
                                }
                                // this.router.push('/console');
                            }
                        });
                    }
                    else {
                        alert("问卷已截止或未发布");
                    }
                });
        },
        changeOptions() {
            for (let i = 0; i < this.list.length; i++) {
                if (this.list[i].type == 2 || this.list[i].type == 3) {
                    this.list[i].options = '';
                }
            }
        },
        error_lookup() {
            if (this.statu != 0) {
                alert("不在提交时间范围内");
                return;
            }
            this.warning_lookup();
            clearTimeout(this.error_timer);
            this.error_message = ''
            console.log("this.warning ", this.warning);
            for (let i = 0; i < this.warning.length; i++) {
                if (this.warning[i] != '') {
                    if(this.warning[i] == '1'){
                        this.error_message = '请做答第' + (this.randomArray[i] + 1) + '题';
                    }
                    else if(this.warning[i] == '2'){
                        this.error_message = '第' + (this.randomArray[i] + 1) + '题超出字数限制(256)';
                    }
                    this.error_timer = setTimeout(() => this.error_message = '', 3000);
                    return;
                }
            }
            this.submit();
        },
        hilarity() {
            if (this.have_time)
                this.statu = 0;
        },
        hilarity1() {
            if (this.have_time)
                this.statu = 2;
        },
        other_init() {
            for (let i = 0; i < this.list.length; i++) {
                this.answers.push(this.list[i].arg3);
            }
        },
        computeScore() {
            this.score = 0;
            for (let i = 0; i < this.list.length; i++) {
                let tmp = this.list[i].arg3;
                if (tmp != '') {
                    if (tmp == this.answers[i]) {
                        this.score += parseInt(this.list[i].img_url);
                    }
                    else {
                        if (this.list[i].type == 1) {
                            let options = tmp.split('%&%');
                            let myoptions = this.answers[i].split('%&%');
                            let flag = 0;
                            for (let k = 0; k < myoptions.length; k++) {
                                let once = 0;
                                for (let j = 0; j < options.length; j++) {
                                    if (myoptions[k] == options[j]) {
                                        once = 1;
                                        break;
                                    }
                                }
                                if (once == 1) {
                                    flag = 1;
                                }
                                else {
                                    flag = 0;
                                    break;
                                }
                            }
                            if (flag == 1) {
                                this.score += parseInt(this.list[i].img_url) / 2;
                            }
                        }
                    }
                }
            }
        },
        tryGetAnswer() {
            let content = getAnsweredQ(this.q_id);
            // console.log("abandon, ",this.abandon);
            console.log("content, ", content);
            if(content!=undefined && this.abandon==undefined){
                ElMessageBox.alert('检测到历史做答', '提示', {
                    confirmButtonText: '确定',
                    callback: () => {
                        this.last_answer = content.split('^&^');
                        this.recover();
                    }
                });
            }
            else if(this.abandon=='true'){
                this.last_answer = content.split('^&^');
                this.recover();
            }
        },
        recover() {
            for (let i = 0; i < this.list.length; i++) {
                if (this.list[i].type === 0 || this.list[i].type === 1) {
                    let ops = this.last_answer[i].split('%&%');
                    console.log("ops", ops);
                    for (let j = 0; j < ops.length; j++) {
                        if (ops[j] != '') {
                            this.list[i].options[parseInt(ops[j])].choosed = true;
                        }
                    }
                }
                else if (this.list[i].type === 2) {
                    this.list[i].options = parseInt(this.last_answer[i]);
                }
                else {
                    this.result[i] = this.last_answer[i];
                }
            }
        },
        tmpStore() {
            let tmpAnswer = '';
            for (let i = 0; i < this.list.length; i++) {
                let tmp = '';
                if (this.list[i].type === 0 || this.list[i].type === 1) {
                    let tmp2 = '';
                    for (let j = 0; j < this.list[i].options.length; j++) {
                        if (this.list[i].options[j].choosed == true) {
                            if (tmp2 == '') {
                                tmp2 = String(j);
                            }
                            else {
                                tmp2 = [tmp2, String(j)].join('%&%');
                            }
                        }
                    }
                    tmp = tmp2;
                }
                else if (this.list[i].type === 2) {
                    tmp = String(this.list[i].options);
                    if (this.type == 1) {
                        this.answers[i] = String(this.list[i].options);
                    }
                }
                else {
                    tmp = this.result[i];
                }
                if (tmpAnswer == '') {
                    tmpAnswer = tmp;
                }
                else {
                    tmpAnswer = [tmpAnswer, tmp].join("^&^");
                }
            }
            console.log("tmpAnswer, ", tmpAnswer);
            setAnsweredQ(this.q_id, tmpAnswer);
        },
        getRandomArray() {
            let n = this.list.length;
            let arr = Array.from({ length: n }, (_, index) => index);
            for (let i = arr.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            this.randomArray = arr;
        },
        getNormalArray() {
            this.randomArray = [];
            for (let i = 0; i < this.list.length; i++) {
                this.randomArray.push(i);
            }
        },
        getTouOut() {
            getStatistic({ qn_id: this.q_id }).then((res2) => {
                this.answer = res2.data.list;
                console.log("this.answer, ", this.answer);
            }).catch((err) => {
                console.log("res2, ", err);
            });
        },
    },
    mounted() {
        this.q_id = this.$route.query.q_id;
        this.abandon = this.$route.query.abandon;
        let data = {
            q_id: this.q_id,
        };
        getQ(data)
            .then((res) => {
                if (res.data.status_code == 5) {
                    this.isRealsed = false;
                    return;
                }
                else if (res.data.status_code != 1) {
                    this.isWrong = true;
                    return;
                }
                console.log("answer_res, ", res.data);
                this.title = res.data.title;
                this.jianjie = res.data.description;
                this.type = parseInt(res.data.type);
                let tmp = res.data.list;
                this.start_time = res.data.fuck_time;
                if (this.start_time == null) {
                    this.have_time = false;
                    this.statu = 0;
                }
                else {
                    this.start_time = new Date(this.start_time).getTime();
                }
                this.end_time = res.data.finished_time;
                if (this.end_time == null) {
                    this.have_time = false;
                    this.statu = 0;
                }
                else {
                    this.end_time = new Date(this.end_time).getTime();
                }
                for (let i = 0; i < tmp.length; i++) {
                    tmp[i].type = parseInt(tmp[i].type);
                    if (this.type == 2 || this.type == 3) {
                        if (tmp[i].type == 0 || tmp[i].tmp == 1) {
                            if (tmp[i].img_url == 'true') {
                                tmp[i].img_url = true;
                            }
                            else {
                                tmp[i].img_url = false;
                            }
                        }
                    }
                }
                this.list = tmp;
                this.result_init();
                this.warning_init();
                this.warning_lookup();
                this.tryGetAnswer();
                if (this.type == 1) {
                    this.getRandomArray();
                }
                else {
                    this.getNormalArray();
                }
            })
            .catch((err) => {
                console.log("res, ", err);
            });
    }
}
</script>

<style scoped>
.outer {
    width: 90%;
    height: auto;
    margin-left: 50%;
    margin-top: 20px;
    margin-bottom: 20px;
    transform: translate(-50%, 0);
    background: white;
    box-shadow: 0px 0px 1px 1px rgb(200, 200, 200);
}

.kuang {
    margin: 20px 0px;
    width: 100%;
}

.title_wrap {
    display: flex;
    align-items: center;
}

.checkedKuang {
    appearance: none;
    background-color: #fff;
    border: 1px solid #a6a6a6;
    box-shadow: 0 1px 0 0 rgba(0, 0, 0, 0.08);
    border-radius: 50px;
    display: inline-block;
    transition: all 0.1s;
}

.checkedKuang.checked {
    border: 5px solid #0095ff;
    padding: 6.8px;
}

.checkedKuang.multi {
    border-radius: 0;
}

input {
    border: 0px solid;
    padding: 10px;
    background-color: white;
}

input:hover {
    border: 1px solid;
}

input:focus {
    border: 1px solid;
    outline: 1px solid transparent;
}

.container {
    width: 100%;
    height: 100%;
    position: fixed;
    overflow-y: scroll;
    overflow-x: hidden;
}

.submit {
    position: fixed;
    top: 0%;
    width: 100%;
    height: 40px;
    background: white;
    box-shadow: 0px 0px 1px 1px rgba(200, 200, 200, 0.8);
    border-radius: 3px;
}

.error {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: 18px;
    color: red;
}

.jiao {
    position: absolute;
    right: 50%;
    bottom: 10px;
    transform: translate(50%, 0);
    padding: 5px 10px;
    box-shadow: 0px 0px 1px 1px rgba(200, 200, 200, 0.8);
    font-size: 18px;
}

.jiao:hover {
    background: #04b722;
}

.win {
    height: 20%;
    position: absolute;
    top: 35%;
    right: 50%;
    transform: translate(50%, -50%);
}

.success {
    position: absolute;
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    font-size: 20px;
    font-weight: 600;
}

.score {
    position: absolute;
    top: 55%;
    right: 50%;
    transform: translate(50%, -50%);
    font-size: 20px;
    font-weight: 500;
}

#createQsButton {
    margin-left: 5%;
    height: 45px;
    width: 90%;
    font-size: 18px;
    justify-content: center;
    align-items: center;
    border: none;
    border-radius: 5px;
    background-color: #87ceeb;
    color: #333;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.5s ease, color 0.5s ease, box-shadow 0.5s ease;
    cursor: pointer;
}

#createQsButton:hover {
    background-color: #71b3e9;
    color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.question {
    width: 80%;
    min-width: 500px;
    min-height: 100px;
    margin-left: 10%;
    margin-right: 10%;
}

.description {
    font-size: 20px;
    height: 60px;
    line-height: 60px;
    width: 100%;
}

.toufen{
    position: absolute;
    top:53%;
    width: 100%;
}
</style>