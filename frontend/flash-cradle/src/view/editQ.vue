<template>
  <div style="width: 100%; height: 100%; background: rgb(249, 251, 255)">
    <div>
      <ConsoleHeader></ConsoleHeader>
      <div class="container">
        <div class="bian">
          <div style="width: 100%; height: 3%"></div>
          <div class="kuang" style="text-align: center">
            <!-- <div :style="title.style" style="
                display: inline-block;
                width: 90%;
                margin-left: 3%;
                text-align: center;
              " class="input_div" contenteditable="true" @input="handleInput(-2, 0, $event)">
              {{ title.description }}
            </div> -->
            <input v-model="title.description" style="
                display: inline-block;
                width: 90%;
                margin-left: 3%;
                text-align: center;
                font-size: 24px;" />
            <!-- <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit" @click="changeTextStyle(-2, 0)" /> -->
          </div>
          <div class="kuang">
            <div :style="jianjie.style" style="display: inline-block; width: 90%; margin-left: 3%" class="input_div"
              contenteditable="false" @input="handleInput(-1, 0, $event)">
              <v-md-preview :text="jianjie.description"></v-md-preview>
            </div>
            <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit" @click="changeMarkdownStyle(jianjie)" />
          </div>
          <div style="
              width: 100%;
              height: 1px;
              background-color: rgba(220, 220, 220, 1);
            "></div>

          <div v-for="(q, index) in list" :key="index" style="width: 92%; margin-left: 4%">
            <div style="width: 100%; height: 20px"></div>
            <div style="border: 1px solid rgba(200, 200, 200, 0.6); border-radius: 3px;">
            <div class="kuang" style="margin-left: 2%;">
              <div class="title_wrap">
                <span style="width: 10px; padding-bottom: 10px; color: #ff4040" v-if="q.must === true">*</span>
                <span class="ti_title" style="font-size: 18px" :class="{ must: q.must }">{{ index + 1 }}.
                </span>
                <div style="display: inline-block; width: 60%" class="input_div" contenteditable="false"
                  @input="handleInput(index, 0, $event)">
                  <v-md-preview class="v-md-preview" :text="q.description"></v-md-preview>
                </div>
                <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit" title="编辑题目"
                  @click="changeMarkdownStyle(q)" />
                <font-awesome-icon v-if="q.type === 0 || q.type === 1" :icon="['fas', 'plus']" class="edit" title="添加选项"
                  style="font-size: 18px" @click="handleAddItem(index)" />
                <font-awesome-icon :icon="['fas', 'xmark']" class="edit" title="删除题目" style="font-size: 21px"
                  @click="handleDelTitle(index)" />
                  <div style="display: flex; " v-if="type == 1">
                    <span style="margin-top: 5px;">分值：</span>
                    <input style="width: 50px;height: 10px;" type="number" v-model="q.img_url">
                  </div>

              </div>

              <div class="item_wrap" v-if="q.type === 0 || q.type === 1">

                <div v-for="(item, index_item) in q.options" :key="index_item"
                  style="margin-left: 20px;margin-top: 10px; display: flex; align-items: center">
                  <!-- <span v-if="index_item != 0" class="item-title">{{ index_item }}.</span> -->
                  <input type="radio" :checked="item.choosed" class="checkedKuang" :class="{
              checked: item.choosed,
              multi: q.type === 1,
            }" @click="handleChoose(index, index_item)" />
                   <el-input  v-model="item.content" style="width: 60%;" :autosize="{ minRows: 1, maxRows: 4 }" type="textarea" placeholder="please input content"/>
                  <!-- <font-awesome-icon v-if="index_item != 0" :icon="['fas', 'pen-to-square']" class="edit" title="编辑选项"
                    @click="changeTextStyle(index, index_item)" /> -->
                  <font-awesome-icon :icon="['fas', 'xmark']" class="edit" title="删除选项" style="font-size: 21px"
                    @click="handleDelItem(index, index_item)" />
                  <div style="display: flex; " v-if="type == 3&&q.img_url">
                    <span style="margin-top: 5px;">最大人数：</span>
                    <input style="width: 50px;height: 10px;" type="number" v-model="item.arg">
                  </div>
                </div>

                <div class="select-wrap" v-if="q.type === 1">
                  <div class="select-wrap-item">
                    <span>至少选</span>
                    <select title="至少选几项" v-model="q.arg1" class="custom-select">
                      <option v-for="(item, index_option) in q.options.length" :key="index_option"
                        :disabled="q.arg2 < index_option + 1" class="option-item">
                        {{ index_option + 1 }}
                      </option>
                    </select>
                    <span>项</span>
                  </div>
                  <div class="select-wrap-item">
                    <span>至多选</span>
                    <select title="至多选几项" v-model="q.arg2" class="custom-select">
                      <option v-for="(item, index_option) in q.options.length" :key="index_option"
                        :disabled="q.arg1 > index_option + 1" class="option-item">
                        {{ index_option + 1 }}
                      </option>
                    </select>
                    <span>项</span>
                  </div>
                </div>
              </div>
              <div class="rate-wrap" v-if="q.type === 2" style="margin-top: 10px; margin-left: 30px">
                <div class="rate-block">
                  <el-rate style="--el-rate-icon-size: 30px" show-score :max="q.arg2" :size="10"
                    :void-icon="rateStyleList[q.arg1].icons[0]" :icons="{
              [q.arg2 / 3]: rateStyleList[q.arg1].icons[0],
              [(q.arg2 * 2) / 3]: rateStyleList[q.arg1].icons[1],
              [q.arg2]: rateStyleList[q.arg1].icons[2],
            }" :colors="{
              [q.arg2 / 3]: rateStyleList[q.arg1].colors[0],
              [(q.arg2 * 2) / 3]: rateStyleList[q.arg1].colors[1],
              [q.arg2]: rateStyleList[q.arg1].colors[2],
            }" v-model="q.arg3" />
                </div>

                <div class="rate-theme-option" style="
                    margin-top: 10px;
                    position: absolute;
                    display: flex;
                    align-items: center;
                  ">
                  <el-icon v-if="q.arg1 === 0" :size="20" class="rate-theme-item-option" color="#f7ba2a">
                    <Star />
                  </el-icon>
                  <el-icon v-else :size="20" class="rate-theme-item-option" @click="handleChangeRateTheme(index, 0)">
                    <Star />
                  </el-icon>

                  <el-icon v-if="q.arg1 === 1" :size="20" class="rate-theme-item-option" color="#f7ba2a">
                    <Cloudy />
                  </el-icon>
                  <el-icon v-else :size="20" class="rate-theme-item-option" @click="handleChangeRateTheme(index, 1)">
                    <Cloudy />
                  </el-icon>

                  <el-icon v-if="q.arg1 === 2" :size="20" class="rate-theme-item-option" color="#f7ba2a">
                    <ChatRound />
                  </el-icon>
                  <el-icon v-else :size="20" class="rate-theme-item-option" @click="handleChangeRateTheme(index, 2)">
                    <ChatRound />
                  </el-icon>

                  <el-icon v-if="q.arg1 === 3" :size="20" class="rate-theme-item-option" color="#f7ba2a">
                    <Watermelon />
                  </el-icon>
                  <el-icon v-else :size="20" class="rate-theme-item-option" @click="handleChangeRateTheme(index, 3)">
                    <Watermelon />
                  </el-icon>
                  <span style="display: inline-block; padding-left: 10px">评分项数</span>
                  <select title="最大值:" style="height: 22px" v-model="q.arg_tmp" class="custom-select"
                    @change="handleChangeRateNum(index)">
                    <option v-for="(item, index_option) in 8" :key="index_option" class="option-item">
                      {{ index_option + 5 }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="easy-answer" v-if="q.type === 3">

                <textarea style="
                    width: 90%;
                    min-height: calc(2em + 2px);
                    padding: 8px;
                    font-size: 16px;
                    line-height: 1.5;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                    resize: vertical;
                    cursor: not-allowed;
                    margin-left: 24px;
                  " placeholder="请输入内容..." v-model="q.arg3"></textarea>
              </div>
              <div v-if="q.type === 2" class="button-wrap" style="margin-left: 24px; margin-top:40px;">
                <el-button @click="handleMoveUp(index)">上移</el-button>
                <el-button @click="handleMoveDown(index)">下移</el-button>
                <el-switch v-model="q.must" class="edit-special" size="large" inline-prompt active-text="必选"
                  inactive-text="可选" />
              </div>
              <div v-else class="button-wrap" style="margin-left: 24px; margin-top:6px;">
                <el-button @click="handleMoveUp(index)">上移</el-button>
                <el-button @click="handleMoveDown(index)">下移</el-button>
                <el-switch v-model="q.must" class="edit-special" size="large" inline-prompt active-text="必选"
                  inactive-text="可选" />
                <el-switch v-model="q.img_url" class="edit-special" size="large" inline-prompt active-text="投票题"
                  inactive-text="非投票" v-if="type==2&&(q.type == 1||q.type == 0)"/>
                <el-switch v-model="q.img_url" class="edit-special" size="large" inline-prompt active-text="报名题"
                  inactive-text="非报名" v-if="type==3&&(q.type == 1||q.type == 0)"/>
              </div>
            </div>

            
          </div>
          <div style="width: 100%; height: 10px"></div>
          </div>

          <div style="
              display: flex;
              justify-content: center;
              margin: 20px 0px;
              width: 100%;
            ">
            <div style="display: flex; justify-content: center; width: 700px">
              <div style="width: 100px" @click="createTi(0)">
                <font-awesome-icon :icon="['fas', 'check']" style="color: blue" />
                <span style="margin-left: 5px; cursor: pointer">单选题</span>
              </div>
              <div style="width: 100px" @click="createTi(1)">
                <font-awesome-icon :icon="['fas', 'check-double']" style="color: blue" />
                <span style="margin-left: 5px; cursor: pointer">多选题</span>
              </div>
              <div style="width: 100px" @click="createTi(2)">
                <font-awesome-icon :icon="['fas', 'i']" style="color: blue" />
                <span style="margin-left: 5px; cursor: pointer">评分题</span>
              </div>
              <div style="width: 100px" @click="createTi(3)">
                <font-awesome-icon :icon="['fas', 'i']" style="color: blue" />
                <span style="margin-left: 5px; cursor: pointer">填空题</span>
              </div>
            </div>
          </div>
        </div>
        <span class="warning_edit">{{ this.warning }}</span>
        <button type="button" @click="handleCreateQuestionnaire()" id="createQsButton">
          创建问卷
        </button>
      </div>
    </div>

    <div class="tanchuang" v-if="md_show == 1">
      <button id="mdExitButton" type="button" @click.prevent="exitMdEditor()">
        exit
      </button>
      <div class="mdWindow">
        <VueMarkdownEditor v-model="cur_element.description" height="100%"></VueMarkdownEditor>
      </div>
    </div>
    <div class="submit">
      <span style="position: absolute; left: 50%; top:10px;transform: translate(-50%, 0); 
            font-size: 20px; font-weight: 600; color: #0095ff; width: 100%; text-align: center">
        限制截止时刻</span>
      <div class="start_choose">
        <el-date-picker v-model="start_time" type="datetime" placeholder="选择起始时间">
        </el-date-picker>
        <div style="width: 10px; height: 15px;"></div>
        <el-date-picker v-model="end_time" type="datetime" placeholder="选择结束时间">
        </el-date-picker>
      </div>
    </div>
    <div class="cover_submit" v-if="!have_time && md_show!=1"></div>
    <span class="time_warning" v-if="(start_time > end_time)&&have_time">起始时间不能大于终止时间</span>
    <div class="have_time">
      <el-switch v-model="have_time" size="large" inline-prompt active-text="设置限时"
                  inactive-text="设置限时" />
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
import ConsoleHeader from "@/components/ConsoleHeader.vue";
import { getUserId ,imgUrl} from "../../http/cookies";
import { createQ, editQFetch, editQSend } from "../../api/questionnaire/editQ";
import { useRouter } from 'vue-router';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { ElInput,  ElRate, ElIcon, ElButton, ElSwitch, ElDatePicker } from 'element-plus'
import * as Icons from '@element-plus/icons-vue';
import { ElMessageBox } from "element-plus";
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// Introduce the theme you use. Take the github theme as an example here
import githubTheme from '@kangc/v-md-editor/lib/theme/github';
import '@kangc/v-md-editor/lib/theme/style/github.css';
// highlightjs
import hljs from 'highlight.js';
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';
VueMarkdownEditor.use(vuepressTheme, {
  Prism,
});

export default {
  name: "EditQ",
  components: {
    ConsoleHeader,
    ChatRound,
    Watermelon,
    Star,
    Cloudy,
    FontAwesomeIcon,
    ElInput,  
    ElRate, 
    ElIcon, 
    ElButton, 
    ElSwitch,
    ElDatePicker,
    ...Icons,
    VMdPreview,
    VueMarkdownEditor,
  },
  data() {
    return {
      imgUrl: imgUrl,
      edit_id: -1,
      isChangeEdit: false,
      router: useRouter(),
      user_img: imgUrl + "/assets/search.png",
      title: {},
      jianjie: {},
      type: 0,
      list: [],
      tan_show: 0,
      md_show: 0,
      cur_element: {},
      cur_change: [0, 0],
      cur_style: {},
      show_font_size: 0,
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
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date());
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', date);
          }
        }]
      },
      start_time: new Date(),
      end_time: new Date(),
      have_time: false,
      warning: '',
      error_timer: '',
    };
  },
  methods: {
    changeMarkdownStyle(element) {
      this.cur_element = element;
      this.md_show = 1;
    },
    changeTextStyle(i, j) {
      this.cur_change[0] = i;
      this.cur_change[1] = j;
      if (i == -2) {
        this.cur_style = this.title;
      } else if (i == -1) {
        this.cur_style = this.jianjie;
      } else {
        this.cur_style = this.list[i].content[j];
      }
      this.tan_show = 1;
    },
    handleInput(i, j, event) {
      console.log(i, j, event);
      if (i == -3) {
        this.cur_style.description = event.target.innerText;
      } else if (i == -2) {
        this.title.description = event.target.innerText;
      } else if (i == -1) {
        this.jianjie.description = event.target.innerText;
      } else {
        this.list[i].options[j].content = event.target.innerText;
      }
    },
    cancelChange() {
      this.tan_show = 0;
      this.show_font_size = 0;
    },
    changeBold() {
      if (this.cur_style.style.fontWeight == 500) {
        this.cur_style.style.fontWeight = 600;
      } else {
        this.cur_style.style.fontWeight = 500;
      }
    },
    changeUnderline() {
      if (this.cur_style.style.textDecoration == "none") {
        this.cur_style.style.textDecoration = "underline";
      } else {
        this.cur_style.style.textDecoration = "none";
      }
    },
    changeItalic() {
      if (this.cur_style.style.fontStyle == "normal") {
        this.cur_style.style.fontStyle = "italic";
      } else {
        this.cur_style.style.fontStyle = "normal";
      }
    },
    showFontSize() {
      this.show_font_size = 1;
    },
    chooseFontSize(i) {
      this.cur_style.style.fontSize = i;
      this.show_font_size = 0;
    },
    createTi(i) {
      let isTou = 1;
      if(this.type == 2||this.type == 3){
        isTou = false;
      }
      if (i == 0 || i == 1) {
        let tmp = "单选题";
        if (i == 1) {
          tmp = "多选题";
          this.list.push({
            type: i,
            arg1: 1,
            arg2: 2,
            arg3: '',
            must: true,
            description: tmp,
            img_url: isTou,
            video_url: "",
            options: [
              {
                content: "选项",
                choosed: false,
                arg: 0,
              },
              {
                content: "选项",
                choosed: false,
                arg: 0,
              },
            ],
          });
        } else
          this.list.push({
            type: i,
            arg1: 1,
            arg2: 1,
            arg3: '',
            must: true,
            description: tmp,
            img_url: isTou,
            video_url: "",
            options: [
              {
                content: "选项",
                choosed: false,
                arg: 0,
              },
              {
                content: "选项",
                choosed: false,
                arg: 0,
              },
            ],
          });
      } else {
        let tmp = "评分题";
        if (i == 3) {
          tmp = "填空题";
          this.list.push({
            type: i,
            arg1: 1,
            arg2: 1,
            arg3: '',
            must: true,
            description: tmp,
            img_url: isTou,
            video_url: "",
            options: [],
          });
        } else
          this.list.push({
            type: i,
            arg1: 0, //style类型
            arg2: 5, //评分上限
            arg3: 0,  //评分
            arg_tmp: 5,
            must: true,
            description: tmp,
            img_url: isTou,
            video_url: "",
            options: [],
          });
      }
    },
    exitMdEditor() {
      this.md_show = 0;
    },
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
        this.list[index].options[index_item].choosed =
          !this.list[index].options[index_item].choosed;
      }
    },
    handleAddItem(index) {
      this.list[index].options.push({
        content: "选项",
        choosed: false,
        arg: 0,
      });
    },
    handleDelTitle(index) {
      this.list.splice(index, 1);
    },
    handleDelItem(index, index_item) {
      if (this.list[index].options.length === 2) {
        alert("请至少保留一个选项!");
        return;
      }
      this.list[index].options.splice(index_item, 1);
    },
    handleMoveUp(index) {
      if (index === 0) return;
      let tmp = this.list[index];
      this.list[index] = this.list[index - 1];
      this.list[index - 1] = tmp;
    },
    handleMoveDown(index) {
      if (index === this.list.length - 1) return;
      let tmp = this.list[index];
      this.list[index] = this.list[index + 1];
      this.list[index + 1] = tmp;
    },
    handleChangeRateTheme(index, num) {
      this.list[index].arg1 = num;
    },
    handleChangeRateNum(index) {
      this.list[index].arg2 = parseInt(this.list[index].arg_tmp);
    },
    error_lookup(){
      if(this.title.description.length>256){
        this.warning = '标题过长'
        return ;
      }
      if(this.jianjie.description.length>256){
        this.warning = '简介过长'
        return ;
      }
      for (let i = 0 ; i < this.list.length ; i++){
        if(this.list[i].description.length > 256){
          this.warning = '第' + (i+1) + '题题目过长';
          return ;
        }
        for(let j = 0 ; j < this.list[i].options.length ; j++){
          if(this.list[i].options[j].content.length > 256){
            this.warning = '第' + (i+1) + '题选项过长';
            return ;
          }
        }
      }
    },  
    getFormedList() {
      let formList = [];
      for (let i = 0; i < this.list.length; i++) {
        if(this.type != 0){
          this.list[i].img_url = String(this.list[i].img_url);
        }
        if (this.list[i].type === 2) {
          formList.push({
            type: this.list[i].type,
            arg1: this.list[i].arg1,
            arg2: this.list[i].arg2,
            arg3: this.list[i].arg3.toString(),
            description: this.list[i].description,
            must: this.list[i].must,
            img_url: this.list[i].img_url,
            video_url: this.list[i].video_url,
            options: [],
          });
        }
        else if (this.list[i].type == 0 || this.list[i].type == 1) {
          if (this.type == 3) {
            let tmp = '';
            for (let j = 0; j < this.list[i].options.length; j++) {
              if (tmp == '') {
                tmp = this.list[i].options[j].arg.toString();
              }
              else {
                tmp = [tmp, this.list[i].options[j].arg.toString()].join('&_&');
              }
            }
            this.list[i].arg3 = tmp;
          }
          else if (this.type == 1) {
            let tmp = '';
            for (let j = 0; j < this.list[i].options.length; j++) {
              if (this.list[i].options[j].choosed) {
                if (tmp == '') {
                  tmp = j.toString();
                }
                else {
                  tmp = [tmp, j.toString()].join('%&%');
                }
              }
            }
            this.list[i].arg3 = tmp;
          }
          formList.push(this.list[i]);
        } else formList.push(this.list[i]);
      }
      return formList;
    },
    handleCreateQuestionnaire() {
      this.warning = '';
      clearTimeout(this.error_timer);
      this.error_lookup();
      if (this.warning != ''){
        this.error_timer = setTimeout(() => this.warning = '', 3000);
        return ;
      }
      const qs = {};
      qs["username"] = getUserId();
      qs["title"] = this.title.description;
      qs["description"] = this.jianjie.description;
      qs["type"] = this.type;
      qs["list"] = this.getFormedList();
      qs["fuck_time"] = this.start_time.toISOString();
      qs["finished_time"] = this.end_time.toISOString();
      if(!this.have_time){
        qs["fuck_time"] = '';
        qs["finished_time"] = '';
      }
      console.log("created_qs", qs);
      if ((this.start_time > this.end_time)&&this.have_time) {
        return;
      }
      if(this.isChangeEdit){
        qs['old_ID'] = parseInt(this.edit_id);
        editQSend(qs)
        .then(res => {
          switch (res.data.status_code) {
            case 1:
              // this.router.push('/console');
              ElMessageBox.alert('问卷编辑成功,跳转至控制台', 'Success!', {
                confirmButtonText: '确定',
                callback: () => {
                  this.router.push('/console');
                }
              });
              break;
            case 2:
              alert("用户不存在或未登录");
              break;
            case -1:
              alert("数据格式错误");
              break;
            case -2:
              alert("请求类型错误");
              break;
            default:
              console.log("res.data", res.data);
              alert(res.data.message);
              break;
          }
        })
      }else {
        createQ(qs)
        .then((res) => {
          switch (res.data.status_code) {
            case 1:
            ElMessageBox.alert('问卷创建成功,跳转至控制台', 'Success!', {
                confirmButtonText: '确定',
                callback: () => {
                  this.router.push('/console');
                }
              });
              break;
            case 2:
              alert("传输数据格式错误");
              break;
            case -1:
              alert("用户未登录");
              break;
            case -2:
              alert("请求类型错误");
              break;
            default:
              alert(res.data.status_code);
              break;
          }
        })
        .catch((err) => {
          console.log(err);
        });
      }
      
    },
    handleGetQ(){
      let data = {};
      data['qn_id'] = this.edit_id;
      editQFetch(data)
      .then(res => {
        console.log(res.data);
        data = res.data;
        this.title.description = data.title;
      this.jianjie.description = data.description;
      this.type = parseInt(data.type);
      this.end_time = data.finished_time;
      this.start_time = data.fuck_time;
      if(this.end_time == undefined){
        this.end_time = new Date();
      }
      if(this.start_time == undefined){
        this.start_time = new Date();
      }
      this.list = data.question_list;
      for(let i=0; i<this.list.length;i++){
        this.list[i].type = parseInt(this.list[i].type);
        console.log("this.type ", this.type, this.list[i].img_url)
        if(this.type == 1){
          this.list[i].img_url = parseInt(this.list[i].img_url);
        }
      }
      console.log(this.list);
      console.log(data.status_code);
      })
      .catch(err => {
        console.log(err);
      })
    },
    autoResize(textarea) {
            console.log(textarea.style);
            textarea.style.height = 'auto'; // 重置高度
            textarea.style.height = textarea.scrollHeight + 'px'; // 设置新的高度
    },
  },
  computed: {},
  mounted() {
    library.add(fas);
    this.title = {
      style: {
        fontSize: "24px",
        color: "#000000",
        fontWeight: "600",
        fontStyle: "normal",
        textDecoration: "none",
      },
      description: this.$route.query.q_name,
    };
    this.jianjie = {
      style: {
        fontSize: "18px",
        color: "#000000",
        fontWeight: "500",
        fontStyle: "normal",
        textDecoration: "none",
      },
      description: "问卷描述",
    };
    this.type = parseInt(this.$route.query.create_id);
    this.edit_id = this.$route.query.edit_id;
    if(this.$route.query.edit_id == undefined){
      this.edit_id = -1;
    }
    if(this.edit_id != -1){
      this.handleGetQ();
      this.isChangeEdit = true;
    }
  },
};
</script>
<style>
.github-markdown-body {
  padding: 0 !important;
}

