<template>
    <div style="width:100%; max-height: 100%; overflow:hidden;">
    <el-dialog v-model="dialogFormVisible1" title="修改用户名" width="500px">
      <el-form :model="form">
        <el-form-item label="新用户名" :label-width="formLabelWidth">
          <el-input v-model="form.newname" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="Cancel" class="button">取消</el-button>
          <el-button type="primary" @click="confirmChange" class="button">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <el-dialog
      v-model="dialogFormVisible2"
      title="修改邮箱"
      width="500px"
    >
      <el-form :model="form">
        <el-form-item label="新邮箱" :label-width="formLabelWidth">
          <el-input v-model="form.newemail" autocomplete="off" style="margin-bottom: 10px;"/>
        </el-form-item>
        <el-form-item label="验证码" :label-width="formLabelWidth">
          <el-input v-model="form.verification_code" autocomplete="off" />
        </el-form-item>
        <button
          type="button"
          v-if="isSended"
          class="verification-code"
          @click="getVerificationCode"
        >
          获取验证码
        </button>
        <button v-else disabled="true" class="verification-code">
          {{ clock.time_code }}s后重新发送
        </button>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="Cancel2" class="button">取消</el-button>
          <el-button type="primary" @click="confirmChange2" class="button">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <div class="box">
      <el-menu
        :default-active="activeIndex2"
        class="el-menu-demo"
        mode="horizontal"
        background-color="rgb(59, 72, 89)"
        text-color="#fff"
        active-text-color="#ffd04b"
        @select="handleSelect"
      >
        <el-menu-item index="0" style="width: 340px">
          <img
            style="
              width: 50px;
              height: 40px;
              margin-left: 50px;
              margin-right: 5px;
            "
            :src="`${imgUrl}/assets/flashq.svg`"
            alt="Element logo"
          />
          <span
            style="
              font-weight: 550;
              padding-right: 20px;
              font-size: 20px;
              margin-right: 230px;
            "
            >闪电问卷</span
          >
        </el-menu-item>
        <el-sub-menu index="1" style="width: 120px; margin-left: calc(100% - 700px)">
          <template #title>客服帮助</template>
          <el-menu-item index="1-1">王飞阳 : wfy1712619114(微信)</el-menu-item>
          <el-menu-item index="1-2"
            >罗智阳 : L2004yangyang2004(微信)</el-menu-item
          >
          <el-menu-item index="1-3">刘润林 : yhj090227(微信)</el-menu-item>
          <el-menu-item index="1-4">宋学斌 : s15972503232(微信)</el-menu-item>
          <el-menu-item index="1-5">余绍函 : im_2ppai(微信)</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="2">
          <img
            style="
              width: 28px;
              height: 28px;
              padding-right: 20px;
              padding-left: 20px;
            "
            :src="`${imgUrl}/assets/home.svg`"
            @click="go_back"
          />
        </el-menu-item>
        <!-- <el-menu-item index="3">
          <img
            style="
              width: 28px;
              height: 28px;
              padding-right: 20px;
              padding-left: 20px;
            "
            src="../assets/square.svg"
            @click="go_to_square"
          />
        </el-menu-item>
        <el-menu-item index="4">
          <img
            style="
              width: 28px;
              height: 28px;
              padding-right: 20px;
              padding-left: 20px;
            "
            src="../assets/help.svg"
            @click="go_to_help"
          />
        </el-menu-item>
        <el-menu-item index="5">
          <img
            style="
              width: 28px;
              height: 28px;
              padding-right: 20px;
              padding-left: 20px;
            "
            src="../assets/message.svg"
          />
        </el-menu-item> -->
        <el-sub-menu index="6">
          <template #title>
            <el-avatar
              :size="40"
              :src="imageUrl"
              class="avatar-border2"
              v-loading="loading"
          /></template>
          <el-menu-item index="2-1">
            <img
              :src="`${imgUrl}/assets/flashq.svg`"
              alt=""
              class="icon_flash"
            />
            <span> 闪电币: {{ user_money }}</span>
          </el-menu-item>
          <el-menu-item index="2-2" @click="logout">退出</el-menu-item>
        </el-sub-menu>
      </el-menu>
      <el-row class="tac" style="height: 100vh; overflow-y: auto">
        <el-col :span="12">
          <el-menu
            active-text-color="#ffd04b"
            background-color="rgb(59, 72, 89)"
            class="el-menu-vertical-demo"
            default-active="2"
            text-color="#fff"
            @open="handleOpen"
            @close="handleClose"
          >
            <h2
              style="
                text-align: center;
                margin-top: 10px;
                margin-bottom: 7px;
                color: #fff;
              "
            >
              User Center
            </h2>
            <!-- <el-sub-menu index="1">
              <template #title>
                <el-icon><IconMenu /></el-icon>
                <span>功能区</span>
              </template>
              <el-menu-item index="1-1" @click="make_questionnaire"
                >问卷制作</el-menu-item
              >
              <el-menu-item index="1-2" @click="do_questionnaire"
                >问卷填写</el-menu-item
              >
              <el-menu-item index="1-3" @click="data_statistics"
                >数据统计</el-menu-item
              >
              <el-menu-item index="1-4" @click="data_analysis"
                >数据分析</el-menu-item
              >
            </el-sub-menu> -->
            <el-sub-menu index="2">
              <template #title>
                <el-icon><User /></el-icon>
                <span>我的</span>
              </template>
              <el-menu-item index="2-1" @click="make_questionnaire"
                >我的发布</el-menu-item
              >
              <el-menu-item index="2-2" @click="go_to_buy"
                >我的购买</el-menu-item
              >
              <el-menu-item index="2-3" @click="go_to_collection"
                >我的收藏</el-menu-item
              >
              <el-menu-item index="2-4" @click="go_to_history"
                >填写记录</el-menu-item
              >
            </el-sub-menu>
            <el-menu-item index="3" @click="go_to_help">
              <el-icon><Document /></el-icon>
              <span>说明文档</span>
            </el-menu-item>
            <el-sub-menu index="4">
              <template #title>
                <el-icon><Setting /></el-icon>
                <span>设置</span>
              </template>
              <el-menu-item index="4-1" @click="dialogFormVisible1 = true"
                >修改用户名</el-menu-item
              >
              <el-menu-item index="4-2" @click="dialogFormVisible2 = true"
                >修改邮箱</el-menu-item
              >
              <el-menu-item index="4-3" @click="go_to_pwchange"
                >修改密码</el-menu-item
              >
              <el-menu-item index="4-4" @click="logout">注销账号</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="5" disabled>
              <!-- <el-icon><More /></el-icon> -->
              <span>To Be Continue...</span>
            </el-menu-item>
          </el-menu>
        </el-col>
      </el-row>
      <div class="content">
        <div class="user-wrapper">
          <div class="demo-type">
            <div>
              <el-upload
                v-loading="loading"
                class="avatar-uploader"
                action="https://www.imgurl.org/api/v2/upload"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <el-avatar
                  v-if="imageUrl"
                  :src="imageUrl"
                  :size="125"
                  class="avatar-border"
                />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </div>
          </div>
          <div class="user-form">
            <div class="form-item">
              <span>用户名</span>
              <button
                class="user-info"
                @mouseover="handleFocus1"
                v-if="isNotFocus1"
              >{{ user_name }}</button>
              <button
                class="user-info"
                v-if="!isNotFocus1"
                @mouseleave="handleBlur1"
                plain
                @click="dialogFormVisible1 = true"
              >
                修改用户名
              </button>
            </div>
            <div class="email form-item">
              <span>邮箱</span>
              <button
                class="user-info"
                @mouseover="handleFocus2"
                v-if="isNotFocus2"
              >
                {{ user_email }}
              </button>
              <button
                class="user-info"
                v-if="!isNotFocus2"
                @mouseleave="handleBlur2"
                plain
                @click="dialogFormVisible2 = true"
              >
                修改用户邮箱
              </button>
            </div>
            <div class="logout form-item">
              <span>退出</span>
              <button class="logout-btn" @click="logout">登出</button>
            </div>
          </div>
          <div class="divider">
            <span class="line"></span>
            <span class="divider-text">常用功能区</span>
            <span class="line"></span>
          </div>
          <div class="other-user-wrapper">
            <div class="choose_list1">
              <div
                v-for="choose in choose_list1"
                :key="choose.id"
                :style="{ '--x': choose.id % 1, '--y': (choose.id / 1) | 0 }"
                class="choose"
              >
                <div style="position: absolute; width: 100px; height: 100%">
                  <span
                    style="
                      position: absolute;
                      top: 10%;
                      left: 20%;
                      font-size: 20px;
                      font-weight: 600;
                    "
                    >{{ choose.text }}</span
                  >
                  <span
                    style="
                      position: absolute;
                      top: 45%;
                      left: 20%;
                      font-size: 16px;
                    "
                    >{{ choose.discribe }}</span
                  >
                </div>
                <div
                  style="
                    position: absolute;
                    height: 60px;
                    top: 20px;
                    width: 1px;
                    left: 132px;
                    background: rgb(158, 166, 172);
                  "
                ></div>
                <img
                  :src="choose.img_src"
                  style="
                    width: 48px;
                    height: 58px;
                    position: absolute;
                    top: 22px;
                    left: 150px;
                  "
                />
                <img
                  :src="`${imgUrl}/assets/next.svg`"
                  style="
                    width: 70px;
                    height: 80px;
                    position: absolute;
                    top: 10px;
                    left: 140px;
                    cursor: pointer;
                  "
                  @click="handle1(choose)"
                  class="create"
                />
              </div>
            </div>
            <div class="choose_list2">
              <div
                v-for="choose in choose_list2"
                :key="choose.id"
                :style="{ '--x': choose.id % 1, '--y': (choose.id / 1) | 0 }"
                class="choose"
              >
                <div style="position: absolute; width: 100px; height: 100%">
                  <span
                    style="
                      position: absolute;
                      top: 10%;
                      left: 20%;
                      font-size: 20px;
                      font-weight: 600;
                    "
                    >{{ choose.text }}</span
                  >
                  <span
                    style="
                      position: absolute;
                      top: 45%;
                      left: 20%;
                      font-size: 16px;
                    "
                    >{{ choose.discribe }}</span
                  >
                </div>
                <div
                  style="
                    position: absolute;
                    height: 60px;
                    top: 20px;
                    width: 1px;
                    left: 132px;
                    background: rgb(158, 166, 172);
                  "
                ></div>
                <img
                  :src="choose.img_src"
                  style="
                    width: 48px;
                    height: 58px;
                    position: absolute;
                    top: 22px;
                    left: 150px;
                  "
                />
                <img
                  :src="`${imgUrl}/assets/next.svg`"
                  style="
                    width: 70px;
                    height: 80px;
                    position: absolute;
                    top: 10px;
                    left: 140px;
                    cursor: pointer;
                  "
                  @click="handle2(choose)"
                  class="create"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessageBox } from "element-plus";
