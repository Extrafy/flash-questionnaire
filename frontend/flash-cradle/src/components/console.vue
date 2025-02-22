<template>
  <div style="position: absolute;width: 100%;height: 100%;background: rgb(249, 251, 255);min-width: 800px;overflow-y: scroll;
 ">
    <ConsoleHeader></ConsoleHeader>

    <el-dialog v-model="dialogFormVisible" title="问卷链接" width="500px">
      <el-form :model="form">
        <el-form-item label="问卷链接:  " :label-width="formLabelWidth">
          <!-- <input v-model="link"></input> -->
          <el-input v-model="link" style="width: 70%" />
          <el-button type="primary" @click="Copytest()" class="button" style="margin-left: 10px;">
            复制链接
          </el-button>
        </el-form-item>
        <el-button color="#ED6A5C" :dark="isDark" @click="Generate_code()" style="margin-left: 72px; width: 119px; color: white">
          生成二维码
        </el-button>
        <el-button color="#F19A39" :dark="isDark" @click="open_questionnaire()"
          style="margin-left: 10px;width: 119px; color: white">
          打开问卷
        </el-button>
        <el-button color="#F9D959" :dark="isDark" @click="shareToPlaza()"
          style="margin-left: 10px; width: 119px; color: white">
          分享到广场
        </el-button>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="Cancel()" class="button">取消</el-button>
          <el-button type="primary" @click="confirmChange()" class="button">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="copyVisiable" title="问卷复制" width="500">
      <el-form :model="form">
        <el-form-item label="问卷标题" :label-width="formLabelWidth">
          <el-input v-model="copyTitle" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="copyTitle = q_list[copyIndex].name">复用原标题</el-button>
          <el-button @click="handleCancelCopy()">取消</el-button>
          <el-button type="primary" @click="handleCopyQ()">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <div class="container">
      <div class="item1">
        <!-- <span style="position: absolute; top:10%; left: 50%; font-size: 20px; font-weight: 600;
            transform: translate(-50%, 0%);">创建问卷</span> -->
        <div class="choose_list">
          <div v-for="choose in choose_list" :key="choose.id" @click="createQ(choose.id)"
            :style="{ '--x': choose.id % 1, '--y': (choose.id / 1) | 0 }" class="choose">
            <div style="position: absolute; width: 100px; height: 100%">
              <span style="
                  position: absolute;
                  top: 20%;
                  left: 20%;
                  font-size: 20px;
                  font-weight: 600;
                ">{{ choose.text }}</span>
              <span style="position: absolute; top: 55%; left: 20%; font-size: 16px; width: 100px;">{{ choose.discribe }}</span>
            </div>
            <div style="
                position: absolute;
                height: 60px;
                top: 20px;
                width: 1px;
                left: 132px;
                background: rgb(158, 166, 172);
              "></div>
            <img :src="choose.img_src" style="
                width: 48px;
                height: 58px;
                position: absolute;
                top: 22px;
                left: 150px;
              " />
            <img :src="`${imgUrl}/assets/create.png`" style="
                width: 70px;
                height: 80px;
                position: absolute;
                top: 10px;
                left: 140px;
                cursor: pointer;
              " class="create" />
          </div>
        </div>
        <div style="
            position: absolute;
            top: calc(7% + 510px);
            right: 50%;
            transform: translate(50%, -50%);
          " id="recycle" @click="handleToRecycle">
          <el-icon>
            <Delete />
          </el-icon>
          <span>回收站</span>
        </div>
      </div>
      <div class="item2">
        <span class="q-total-title">问卷列表</span>
        <div class="sort-list-wrap" @mouseover="show_sort_list" @mouseleave="close_sort_list" style="z-index: 1000">
          <span class="s_list-name" style="right: 390px">{{
            sort_name[sort_option].name
          }}</span>
          <div class="s_list-wrap" style="right: 380px" v-if="sort_list_visible">
            <span v-for="sort_item in sort_name" class="sort_list_item" :key="sort_item.id"
              :style="{ '--i': sort_item.id + 0.2 }" @click="sort_option_change(sort_item.id)">{{ sort_item.name
              }}</span>
          </div>
        </div>
        <div class="state-list-wrap" @mouseover="show_state_list" @mouseleave="close_state_list" style="z-index: 1000">
          <span class="s_list-name" style="right: 310px">{{
            state_name[state_option].name
          }}</span>
          <div class="s_list-wrap" style="right: 300px" v-if="state_list_visible">
            <span v-for="state_item in state_name" class="sort_list_item" :key="state_item.id"
              :style="{ '--i': state_item.id + 0.2 }" @click="state_option_change(state_item.id)">{{ state_item.name
              }}</span>
          </div>
        </div>
        <div class="search-wrap">
          <el-input v-model="searchedValue" style="width: 240px" placeholder="Please input to search" />
        </div>

        <div class="q-list">
          <div class="q_item" v-for="(q_item, index) in paginatedBoxes" :key="index" :style="{ '--i': index + 0.1 }">
            <div class="q-item-top">
              <div class="q-item-top-left">
                <span class="q-item-top-item">{{ q_item.name }}</span>
                <span class="q-item-top-item" id="q_type">{{
                  q_type[q_item.type]
                }}</span>
              </div>
              <div class="q-item-top-right">
                <span class="q-item-top-item">ID:{{ q_item.id }}</span>
                <span class="q-item-top-item">{{
                  state_name[q_item.state].name
                }}</span>
                <span class="q-item-top-item">答卷:{{ q_item.used_time }}</span>
                <span class="q-item-top-item">{{ q_item.time }}</span>
              </div>
            </div>
            <div class="q-item-bottom">
              <div class="q-item-bottom-left">
                <span class="q-item-bottom-item" @click="handleEditQ(index)">
                  <el-icon color="#4b97ce">
                    <Edit />
                  </el-icon>
                  <span>编辑问卷</span>
                </span>
                <span class="q-item-bottom-item" @click="handleShareQ(index)">
                  <el-icon color="#f59917">
                    <Promotion />
                  </el-icon>
                  <span>导出分享</span>
                </span>
                <span class="q-item-bottom-item" @click="handleDataAnalyse(index)">
                  <el-icon color="#627ce5">
                    <Histogram />
                  </el-icon>
                  <span>数据分析</span>
                </span>
                <span class="q-item-bottom-item" @click="handleDataCrossAnalyse(index)">
                  <el-icon color="#627ce5">
                    <Grid />
                  </el-icon>
                  <span>交叉分析</span>
                </span>
              </div>
              <div class="q-item-bottom-right">
                <span class="q-item-bottom-item" v-if="q_item.state === 2" @click="handleReleaseQ(index)">
                  <!-- color="#000" :size="24" id="special-icon" -->
                  <el-icon>
                    <VideoPlay />
                  </el-icon>
                  <span>发布</span>
                </span>
                <span class="q-item-bottom-item" v-if="q_item.state === 1" @click="handlePauseQ(index)">
                  <el-icon>
                    <VideoPause />
                  </el-icon>
                  <span>停止</span>
                </span>
                <span class="q-item-bottom-item" @click="handleCopyQPre(index)">
                  <el-icon>
                    <CopyDocument />
                  </el-icon>
                  <span>复制</span>
                </span>
                <span class="q-item-bottom-item" @click="handleDeleteQ(index)">
                  <el-icon>
                    <Delete />
                  </el-icon>
                  <span>删除</span>
                </span>
              </div>
            </div>
          </div>
          <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :hide-on-single-page="false"
            :total="totalBoxes" layout="prev, pager, next,jumper,total" @current-change="handleCurrentChange"
            style="position: absolute; bottom: 5%; right: 5%" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserId ,imgUrl} from "../../http/cookies";