el-rate {
  --el-rate-icon-size: 16px;
}
.el-textarea textarea{
  resize: none !important;
}
.rate-theme-item-option:hover {
  color: #87ceeb;
  cursor: pointer;
  transition: all 0.3s;
}
</style>

<style scoped>
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

.select-wrap {
  margin-left: 26px;
}

.select-wrap-item {
  margin: 5px, 10px;
  border-radius: 0;
  display: inline-block;
  margin-right: 30px;
}

.custom-select {
  appearance: none;
  height: 28px;
  width: 24px;
  text-align: center;
  font-size: 18px;
  /* Font size */
  color: black;
  border: none;
  /* Border */
  background-color: #fff;
  /* Rounded corners */
  background-color: white;
  /* Background color */
  cursor: pointer;
  /* Pointer cursor */
}

.option-item {
  color: #0095ff;
}

.option-item:disabled {
  color: #f27575;
}

.edit {
  display: none;
  margin-left: 12px;
  cursor: pointer;
}

.kuang:hover .edit {
  display: inline;
  color: rgba(120, 120, 120, 0.6);
}

.edit-special {
  display: inline-flex;
  margin-left: 12px;
}

.kuang:focus {
  background-color: rgb(211, 211, 211);
}

.top_lan {
  width: 100%;
  height: 8vh;
  position: absolute;
  background-color: white;
  box-shadow: 0px 0px 2px 2px rgba(0, 0, 0, 0.5);
}