import { ElMessage } from "element-plus";
import {
  logoutapi,
  getVerificationCodeapi,
  changeUserNameAPI,
  changeUserEmailAPI,
  uploadAvatarAPI,
} from "../../api/account/usercenter";
import { imgUrl } from "../../http/cookies";
export default {
  name: "ConsoleItem",
  data() {
    return {
      imgUrl: imgUrl,
      choose_list1: [
        {
          id: 0,
          text: "我的购买",
          discribe: "查看购买的问卷",
          img_src: imgUrl + "/assets/buy.svg",
        },
        {
          id: 1,
          text: "填写记录",
          discribe: "查看自己填过的问卷",
          img_src: imgUrl + "/assets/history.svg",
        },
      ],
      choose_list2: [
        {
          id: 0,
          text: "我的收藏",
          discribe: "查看自己收藏的问卷",
          img_src: imgUrl + "/assets/mycollect.svg",
        },
        {
          id: 1,
          text: "修改密码",
          discribe: "修改账户的密码",
          img_src: imgUrl + "/assets/changepw.svg",
        },
      ],
      user_img:imgUrl+"/assets/search.png",
    };
  },
  methods: {
    logout() {
      ElMessageBox.confirm("确定退出登录吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          try {
            logoutapi().then((response) => {
              console.log("退出成功:", response.data);
              // 处理响应数据，例如保存token，跳转页面等
              const statusCode = response.data.status_code;
              switch (statusCode) {
                case 200:
                  removeUserId();
                  removeUserEmail();
                  removeUserAvatarURL();
                  removeUserMoney();
                  console.log(getUserId);
                  console.log(getUserEmail);
                  console.log(getUserAvatarURL);
                  ElMessage.success({
                    message: "退出成功!",
                  });
                  this.$router.push("/home");
                  break;

                case 401:
                  alert("未登录");
                  break;

                default:
                  alert("未知错误，请稍后重试");
                  break;
              }
            });
          } catch (error) {
            console.error("退出失败:", error);
            // 处理错误，显示错误信息等
          }
        })
        .catch(() => {
          ElMessage.info({
            message: "已取消",
          });
        });
    },
    handle1(item) {
      if (item.id == 0) window.open("/buy", "_blank");
      else window.open("/history", "_blank");
    },

    handle2(item) {
      if (item.id == 0) window.open("/collection", "_blank");
      else this.$router.push("/changePw");
    },

    go_back() {
      this.$router.push("/home");
    },
    go_to_square() {
      window.open("/plaza", "_blank");
    },
    go_to_help() {
      window.open("https://flash-questionnaire.github.io/", "_blank");
    },
    make_questionnaire() {
      this.$router.push("/console");
    },
    do_questionnaire() {
      window.open("/plaza", "_blank");
    },
    data_statistics() {
      this.$router.push("/console");
    },
    data_analysis() {
      this.$router.push("/console");
    },
    go_to_collection() {
      window.open("/collection", "_blank");
    },
    go_to_buy() {
      window.open("/buy", "_blank");
    },
    go_to_history() {
      window.open("/history", "_blank");
    },
    go_to_pwchange() {
      this.$router.push("/changePw");
    },
  },
};
</script>

