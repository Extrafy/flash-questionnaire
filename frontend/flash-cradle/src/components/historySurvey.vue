<template>
  <div
    class="wrapper"
    @mouseenter="isHovering = true"
    @mouseleave="isHovering = false"
    :style="blockStyle"
  >
    <el-dialog v-model="purchaseVisiable" title="问卷浏览" width="500">
      <el-form :model="form">
        <el-form-item label="我的闪电币:" :label-width="formLabelWidth">
          <span> {{ leftMoney }} </span>
        </el-form-item>
        <el-form-item label="需要闪电币:" :label-width="formLabelWidth">
          <span> 3 </span>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCancel()">取消</el-button>
          <el-button
            type="primary"
            :disabled="leftMoney < 3"
            @click="handlePurchase()"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <div class="title">
      {{ title.length > 7 ? title.substring(0, 7) + "..." : title }}
      <el-icon
        v-if="isCollected"
        :size="20"
        class="rate-theme-item-option"
        @click="handleUnCollect()"
        color="#409eff"
      >
        <StarFilled />
      </el-icon>
      <el-icon
        v-if="!isCollected"
        :size="20"
        class="rate-theme-item-option"
        @click="handleCollect()"
        :color="collectedColor"
      >
        <Star />
      </el-icon>
    </div>

    <div class="content">
      <div class="content-word" v-if="!isHovering">
        问卷状态：{{ state_list[state] }}
      </div>
      <div class="content-word" v-if="!isHovering">
        参加人数：{{ used_time }}人
      </div>
      <div class="content-word" v-if="!isHovering">
        问卷类型：{{ type_list[type] }}
      </div>
      <div v-if="isHovering">
        <button class="content-button" @click="handleWatch()">浏览</button>
        <button class="content-button" @click="handleWriteQ()">填写</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElDialog, ElForm, ElFormItem, ElButton, ElIcon } from "element-plus";
import { collectQ, purchaseQ, uncollectQ } from "../../api/questionnaire/plaza";
import { getUserId, getUserMoney, setUserMoney } from "../../http/cookies";
import 'element-plus/dist/index.css'
import * as Icons from '@element-plus/icons-vue';
export default {
  name: "SurveyBlock",
  components: {
    ElDialog,
    ElForm, 
    ElFormItem, 
    ElButton, 
    ElIcon,
    ...Icons,
  },
  props: {
    id: Number,
    title: String,
    state: Number,
    used_time: Number,
    type: Number,
    coin_reward: Number,
    coin_need: Number,
    iscollected: Boolean,
    purchased: Array,
    marginWidth: Object,
  },
  data() {
    return {
      collectedColor: "#c6d1de",
      purchaseVisiable: false,
      isHovering: false,
      state_list: ["已发布", "已停止", "未知"],
      type_list: ["普通", "投票", "考试", "报名"],
    };
  },
  computed: {
    isCollected() {
      return this.iscollected;
    },
    leftMoney() {
      return getUserMoney();
    },
    blockWidth() {
      return this.marginWidth["width"];
    },
    blockStyle() {
      const data = {};
      data["marginLeft"] = `${this.blockWidth}` + "px";
      data["marginRight"] = `${this.blockWidth}` + "px";
      return data;
    },
  },
  methods: {
    handleCollect() {
      const data = {};
      data["qn_id"] = this.id;
      data["user_name"] = getUserId();
      collectQ(data)
        .then((res) => {
          console.log(res.data.status_code);
          this.collectedColor = "#409eff";
          this.$emit("update-iscollected", true, this.id);
          console.log(this.id);
          ElMessage.success("收藏成功");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleUnCollect() {
      const data = {};
      data["qn_id"] = this.id;
      data["user_name"] = getUserId();
      uncollectQ(data)
        .then((res) => {
          console.log(res.data.status_code);
          this.collectedColor = "#c6d1de";
          this.$emit("update-iscollected", false, this.id);
          console.log(this.id);
          ElMessage.success("取消收藏成功");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    prePurchase() {
      for (let i = 0; i < this.purchased.length; ++i) {
        if (this.purchased[i].id == this.id) {
          //去预览fuckman
          this.$router.push({ path: "/analyse", query: { qnid: this.id } });
          return;
        }
      }
      this.purchaseVisiable = true;
    },
    handleCancel() {
      this.purchaseVisiable = false;
    },
    handlePurchase() {
      const data = {};
      data["qn_id"] = this.id;
      data["user_name"] = getUserId();
      purchaseQ(data)
        .then((res) => {
          ElMessage.success("购买成功!");
          let money = getUserMoney();
          setUserMoney(money - 3);
          let newItems = this.purchased;
          newItems.push({ id: this.id });
          this.$emit("update-items", newItems);
          // this.$route.push({path: '/plaza', query: {}});
          console.log(res.data.status_code);
        })
        .catch((err) => {
          console.log(err);
        });

      this.purchaseVisiable = false;
    },
    handleWatch() {
      this.$router.push({
        path: "/answer",
        query: { q_id: this.id, reward: true, abandon: true },
      });
    },
    handleWriteQ() {
      if (this.state != 1) {
        ElMessage.info("问卷停止，无法填写！");
        return;
      }
      this.$router.push({
        path: "/answer",
        query: { q_id: this.id, reward: true },
      });
    },
  },
  mounted() {
    console.log(this.marginWidth);
    console.log(this.marginWidth["width"]);
    // this.blockWidth = this.marginWidth['width'];
    // console.log(this.blockWidth);
    // this.blockStyle.marginLeft = `${this.blockWidth}` + 'px';
    // this.blockStyle.marginRight = `${this.blockWidth}` + 'px';
    // console.log(this.blockStyle.marginLeft);
    // console.log(this.blockStyle.marginRight);
  },
};
</script>

<style scoped>
.wrapper {
  width: 250px;
  height: 150px;
  background-color: white;
  border-radius: 10px;
  margin-bottom: 15px;
  float: left;
}
.wrapper:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}
.title {
  font-size: 25px;
  padding-top: 10px;
  padding-bottom: 10px;
}
.content {
  width: 200px;
  height: 100px;
  padding-left: 25px;
}
.content-word {
  font-size: 18px;
  color: grey;
}
.content-button {
  width: 80px;
  height: 60px;
  font-size: 23px;
  color: white;
  margin-left: 10px;
  margin-right: 10px;
  background-color: #3d99fb;
  padding: 0;
  border: 0;
  border-radius: 10px;
  cursor: pointer;
}
.content-button:hover {
  background-color: #0078f8;
}
</style>
