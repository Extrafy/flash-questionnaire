<template>
<div class="window">
    <ConsoleHeader></ConsoleHeader>
    <div class="body">
        <div v-if="qnid !== -1">
            <div class="title">{{questionnaire.title}}</div>
            <div class="statistics">
                <el-table :data="record.rows.slice((currentPage-1)*10,Math.min((currentPage)*10,record.rows.length))" border stripe table-layout="auto" height="440px" >
                    <el-table-column v-for="index in new Array(record.colname.length).keys()" :key="index" :prop="record.colname[index]" :label="questionnaire.list[index].description" min-width="200px"></el-table-column>
                </el-table>
                <div style="display: flex; justify-content: space-between;">
                    <el-pagination v-model=currentPage @current-change="currentPageChange" layout="prev, pager, next" :total="record.rows.length" style="padding-top: 5px;"/>
                    <button class="bt" @click="toExcel">下载数据</button>
                </div>
            </div>
            <div class="question" v-for="(q, index) in questionnaire.list" :key="index">
                <div class="description">
                    <span>{{ index+1 }}.</span>
                    <div style="display: inline-block; width: 60%"><v-md-preview :text="q.description"></v-md-preview></div>
                </div>
                <!-- <div class="description">{{index + 1}}.{{q.description}}</div> -->
                <div v-if="parseInt(q.type) !== 3">
                    <VisualChoice :data="answer[index]"></VisualChoice>
                </div>
                <div v-if="parseInt(q.type) === 3">
                    <VisualWord :txt="answer[index]"></VisualWord>
                </div>
            </div>
        </div>
        <div style="width: 100%; height: 100px;"></div>           
    </div>
</div>
</template>

<script>
import ConsoleHeader from '@/components/ConsoleHeader.vue';
import VisualChoice from '@/components/VisualChoice.vue';
import VisualWord from '@/components/VisualWord.vue';
import { initialize, getStatistic, getData } from '../../api/questionnaire/analyse.js';
import { getUserId } from '../../http/cookies.js';
import { ElTable, ElPagination } from "element-plus"
export default {
    name: "BasicAnalysis",
    components: {
        ConsoleHeader,
        VisualChoice,
        VisualWord, ElTable, ElPagination
    },
    data() {
        return {
            qnid: -1,
            currentPage: 1,
            questionnaire: {},
            answer: [],
            record: { colname: [], rows: [] }
        }
    },
    mounted() {
        initialize({
            q_id: this.$route.query.qnid,
            user_name: getUserId()
        }).then((res1) => {
            console.log("???", res1.data.status_code);
            if (res1.data.status_code === 1) {
                this.qnid = this.$route.query.qnid;
                this.questionnaire = res1.data;
                console.log(this.questionnaire);
                getStatistic({qn_id: this.qnid}).then((res2) => {
                    this.answer = res2.data.list;
                    console.log("this.answer, ", this.answer);
                    getData({qn_id: this.qnid}).then((res3) => {
                        this.record = res3.data;
                        console.log(this.record);
                    }).catch((err) => {
                        console.log("res3, ", err);
                    });
                }).catch((err) => {
                    console.log("res2, ", err);
                });
            }
            else {
                this.qnid = -1;
                console.log(res1.data.status_code);
            }
        }).catch((err) => {
            console.log("res1, ", err);
        });  
    },
    methods: {
        currentPageChange(number) {
            this.currentPage = number;
        },
        getFormattedDateTime() {
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hour = String(now.getHours()).padStart(2, '0'); // 获取小时
            const minute = String(now.getMinutes()).padStart(2, '0'); // 获取分钟
            const second = String(now.getSeconds()).padStart(2, '0'); // 获取秒
            return `${year}_${month}_${day}-${hour}_${minute}_${second}`;
        },
        async toExcel(){
            // eslint-disable-next-line no-undef
            const workbook = new ExcelJS.Workbook();
            const worksheet = workbook.addWorksheet('flash-questionnaire');
            let columns = [];
            let rows = [];
            for (let i = 0; i < this.questionnaire.list.length; i++)
                columns.push({header: this.questionnaire.list[i].description, key: String(i), width: 50});
            for (let i = 0; i < this.record.rows.length; i++) {
                let r = {};
                for (let j = 0; j < this.record.colname.length; j++)
                    r[String(j)] = this.record.rows[i][this.record.colname[j]];
                rows.push(r);
            }
            console.log(columns);
            console.log(rows);
            worksheet.columns = columns;
            worksheet.addRows(rows);
            const buffer = await workbook.xlsx.writeBuffer()
            const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            // eslint-disable-next-line no-undef
            saveAs(blob, `${this.questionnaire.title}_${this.getFormattedDateTime()}.xlsx`);
        }
    }
}
</script>
<style>
.github-markdown-body {
  padding: 0 !important;
}
</style>
<style scoped>
.window {
    width: 100%;
    min-width: 750px;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    overflow-x: scroll;
    background-color: rgb(238, 244, 251);
    font-family: Arial, Helvetica, sans-serif;
}
.body {
    position: absolute;
    top: 60px;
    left: 10%;
    width: 80%;
    min-width: 600px;
    min-height: calc(100% - 60px);
    background-color: white;
}
.title {
    height: 100px;
    line-height: 100px;
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}
.statistics {
    width: 80%;
    margin-left: 10%;
    margin-right: 10%;
    overflow-y: scroll;
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
    /* height: 60px; */
    /* line-height: 60px; */
  display: flex;
  /* align-items: center; */
}
.bt {
    width: 80px;
    margin-top: 10px;
    font-size: 15px;
    height: 30px;
    border-radius: 5px;
    background-color: #007bff;
    border: 0px;
    color: white;
}
.bt:hover {
    background-color: #0056b3;
    cursor:pointer;
}
</style>