<script setup>
import { reactive, ref } from "vue";
// import { useRoute } from "vue-router";
import {
  getUserEmail,
  setUserEmail,
  getUserAvatarURL,
  setUserAvatarURL,
  getUserId,
  setUserId,
  removeUserId,
  removeUserEmail,
  removeUserAvatarURL,
  removeUserMoney,
  getUserMoney,
} from "../../http/cookies";
import {
  Document,
  // Menu as IconMenu,
  Setting,
  User,
} from "@element-plus/icons-vue";
import { Plus } from "@element-plus/icons-vue";
import axios from "axios";
import { ElForm, ElFormItem, ElButton, ElInput, ElUpload, 
  ElDialog, ElMenu, ElMenuItem, ElSubMenu, ElAvatar, ElRow, ElCol, ElIcon } from "element-plus"
// const route = useRoute();
let user_name = getUserId();
let user_email = getUserEmail();
let user_money = getUserMoney();
console.log(user_money);
// console.log(getUserId());
// console.log(getUserEmail());
// let user_avatarURL = getUserAvatarURL();
console.log(user_email);
const loading = ref(false);
const isNotFocus1 = ref(true);
const isNotFocus2 = ref(true);
const handleFocus1 = (isNotFocus) => {
  isNotFocus1.value = !isNotFocus1.value;
};
const handleBlur1 = (isNotFocus) => {
  isNotFocus1.value = !isNotFocus1.value;
};
const handleFocus2 = (isNotFocus) => {
  isNotFocus2.value = !isNotFocus2.value;
};
const handleBlur2 = (isNotFocus) => {
  isNotFocus2.value = !isNotFocus2.value;
};