import ConsoleHeader from "./ConsoleHeader.vue";
import { getQ, releaseQ, pauseQ, deleteQ, copyQ ,shareQ} from "../../api/questionnaire/console";
import { useRouter } from "vue-router";
import { ElMessage, ElButton, ElFormItem, ElDialog, 
  ElForm, ElInput, ElPagination } from "element-plus";
import * as Icons from '@element-plus/icons-vue';
import { ElIcon } from 'element-plus';
import 'element-plus/dist/index.css'
import { ElMessageBox } from "element-plus";
// import { isDark } from '~/composables/dark'
export default {
  name: "ConsoleItem",
  components: {
    ConsoleHeader,
    ElIcon,
    ElButton, 
    ElFormItem, 
    ElDialog, 
    ElForm, 
    ElInput,
    ElPagination,
    ...Icons,
  },
  data() {
    return {
      imgUrl: imgUrl,
      searchedValue: "",
      copyVisiable: false,
      copyTitle: "",
      copyIndex: -1,
      router: useRouter(),
      choose_list: [
        {
          id: 0,
          text: "调查",
          discribe: "创建调查问卷",
          img_src: imgUrl + "/assets/search.png",
        },
        {
          id: 1,
          text: "考试",
          discribe: "创建考试问卷",
          img_src: imgUrl + "/assets/exam.png",
        },
        {
          id: 2,
          text: "投票",
          discribe: "创建投票问卷",
          img_src: imgUrl + "/assets/vote.png",
        },
        {
          id: 3,
          text: "报名",
          discribe: "创建报名问卷",
          img_src: imgUrl + "/assets/gragon.png",
        },
      ],
      sort_name: [
        { id: 0, name: "时间正序" },
        { id: 1, name: "时间倒序" },
      ],
      sort_option: 0,
      sort_list_visible: false,
      state_name: [
        { id: 0, name: "全部" },
        { id: 1, name: "已发布" },
        { id: 2, name: "未发布" },
      ],
      state_option: 0,
      state_list_visible: false,
      q_name: "",
      q_list: [
        {
          id: 0,
          name: "test1",
          state: 1,
          time: "5月21日 10:30",
          used_time: 1,
          type: 1,
        },
        {
          id: 1234234223423,
          name: "test2",
          state: 2,
          time: "5月21日 10:30",
          used_time: 21,
          type: 1,
        },
        {
          id: 3,
          name: "test3",
          state: 2,
          time: "5月21日 10:30",
          used_time: 32,
          type: 1,
        },
        {
          id: 4,
          name: "test14",
          state: 1,
          time: "5月21日 10:30",
          used_time: 32,
          type: 1,
        },
        {
          id: 5,
          name: "test15",
          state: 1,
          time: "5月21日 10:30",
          used_time: 32,
          type: 1,
        },
        {
          id: 6,
          name: "test26",
          state: 2,
          time: "5月21日 10:30",
          used_time: 32,
          type: 1,
        },
        {
          id: 7,
          name: "test36",
          state: 2,
          time: "5月21日 10:30",
          used_time: 32,
          type: 1,
        },
      ],
      user_img: imgUrl + "/assets/search.png",
      currentPage: 1,
      pageSize: 4,
      user_id: "",
      q_type: {
        0: "调查",
        1: "考试",
        2: "投票",
        3: "报名",
        4: "其他",
      },
      dialogFormVisible: false,
      link:'',
      filterOptions:[],
      loading: false,
      sharedIndex: -1,//用于对问卷分享到广场的弹窗
    };
  },
  computed: {
    current_list() {
      let q = [];
      switch (this.state_option) {
        case 0:
          q = this.q_list;
          break;
        case 1:
          for (let i = 0; i < this.q_list.length; i++) {
            if (this.q_list[i].state == 1) {
              q.push(this.q_list[i]);
            }
          }
          break;
        case 2:
          for (let i = 0; i < this.q_list.length; i++) {
            if (this.q_list[i].state == 2) {
              q.push(this.q_list[i]);
            }
          }
          break;
      }
      switch (this.sort_option) {
        case 0:
          q = q.sort((a, b) => {
            if (a.time < b.time) return 1;
            else if (a.time > b.time) return -1;
            else return 0;
          });
          break;
        case 1:
          q = q.sort((a, b) => {
            if (a.time < b.time) return -1;
            else if (a.time > b.time) return 1;
            else return 0;
          });
          break;
      }
      if(this.searchedValue != null && this.searchedValue != ""){
        q = q.filter((item) => {
        return item.name.toLowerCase().includes(this.searchedValue.toLowerCase());
      })
      }
      
      return q;
    },
    totalBoxes() {
      // return this.q_list.length;
      return this.current_list.length;
    },
    paginatedBoxes() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.current_list.slice(startIndex, endIndex);
    },
    titleOptions() {
      let list = [];
      for (let i = 0; i < this.current_list.length; i++) {
        list.push({ 
          name: this.current_list[i].name,
          label: `${this.current_list[i].id}:${this.current_list[i].name}`,
          id: this.current_list[i].id,
        });
      }
      return list;
    },
  },
  methods: {
    createQ(i) {
      console.log("fuck", i);
      this.$router.push({ path: "/create", query: { create_id: i } });
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
    },
    show_sort_list() {
      this.sort_list_visible = true;
    },
    close_sort_list() {
      this.sort_list_visible = false;
    },
    sort_option_change(after_id) {
      this.currentPage = 1;
      this.sort_option = after_id;
      this.sort_list_visible = false;
    },
    show_state_list() {
      this.state_list_visible = true;
    },
    close_state_list() {
      this.state_list_visible = false;
    },
    state_option_change(after_id) {
      this.currentPage = 1;
      this.state_option = after_id;
      this.state_list_visible = false;
    },
    idToTrueIndex(id) {
      for(let i = 0;i<this.q_list.length;i++){
        if(this.q_list[i].id == id){
          return i;
        }
      }
    },
    handleEditQ(index) {
      index  = index + (this.currentPage - 1) * this.pageSize;
      if(this.current_list[index].state == 1 || this.current_list[index].used_time > 0){
        ElMessageBox.alert('该问卷已发布或已回收答卷，请复制问卷再编辑', 'Failed!', {
                confirmButtonText: '确定',
                callback: () => {
                }
              });
        return;
      }
      this.$router.push({ path: "/edit", query: { edit_id: this.current_list[index].id } });
      return index;
    },
    handleShareQ(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      this.sharedIndex = index;
      //index基于current_list
      const tlink1 = window.location.href.replace("/console", "/answer");
      const tlink2 = `?q_id=${this.current_list[index].id}`;
      this.link = tlink1 + tlink2;
      this.dialogFormVisible = true;
      return index;
    },
    handleDataAnalyse(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      //index基于current_list
      this.router.push({path: '/analyse', query: {qnid: this.current_list[index].id}});
    },
    handleDataCrossAnalyse(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      //index基于current_list
      this.router.push({path: '/crossAnalysis', query: {q_id: this.current_list[index].id, q_name: this.current_list[index].name}});
    },
    handleReleaseQ(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      index = this.idToTrueIndex(this.current_list[index].id);
      const data = {};
      data["qn_id"] = parseInt(this.q_list[index].id);
      releaseQ(data)
        .then(res => {
          this.q_list[index].state = 1;
          ElMessage.success("发布成功");
          console.log(res.data.status_code);
        })
        .catch(err => {
          console.log(err);
        })
    },
    handlePauseQ(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      index = this.idToTrueIndex(this.current_list[index].id);
      const data = {};
      data["qn_id"] = parseInt(this.q_list[index].id);
      pauseQ(data)
        .then(res => {
          this.q_list[index].state = 2;
          ElMessage.success("暂停成功");
          console.log(res.data.status_code);
        })
        .catch(err => {
          console.log(err);
        })
    },
    handleCopyQPre(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      index = this.idToTrueIndex(this.current_list[index].id);
      this.copyIndex = index;
      this.copyVisiable = true;
    },
    handleCancelCopy() {
      this.copyIndex = -1;
      this.copyVisiable = false;
      this.copyTitle = '';
    },
    handleCopyQ() {
      let index = this.copyIndex;
      this.copyIndex = -1;
      const data = {};
      data["qn_id"] = parseInt(this.q_list[index].id);
      data["title"] = this.copyTitle;
      copyQ(data)
        .then(res => {
          ElMessageBox.alert('问卷复制成功', 'Success!', {
                confirmButtonText: '确定',
                callback: () => {
                  this.handleGetQ();
                }
              });
          console.log(res.data.status_code);
        })
        .catch(err => {
          console.log(err);
        })
      this.copyVisiable = false;
      this.copyTitle = '';
      return index;
    },
    handleDeleteQ(index) {
      index = index + (this.currentPage - 1) * this.pageSize;
      index = this.idToTrueIndex(this.current_list[index].id);
      if(this.q_list[index].state == 1){
        ElMessageBox.alert('问卷已发布，请停止后再删除', 'Failed!', {
                confirmButtonText: '确定',
                callback: () => {
                }
              });
        return;
      }
      const data = {};
      data["qn_id"] = parseInt(this.q_list[index].id);
      deleteQ(data)
        .then(res => {
          this.q_list.splice(index, 1);
          ElMessage.success("问卷删除成功，请到回收站查看");
          console.log(res);
        })
        .catch(err => {
          console.log(err);
        })
      return index;
    },
    handleGetQ() {
      const data = {};
      data["user_name"] = getUserId();
      getQ(data)
        .then((res) => {
          this.q_list = res.data.list;
          for (let i = 0; i < this.q_list.length; i++) {
            this.q_list[i].time = new Date(this.q_list[i].time);
          }
          console.log(res.data.list)
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleToRecycle() {
      this.router.push('/recycle');
    },
    Copytest() {
      // navigator.clipboard
      //   .writeText(this.link)
      //   .then(() => {
      //     ElMessage.success("复制成功");
      //   })
      //   .catch((err) => {
      //     console.error("Failed to copy text: ", err);
      //   });
      const textToCopy = this.link;
      const textarea = document.createElement("textarea");
      textarea.value = textToCopy;
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      textarea.setSelectionRange(0, 99999);
      try {
        document.execCommand("copy");
        ElMessage.success("复制成功");
      } catch (err) {
        console.error("Failed to copy text: ", err);
      }
      document.body.removeChild(textarea);
    },
    confirmChange() {
      this.dialogFormVisible = false;
      this.sharedIndex = -1;
    },
    Cancel() {
      this.dialogFormVisible = false;
      this.sharedIndex =-1;
      ElMessage.info({
        message: "已取消",
      });
    },
    Generate_code() {
      window.open(
        `https://api.caoliao.net/api/qrcode/code?text=${this.link}`,
        "_blank"
      );
    },
    open_questionnaire() {
      window.open(this.link, "_blank");
    },
    shareToPlaza() {
      const data = {};
      data["qn_id"] = this.q_list[this.sharedIndex].id;
      shareQ(data)
      .then(res => {
        console.log(res.data);
        ElMessage.success("问卷成功分享到广场");
        console.log(res.data.status_code);
      })
      .catch(err => {
        console.log(err);
      })
    },
    remoteMethod(query) {
      if (query) {
        this.loading = true
        setTimeout(() => {
          this.loading = false;
          this.filterOptions = this.titleOptions.filter((item) => {
            return item.name.toLowerCase().includes(query.toLowerCase())
          })
        }, 1000)
      } else {
        this.filterOptions = [];
      }
    },
    toSearchedPage() {
      console.log("this.searchedValue, ", this.searchedValue);
      let li = this.searchedValue['0'].split(":");
      let data = {};
      data['id'] = parseInt(li[0]);
      data['name'] = li[1];
      for(let i = 0; i< this.current_list.length; i++){
        if(data.id === this.current_list[i].id){
          this.currentPage = i/4 + 1;
        }
      }
    },
  },
  mounted() {
    this.user_id = getUserId();
    console.log("user_id: ", this.user_id);
    this.handleGetQ();
  },
}
</script>

<style scoped>
#recycle {
  display: flex;
  width: 220px;
  line-height: 40px;
  cursor: pointer;
  transition: all 0.5s;
  align-items: center;
  justify-content: center;
}

#recycle:hover {
  background-color: #f0f0f0;
}

