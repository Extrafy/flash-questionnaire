<template>
  <div class="window">
    <div class="title">
      <img :src="`${imgUrl}/assets/flashq.svg`" style="margin-top: 10px" />
      <div class="title-word">填写记录</div>
    </div>
    <div class="search">
      <!-- <el-input v-model="searchedValue" style="width: 240px;height: 100px;" placeholder="Please input" /> -->
      <input
        class="search-input"
        placeholder="请在此输入您想找的问卷"
        ref="inputRef"
        v-model="searchedValue"
      />
      <!-- <button class="search-button" @click="submitSearch">
        <img src="../../public/search.svg">
      </button> -->
    </div>
    <div class="blocks">
      <el-scrollbar max-height="800px">
        <div
          class="survey-blocks-container"
          style="display: flex; flex-wrap: wrap"
        >
          <SurveyBlock
            v-for="(b, index) in calBlocks"
            :key="index"
            :title="b.title"
            :state="b.state"
            :used_time="b.used_time"
            :iscollected="b.iscollected"
            :type="b.type"
            :id="b.id"
            :marginWidth="marginWidth"
            :purchased="purchased"
            :ownedList="ownedList"
            @update-iscollected="updateIscollected"
          ></SurveyBlock>
        </div>
      </el-scrollbar>
    </div>
  </div>
</template>

<script>
import SurveyBlock from "../components/historySurvey.vue";
import { getHistoryQ } from "../../api/questionnaire/plaza";
import { getUserId ,imgUrl} from "../../http/cookies";
import { ElScrollbar } from "element-plus"

export default {
  name: "PlazaItem",
  components: { SurveyBlock, ElScrollbar },
  computed: {
    calBlocks() {
      let list = this.blocks;
      if (this.searchedValue != null && this.searchedValue != "") {
        list = list.filter((item) => {
          return item.title
            .toLowerCase()
            .includes(this.searchedValue.toLowerCase());
        });
      }
      return list;
    },
  },
  data() {
    return {
      imgUrl: imgUrl,
      searchedValue: "",
      purchased: [],
      collectedList: [],
      blocks: [],
      ownedList: [],
      blockWidth: 0,
      marginWidth: {width: 0,},
    };
  },
  methods: {
    submitSearch() {
      const inputContent = this.$refs.inputRef.value;
      this.$router.push("/search");
      this.$router.replace({
        path: "/plaza/search",
        query: { input: inputContent },
      });
    },
    handleGetQ() {
      const data = {};
      data["user_name"] = getUserId();
      getHistoryQ(data)
        .then((res) => {
          console.log(res.data.list1);
          console.log(res.data.list2);
          console.log(res.data.list3);
          this.blocks = res.data.list1;
          this.purchased = res.data.list2;
          this.collectedList = res.data.list3;
          for (let i = 0; i < this.collectedList.length; i++) {
            for (let j = 0; j < this.blocks.length; j++) {
              if (
                parseInt(this.blocks[j].id) ===
                parseInt(this.collectedList[i].id)
              ) {
                this.blocks[j].iscollected = true;
                break;
              }
            }
            console.log(res.data.status_code);
            console.log(this.blocks);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateIscollected(newIscollected, id) {
      console.log("fuckman");
      console.log(id);
      for (let i = 0; i < this.blocks.length; i++) {
        if (this.blocks[i].id === id) {
          this.blocks[i].iscollected = newIscollected;
        }
      }
      console.log(this.Blocks);
    },
    updateWidth() {
      this.$nextTick(() => {
        const blocks = document.getElementsByClassName('blocks');
        if (blocks.length > 0) {
          this.blockWidth = blocks[0].offsetWidth;
          console.log(this.blockWidth);
          this.notifyWidthChange(this.blockWidth);
        }
      });
    },
    notifyWidthChange(width) {
      // 执行你需要的计算并传递结果给其他组件
      // 例如，通过事件总线或 Vuex 进行传递
      let computedWidth = (width - Math.floor(width / 250) * 250)/2/Math.floor(width/250);
      this.marginWidth.width = computedWidth - 0.04;
      console.log(computedWidth);
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateWidth);
  },
  mounted() {
    this.handleGetQ();
    this.updateWidth();
    window.addEventListener('resize', this.updateWidth);
  },
};
</script>

<style scoped>
.window {
  background-color: rgb(238, 244, 251);
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0%;
  left: 0%;
  overflow-y: scroll;
}

.title {
  width: 100%;
  height: 100px;
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  position: absolute;
  top: 5%;
}

.title-word {
  line-height: 100px;
  font-size: 60px;
  display: inline-block;
  position: relative;
  top: -30px;
}

.search {
  width: 100%;
  height: 50px;
  position: absolute;
  top: 170px;
  text-align: center;
}

.search-input {
  max-width: 600px;
  width: 70%;
  height: 50px;
  top: 10px;
  font-size: 20px;
  padding: 0;
  border: 0;
  text-indent: 10px;
  position: relative;
  top: -6px;
  padding: 2px;
}

.search-button {
  width: 10%;
  min-width: 20px;
  height: 50px;
  font-size: 20px;
  padding: 0;
  border: 0;
  background-color: #007bff;
  position: relative;
  top: 0;
  cursor: pointer;
}

.search-button:active {
  background-color: #0056b3;
}

.blocks {
  width: 90%;
  height: 60%;
  text-align: center;
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  top: 270px;
  left: 5%;
}

.refresh {
  width: 100%;
  font-size: 20px;
  text-decoration: underline;
  cursor: pointer;
}
</style>