const dialogFormVisible1 = ref(false);
const dialogFormVisible2 = ref(false);
const formLabelWidth = "140px";

const form = reactive({
  name: "",
  newname: "",
  newemail: "",
  region: "",
  date1: "",
  date2: "",
  delivery: false,
  type: [],
  resource: "",
  desc: "",
  verification_code: "",
});

const confirmChange = () => {
  // 在这里执行更新用户名的操作，例如向后端发送请求
  // 更新成功后关闭对话框
  // 示例：假设这里是一个更新用户名的异步操作
  updateUsername(form)
    .then(() => {
      // 更新成功
      // console.log(form.name);
    })
    .catch(() => {
      // 更新失败
    });
};

const updateUsername = (form) => {
  console.log("尝试更改用户名");
  console.log("旧用户名:", user_name);
  console.log("新用户名:", form.newname);
  if (form.newname == "") {
    alert("请输入新用户名");
  } else {
    const formData = new FormData();
    formData.append("old_username", user_name);
    formData.append("new_username", form.newname);
    changeUserNameAPI(formData).then((response) => {
      console.log("修改名字成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          alert("用户名修改成功！");
          setUserId(form.newname);
          user_name = form.newname;
          form.newname = "";
          ElMessage.success("用户名已更新");
          dialogFormVisible1.value = false;
          break;

        case -1:
          alert("传输数据格式错误！");
          ElMessage.error("更新失败，请重试");
          break;

        case 2:
          alert("用户不存在或用户未登录！");
          ElMessage.error("更新失败，请重试");
          break;

        case 4:
          alert("请求类型错误！");
          ElMessage.error("更新失败，请重试");
          break;

        default:
          alert("用户名重复");
          ElMessage.error("更新失败，请重试");
          break;
      }
    });
  }

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // user_name = form.newname;
      // form.newname = "";
      resolve();
    }, 100);
  });
};
const Cancel = () => {
  dialogFormVisible1.value = false;
  form.newname = "";
  ElMessage.info({
    message: "已取消",
  });
};