.q-total-title {
  position: absolute;
  font-size: 20px;
  font-weight: 600;
  top: 40px;
  left: 0px;
}

.s_list-wrap {
  position: absolute;
  top: 63px;
  width: 80px;
  background-color: white;
  box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);
}

.s_list-name {
  position: absolute;
  color: grey;
  font-size: 14px;
  top: 43px;
  height: 30px;
  width: 60px;
  text-align: center;
  cursor: pointer;
}

.sort_list_item {
  display: inline-block;
  /* 设置为内联块级元素 */
  line-height: 30px;
  /* 与容器高度相同，实现垂直居中 */
  position: absolute;
  top: calc(var(--i) * 30px);
  font-size: 14px;
  height: 30px;
  width: 80px;
  text-align: center;
  background: white;
  z-index: 1000;
  cursor: pointer;
}

.sort_list_item:hover {
  display: inline-block;
  /* 设置为内联块级元素 */
  line-height: 30px;
  /* 与容器高度相同，实现垂直居中 */
  position: absolute;
  top: calc(var(--i) * 30px);
  font-size: 14px;
  height: 30px;
  width: 80px;
  text-align: center;
  background: #aaaaaa;
  z-index: 1000;
}

.search-wrap {
  position: absolute;
  right: 90px;
  top: 38px;
  height: 30px;
  width: 200px;
  /* background: white;
  box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);
  border-radius: 15px; */
}