.container {
  position: absolute;
  width: 100%;
  top: 7%;
  height: 93vh;
}

.warning_edit{
  display: flex;
  position: absolute;
  top: 85%;
  left: 83%;
  height: 45px;
  width: 150px;
  font-size: 16px;
  justify-content: center;
  align-items: center;
  color: red;
}

#createQsButton {
  display: flex;
  position: absolute;
  top: 90%;
  left: 85%;
  height: 45px;
  width: 90px;
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

.bian {
  position: absolute;
  width: 800px;
  height: 94%;
  top: 3%;
  background-color: white;
  right: 50%;
  transform: translate(50%, 0);
  border-radius: 5px;
  overflow: scroll;
}

.bian::-webkit-scrollbar {
  display: none;
}

input {
  border: 0px solid;
  padding: 10px;
  background-color: white;
}

input:hover {
  border: 1px solid;
}

textarea {
  border: 0px solid;
  padding: 10px;
  background-color: white;
  resize: none;
}

textarea:hover {
  border: 1px solid;
}

input:focus {
  border: 1px solid;
  outline: 1px solid transparent;
}

textarea:focus {
  border: 1px solid;
  outline: 1px solid transparent;
}

.tanchuang {
  position: absolute;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  /* 半透明黑色背景 */
}

#mdExitButton {
  position: absolute;
  top: 1.2%;
  left: 93%;
  display: inline-block;
  height: 30px;
  width: 50px;
  border: none;
  border-radius: 5px;
  background-color: #87ceeb;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.5s ease, color 0.5s ease, box-shadow 0.5s ease;
  cursor: pointer;
}