const confirmChange2 = () => {
  // 在这里执行更新用户名的操作，例如向后端发送请求
  // 更新成功后关闭对话框
  // 示例：假设这里是一个更新用户名的异步操作
  updateUseremail(form)
    .then(() => {
      // 更新成功
      // console.log(form.name);
    })
    .catch(() => {
      // 更新失败
    });
};

const updateUseremail = (form) => {
  console.log("尝试更改邮箱");
  console.log("旧邮箱:", user_email);
  console.log("新邮箱:", form.newemail);
  console.log("验证码:", form.verification_code);
  if (form.newemail == "") {
    alert("请输入新邮箱");
  } else if (form.verification_code == "") {
    alert("请输入验证码");
  } else {
    const formData = new FormData();
    formData.append("old_email", user_email);
    formData.append("new_email", form.newemail);
    formData.append("code", form.verification_code);
    changeUserEmailAPI(formData).then((response) => {
      console.log("修改邮箱成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          alert("邮箱重设成功！");
          setUserEmail(form.newemail);
          user_email = form.newemail;
          form.newemail = "";
          form.verification_code = "";
          ElMessage.success("邮箱已更新");
          dialogFormVisible2.value = false;
          break;

        case -1:
          alert("输入数据格式错误！");
          ElMessage.error("更新失败，请重试");
          break;

        case 2:
          alert("验证码错误！");
          ElMessage.error("更新失败，请重试");
          break;

        case 3:
          alert("验证码过期！");
          ElMessage.error("更新失败，请重试");
          break;

        case -2:
          alert("请求类型错误！");
          ElMessage.error("更新失败，请重试");
          break;

        default:
          alert("未知错误，请稍后重试");
          ElMessage.error("更新失败，请重试");
          break;
      }
    });
  }
  // 模拟异步更新用户名的操作
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, 100);
  });
};
const Cancel2 = () => {
  dialogFormVisible2.value = false;
  form.newemail = "";
  form.verification_code = "";
  ElMessage.info({
    message: "已取消",
  });
};

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};
const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};
// const activeIndex = ref("1");
const activeIndex2 = ref("1");
const handleSelect = (key, keyPath) => {
  console.log(key, keyPath);
};

let imageUrl = getUserAvatarURL();