#screen {
  position: absolute;
  font-size: 14px;
  outline: none;
  border: none;
  top: 6px;
  left: 5px;
}

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

body {
  margin: 0;
  padding: 0;
}

.container {
  position: absolute;
  width: 100%;
  top: 7%;
  height: 93vh;
}

.item1 {
  position: absolute;
  width: 30%;
  height: 100%;
}

.item2 {
  position: absolute;
  left: 30%;
  width: 70%;
  height: 100%;
}

.choose_list {
  position: absolute;
  width: 280px;
  height: 500px;
  left: 50%;
  top: 10%;
  transform: translate(-50%, 0%);
}

.choose {
  position: absolute;
  top: calc(var(--y) * 120px);
  /* left: calc(var(--x)*220px); */
  left: 30px;
  background-color: white;
  border-radius: 3px;
  width: 230px;
  height: 100px;
  box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

.create {
  opacity: 0;
}

.choose:hover .create {
  opacity: 1;
}

.q-list {
  position: absolute;
  left: 0px;
  top: 100px;
  height: 550px;
  width: 95%;
  overflow-y: auto;
  z-index: 10;
}

.q_item {
  width: 99%;
  min-width: 570px;
  height: 100px;
  left: 0.5%;
  background: #fff;
  box-shadow: 0px 0px 4px 0px #f0f0f0;
  border: 1px solid #e6e6e6;
  border-radius: 2px;
  position: absolute;
  top: calc(var(--i) * 120px);
}

#q_type {
  background: #e3eefa;
  color: #008cf0;
  height: 20px;
  background: #ebf4fa;
  border-radius: 3px;
  padding: 0 4px;
  display: inline-block;
  line-height: 20px;
  font-size: 12px;
  vertical-align: top;
  margin-top: 1px;
}