#mdExitButton:hover {
  background-color: #71b3e9;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.nei {
  position: absolute;
  top: 50%;
  right: 50%;
  transform: translate(50%, -50%);
  z-index: 2;
  background-color: #fefefe;
  width: 600px;
  height: 400px;
  border-radius: 5px;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.mdWindow {
  position: absolute;
  top: 50%;
  right: 50%;
  transform: translate(50%, -50%);
  z-index: 2;
  /* background-color: #fefefe; */
  width: 85%;
  height: 88%;
  border-radius: 5px;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.before_class {
  font-size: 16px;
  margin: 6px;
  color: rgba(60, 60, 60, 1);
}

.after_class {
  font-size: 16px;
  margin: 6px;
  color: blue;
}

.changeCur {
  width: 100%;
  padding: 0px;
  border: none;
  text-align: center;
  background-color: white;
  height: 275px;
  position: absolute;
  top: 30px;
}

.font_sizes {
  width: 150px;
  margin: 5px;
  text-align: center;
  display: block;
}

.font_sizes_choosed {
  width: 150px;
  margin: 5px;
  text-align: center;
  display: block;
  background-color: rgba(200, 200, 200, 0.6);
}

.font_sizes:hover {
  background-color: rgba(200, 200, 200, 0.6);
}

.ti_title {
  margin-left: 10px;
  padding-bottom: 12px;
}

.ti_title.must {
  margin-left: 0;
}

.input_div {
  padding: 10px;
  /* 设置文字与边框的内边距为 10px */
  outline: none;
  /* 移除默认的外边框 */
}

.input_div:hover {
  border: 1px solid rgba(200, 200, 200, 0.8);
  /* 设置边框样式 */
}

.input_div:focus {
  border: 1px solid rgba(200, 200, 200, 0.8);
  /* 设置边框样式 */
}

.submit {
  position: fixed;
  top: 10%;
  left: 2%;
  width: 250px;
  height: 150px;
  background: white;
  box-shadow: 0px 0px 1px 1px rgba(200, 200, 200, 0.8);
  border-radius: 3px;
}

.cover_submit {
  position: fixed;
  top: 10%;
  left: 2%;
  width: 250px;
  height: 150px;
  background: rgba(245, 245, 245, 0.5);
  z-index: 100;
  border-radius: 3px;
}

.time_warning {
  position: fixed;
  top: 28%;
  left: 2%;
  width: 250px;
  text-align: center;
  font-size: 16px;
  color: red;
}

.have_time {
  position: fixed;
  top: 30%;
  left: 2%;
  width: 250px;
  text-align: center;
  font-size: 16px;
  color: red;
}

.start_choose {
  position: absolute;
  top: 35%;
  right: 50%;
  transform: translate(50%, 0);
}
</style>