const handleAvatarSuccess = (response, uploadFile) => {
  // 利用 URL.createObjectURL 将上传的文件转换为可预览的 URL，并赋值给 imageUrl
  // imageUrl.value = URL.createObjectURL(uploadFile.raw);
  // console.log(uploadFile.raw);
  // loading.value = !loading.value;
  handleAvatarSuccess2(uploadFile);
  imageUrl = getUserAvatarURL();
  console.log(imageUrl);

  setTimeout(() => {
    window.location.reload();
  }, 4000); // 延迟4秒钟刷新页面
};
const handleAvatarSuccess2 = async (uploadFile) => {
  console.log("尝试上传");
  console.log("UID:", "e12bbad9b00fcfb0740e649dec08703c");
  console.log("Token:", "3443769392752693a92f5adb06154bf8");
  console.log("file:", uploadFile.raw);
  const formData = new FormData();
  formData.append("file", uploadFile.raw);
  formData.append("uid", "5ff0a910840532b525e5e2f12ab011dc");
  formData.append("token", "95eab0a52f075660081a9503ea9d1245");
  try {
    const response = await axios.post(
      "https://www.imgurl.org/api/v2/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    console.log("上传成功", response.data);
    console.log(response.data.data.url);
    uploadAvatar(response.data.data.url);
  } catch (error) {
    console.error("上传失败", error);
  }
};

const beforeAvatarUpload = (rawFile) => {
  loading.value = !loading.value;
  if (rawFile.type !== "image/jpeg" && rawFile.type !== "image/png") {
    ElMessage.error("Avatar picture must be JPG/PNG format!");
    loading.value = !loading.value;
    return false;
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error("Avatar picture size cannot exceed 2MB!");
    loading.value = !loading.value;
    return false;
  }

  return true;
};

//获取验证码
const isSended = ref(true);
const clock = reactive({
  time_code: 0,
});

const timer = reactive({
  timer_code: null,
});

const startCountDown = () => {
  if (timer.timer_code) clearInterval(timer.timer_code);
  timer.timer_code = setInterval(() => {
    clock.time_code--;
    if (clock.time_code === 0) {
      clearInterval(timer.timer_code);
      isSended.value = !isSended.value;
    }
  }, 1000);
};

const isRequired = ref(true);
const getVerificationCode = async () => {
  isRequired.value = false;
  console.log("尝试获取验证码");
  console.log("旧邮箱:", user_email);
  console.log("新邮箱:", form.newemail);
  if (form.newemail == "") {
    alert("请输入新邮箱");
    return;
  }
  const formData = new FormData();
  formData.append("old_email", user_email);
  formData.append("new_email", form.newemail);
  try {
    getVerificationCodeapi(formData).then((response) => {
      console.log("获取邮箱验证码成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          alert("获取成功！");
          isSended.value = !isSended.value;
          clock.time_code = 60;
          startCountDown();
          break;

        case -1:
          alert("输入数据格式错误！");
          break;

        case -2:
          alert("请求类型错误！");
          break;

        case 2:
          alert("用户不存在！");
          break;

        case 3:
          alert("验证码发送失败！");
          break;

        case 4:
          alert("用户未进行邮箱绑定！");
          break;

        case 7:
          alert("验证码已发送");
          break;

        default:
          alert("未知错误，请稍后重试");
          break;
      }
    });
  } catch (error) {
    console.error("获取邮箱验证码失败:", error);
    // 处理错误，显示错误信息等
  }
  isRequired.value = true;
};

const uploadAvatar = async (url) => {
  console.log("尝试上传头像");
  console.log("头像url:", url);
  console.log("用户名:", user_name);
  const formData = new FormData();

  formData.append("url", url);
  formData.append("username", user_name);

  console.log("formData", formData);

  try {
    uploadAvatarAPI(formData).then((response) => {
      console.log("上传成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          alert("头像上传成功！");
          setUserAvatarURL(url);
          break;

        case -1:
          alert("传输数据格式错误！");
          break;

        case 2:
          alert("用户不存在或用户未登录！");
          break;

        case 4:
          alert("请求类型错误！");
          break;

        default:
          alert("未知错误，请稍后重试");
          break;
      }
    });
  } catch (error) {
    console.error("登录失败:", error);
    // 处理错误，显示错误信息等
  }
};
</script>

<style scoped>
@charset "UTF-8";
* {
  margin: 0;
  padding: 0;
}

/* .flex-grow {
  width: 69vw;
} */

.icon_flash {
  width: 25px;
  height: 25px;
  margin-right: 5px;
}

.verification-code {
  display: inline-block;
  width: 100px;
  height: 43px;
  margin-top: 5px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 0.8rem;
  font-size: 0.8rem;
  transition: 0.3s;
}

.verification-code:hover {
  background-color: #0056b3;
}

.el-menu-demo {
  /* position: absolute; */
  z-index: 2;
}

.avatar-border {
  border: 3px solid rgb(59, 72, 89); /* 设置蓝色边框 */
  border-radius: 50%; /* 使边框为圆形 */
  margin-top: 10px;
}

.avatar-border2 {
  border: 3px solid rgb(59, 72, 89); /* 设置蓝色边框 */
  border-radius: 50%; /* 使边框为圆形 */
  margin-top: 3px;
}
.avatar-camera {
  border: 2px solid rgb(59, 72, 89);
  border-radius: 50%; /* 使边框为圆形 */
  padding: 2px;
  margin-left: 0;
  width: 17px;
  height: 17px;
  cursor: pointer;
}

.demo-type {
  display: flex;
}
.demo-type > div {
  flex: 1;
  text-align: center;
}

.demo-type > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
.icon {
  height: 20px;
  margin-right: 0.3rem;
  width: 20px;
}
.el-menu-vertical-demo {
  height: 100vh;
  width: 20vw;
  position: absolute;
  z-index: 2;
}

.button {
  width: 20%;
}

.choose_list1 {
  position: absolute;
  width: 280px;
  height: 200px;
  left: 18%;
  top: 5%;
  transform: translate(-50%, 0%);
}

.choose_list2 {
  position: absolute;
  width: 280px;
  height: 200px;
  left: 82%;
  top: 5%;
  transform: translate(-50%, 0%);
}

.choose {
  position: absolute;
  top: calc(var(--y) * 110px);
  left: 30px;
  background-color: white;
  border-radius: 3px;
  width: 220px;
  height: 100px;
  box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

.box {
  width: 100vw;
  height: 100vh;
  background-color: rgb(29, 67, 89);
}

.box .content .user-wrapper .user-form .user-info {
  width: 100%;
  border-radius: 40px;
  color: #fff;
  border: 0;
  font-weight: 400;
  margin-top: 10px;
  height: 50px;
  background-color: rgb(59, 72, 89);
  font-size: 20px;
  cursor: pointer;
}
.box .content .user-wrapper .user-form .user-info:hover {
  background-color: #8371fd;
}
.user-wrapper {
  height: 90vh;
  margin-top: 2rem;
}
.box .content .user-wrapper h1 {
  text-align: center;
}
.box .content .user-wrapper .user-form .form-item {
  margin: 20px 0;
}
.box .content .user-wrapper .user-form .form-item span {
  display: block;
  margin: 5px 20px;
  font-weight: 800;
  font-size: 20px;
}
.box .content .user-wrapper .user-form .form-item .input-item {
  width: 100%;
  border-radius: 40px;
  padding: 20px;
  box-sizing: border-box;
  font-size: 20px;
  font-weight: 200;
}
.box .content .user-wrapper .user-form .form-item .input-item:focus {
  outline: none;
}
.box .content .user-wrapper .user-form .logout-btn {
  width: 100%;
  border-radius: 40px;
  color: #fff;
  border: 0;
  margin-top: 10px;
  cursor: pointer;
}

.box .content .user-wrapper .user-form .logout-btn:hover {
  background-color: red;
}
.box .content .user-wrapper .divider {
  width: 100%;
  margin: 20px 0;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.box .content .user-wrapper .divider span:nth-child(1) {
  flex: 1;
}
.box .content .user-wrapper .divider span:nth-child(3) {
  flex: 1;
}
.box .content .user-wrapper .divider .line {
  display: inline-block;
  max-width: 30%;
  width: 30%;
}
.box .content .user-wrapper .divider .divider-text {
  vertical-align: middle;
  margin: 0px 20px;
  line-height: 0px;
  display: inline-block;
  width: 100px;
}
.box .content .user-wrapper .other-user-wrapper {
  position: absolute;
  width: 100%;
  height: 20%;
}

.box .content .user-wrapper .other-function-item {
  display: block;
  width: 50%;
  border-radius: 40px;
  color: #fff;
  border: 0;
  font-weight: 400;
  margin-top: 10px;
  height: 50px;
  background-color: rgb(59, 72, 89);
  font-size: 20px;
  margin-top: 30px;
}

/*一般大于手机的尺寸CSS*/
@media (min-width: 767px) {
  .box {
    background-color: rgb(29, 67, 89);
  }
  .box .content {
    width: 80vw;
    height: 100vh;
    background: url("https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com/assets/login_two.jpg") no-repeat;
    background-size: 90% 100%;
    position: absolute;
    right: 0%;
    top: 50%;
    left: 50%;
    transform: translate(-37.5%, -50%);
    background-color: #fff;
    z-index: 1;
  }
  .box .content .user-wrapper {
    height: 90vh;
    width: 25vw;
    position: absolute;
    right: 15%;
    top: 50%;
    transform: translate(20%, -50%);
  }
  .box .content .user-wrapper h1 {
    text-align: center;
    font-size: 45px;
    color: rgb(81, 100, 115);
    margin-bottom: 40px;
  }
  .box .content .user-wrapper .user-form {
    margin: 10px 0;
  }
  .box .content .user-wrapper .user-form .form-item span {
    color: rgb(81, 100, 115);
  }
  .box .content .user-wrapper .user-form .form-item .input-item {
    height: 60px;
    border: 1px solid rgb(214, 222, 228);
  }
  .box .content .user-wrapper .user-form .logout-btn {
    height: 50px;
    background-color: rgb(59, 72, 89);
    font-size: 20px;
  }

  .box .content .user-wrapper .divider .line {
    border-bottom: 1px solid rgb(214, 222, 228);
  }
  .box .content .user-wrapper .other-function-item {
    border-radius: 20px;
  }
  .box .content .user-wrapper .other-function-item img {
    width: 40px;
    height: 40px;
  }
}
/*手机端CSS*/
@media (max-width: 768px) {
  .box .el-menu-demo {
    display: none;
  }
  .box .tac {
    display: none;
  }
  .box .content .user-wrapper .other-user-wrapper {
    display: none;
  }
  .box .content .user-wrapper .divider {
    display: none;
  }
  .box .content {
    width: 100vw;
    height: 100vh;
    background: url("https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com/assets/login_bg_phone.png") no-repeat;
    background-size: 100% 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
  }
  .box .content .user-wrapper {
    width: 70%;
    height: 60%;
    padding-top: 15%;
  }
  .box .content .user-wrapper h1 {
    font-size: 30px;
    color: #fff;
  }
  .box .content .user-wrapper .user-form .form-item {
    margin: 10px 0;
  }
  .box .content .user-wrapper .user-form .form-item span {
    color: rgb(113, 129, 141);
  }
  .box .content .user-wrapper .user-form .form-item .input-item {
    height: 30px;
    border: 1px solid rgb(113, 129, 141);
    background-color: transparent;
    color: #fff;
  }
  .box .content .user-wrapper .user-form .logout-btn {
    height: 40px;
    background-color: rgb(235, 95, 93);
    font-size: 16px;
  }
  .box .content .user-wrapper .divider .line {
    border-bottom: 1px solid #fff;
  }
  .box .content .user-wrapper .divider .divider-text {
    color: #fff;
  }
  .box .content .user-wrapper .other-function-item {
    border-radius: 15px;
  }
  .box .content .user-wrapper .other-function-item img {
    width: 35px;
    height: 35px;
  }
}

.create {
  opacity: 0;
}

.choose:hover .create {
  opacity: 1;
}
</style>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px solid rgb(254, 254, 255);
  /* border-radius: 6px; */
  width: 140px;
  height: 140px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  border-radius: 50%;
  margin-top: 10px;
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
