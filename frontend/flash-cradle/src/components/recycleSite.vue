<template>
    <div>
        <ConsoleHeader></ConsoleHeader>
        <div style="margin-top:100px;">
            <div style="margin:auto;width: 930px;">
                <span
                    style="color: #1ea0fa;font-size:14px;margin-left:10px;">如果您想释放上传文件题的空间，请点击“清空数据”，数据清空后将无法恢复，请谨慎操作！</span>

                <button class="mybtn" style="margin-left:110px;" @click="handleToConsole()">返回控制台</button>
                <button class="mybtn" style="margin-left: 10px;" @click="handleDeleteAllPre()">清空回收站</button>
            </div>
            <div style="margin:auto;">
                <el-table :data="tableData" style="width: 930px;margin:auto;" max-height="800" stripe>
                    <el-table-column prop="name" label="问卷名" width="470" align="center" />
                    <el-table-column prop="id" label="问卷ID" width="80" align="center" />
                    <el-table-column prop="time" label="问卷创建时间" width="170" align="center" />
                    <el-table-column prop="used_time" label="答卷数" width="80" align="center" />
                    <el-table-column fixed="right" label="Operations" width="130" align="center">
                        <template #default="scope">
                            <!-- <el-button link type="primary" size="small" @click="handleDeleteData()">清空数据</el-button> -->
                            <el-button link type="primary" size="small"
                                @click="handleRefresh(scope.$index)">恢复</el-button>
                            <el-button link type="primary" size="small"
                                @click="handleDeleteItemPre(scope.$index)">彻底删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

        </div>
        <el-dialog v-model="deleteConfirmOne" title="Warning" width="500" align-center>
            <span>删除后数据无法恢复，确定吗?</span>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="handleNotDeleteItem()">取消</el-button>
                    <el-button type="primary" @click="handleDeleteItem()">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <el-dialog v-model="deleteConfirmAll" title="Warning" width="500" align-center>
            <span>删除后数据无法恢复，确定吗?</span>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="handleNotDeleteAll()">取消</el-button>
                    <el-button type="primary" @click="handleDeleteAll()">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>

        <el-dialog v-model="recycleConfirm" title="Warning" width="500" align-center>
            <span>已经成功恢复，请到控制台查看</span>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="handleRecycleOver()">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>



</template>

<script>
import ConsoleHeader from './ConsoleHeader.vue';
import { getQ, deleteAll, deleteQ, recycleQ } from "../../api/questionnaire/recycle";
import { getUserId } from "../../http/cookies";
import { useRouter } from 'vue-router';
import { ElTable, ElTableColumn, ElButton, ElDialog } from "element-plus"
export default {
    name: "RecycleSite",
    components: {
        ConsoleHeader,
        ElTable, 
        ElTableColumn, 
        ElButton, 
        ElDialog,
    },
    data() {
        return {
            router: useRouter(),
            deleteConfirmOne: false,
            deleteConfirmAll: false,
            recycleConfirm: false,
            choosedIndex: -1,
            tableData: [
                {
                    name: "test",
                    time: "2018年5月21日9:30",
                    used_time: 0,
                    id: 2,
                },
                {
                    name: "fuck",
                    time: "wocenidema",
                    used_time: 10,
                    id: 3,
                }
            ]
        };
    },
    methods: {
        handleToConsole() {
            this.router.push('/console');
        },
        handleGetQ() {
            const data = {};
            data['user_name'] = getUserId();
            getQ(data)
                .then((res) => {
                    console.log(res.data.list);
                    this.tableData = res.data.list;
                    console.log(res.data.status_code);
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        handleDeleteAllPre() {
            this.deleteConfirmAll = true;
        },
        handleNotDeleteAll() {
            this.deleteConfirmAll = false;
        },
        handleDeleteAll() {
            if (this.tableData.length == 0) {
                alert("没有数据可以删除!");
                return;
            }
            const data = {};
            data['user_name'] = getUserId();
            deleteAll(data)
                .then((res) => {
                    this.tableData = [];
                    console.log(res.data.status_code);
                })
                .catch((err) => {
                    console.log(err);
                })
            this.deleteConfirmAll = false;
        },
        handleRefresh(index) {
            this.recycleConfirm = true;
            const data = {};
            data['qn_id'] = this.tableData[index].id;
            recycleQ(data)
                .then((res) => {
                    this.tableData.splice(index, 1);
                    console.log(res.data.status_code);
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        handleRecycleOver() {
            this.recycleConfirm = false;
        },
        handleDeleteItemPre(index) {
            this.choosedIndex = index;
            this.deleteConfirmOne = true;
        },
        handleNotDeleteItem() {
            this.choosedIndex = -1;
            this.deleteConfirmOne = false;
        },
        handleDeleteItem() {
            let index = this.choosedIndex;
            const data = {};
            data['qn_id'] = this.tableData[index].id;
            deleteQ(data)
                .then((res) => {
                    this.tableData.splice(index, 1);
                    console.log(res.data.status_code);
                })
                .catch((err) => {
                    console.log(err);
                })
            this.deleteConfirmOne = false;
        },
    },
    mounted() {
        this.handleGetQ();
    },

}
</script>

<style scoped>
.mybtn {
    margin-bottom: 4px;
    cursor: pointer;
    height: 34px;
    line-height: 34px;
    padding: 0 18px;
    background-color: #fff;
    color: #a8a4a4;
    white-space: nowrap;
    text-align: center;
    font-size: 14px;
    border: none;
    border-radius: 2px;
    transition: all 0.3s;
}

.mybtn:hover {
    color: #0095ff;
}

.background-wrap {
    position: absolute;
    z-index: 100;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.15);
}

.inner-wrap {
    position: absolute;
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    z-index: 200;
    background-color: #fefefe;
    width: 240px;
    height: 130px;
    border-radius: 5px;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.inner-text {
    line-height: 70px;
    text-align: center;
}

.button-wrap {
    text-align: center;
}

.btn {
    height: 32px;
    border: 1px solid #dedede;
    border-radius: 3px;
    padding: 0 15px;
    color: #333;
    background-color: #87ceeb;
    margin-left: 15px;
    margin-right: 15px;
    transition: all 0.3s;
}

.btn:hover {
    color: #fff;
    background-color: #71b3e9;
}
</style>