.q-item-top {
  padding: 13px 24px 0;
  font-size: 16px;
  height: 22px;
  line-height: 22px;
  color: #262626;
}

.q-item-top-left {
  font-size: 16px;
  float: left !important;
}

.q-item-top-left .q-item-top-item {
  margin-right: 7px;
}

.q-item-top-right {
  font-size: 13px;
  margin-right: 10px;
  float: right !important;
}

.q-item-top-right .q-item-top-item {
  margin-right: 10px;
}

.q-item-top-item {}

.q-item-bottom {
  margin: 0 24px 0;
  height: 36px;
  line-height: 36px;
  padding: 18px 0 18px;
  border-top: 1px solid #f5f5f5;
}

.q-item-bottom-left {
  line-height: 36px;
  float: left !important;
}

.q-item-bottom-item {
  position: relative;
  text-align: center;
  margin-right: 30px;
  cursor: pointer;
  color: #7a7a7a;
  transition: all 0.3s;
}

.q-item-bottom-item:hover {
  color: #008cf0;
}

.q-item-bottom-left .q-item-bottom-item {
  margin-right: 0;
  margin-left: 20px;
}

.q-item-bottom-right .q-item-bottom-item span {
  font-size: 13px;
}

.q-item-bottom-left .q-item-bottom-item span {
  font-size: 14px;
}

.q-item-bottom-left .q-item-bottom-item .el-icon {
  position: absolute;
  top: 15%;
  left: -30%;
}

.q-item-bottom-right .q-item-bottom-item .el-icon {
  position: absolute;
  top: 17%;
  left: -65%;
}

.q-item-bottom-right .q-item-bottom-item #special-icon {
  top: 0%;
  left: -92%;
}

.q-item-bottom-left .q-item-bottom-item {
  margin-right: 10px;
}

.q-item-bottom-right {
  line-height: 36px;
  float: right !important;
}
</style>
