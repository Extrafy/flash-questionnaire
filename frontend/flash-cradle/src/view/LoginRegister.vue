<template>
  <body>
    <main :class="{ 'sign-up-mode': isSignUpMode }">
      <div class="box">
        <div class="inner-box">
          <!-- 表单 -->
          <div class="forms-wrap">
            <!--sign-in-->
            <form action="index.html" autocomplete="off" class="sign-in-form">
              <div class="logo1">
                <img :src="`${imgUrl}/assets/flashq.svg`" alt="logo1" />
                <h2>闪电问卷</h2>
              </div>
              <div class="heading">
                <h2>欢迎回来</h2>
                <h6>Not registered yet?</h6>
                <a href="#" class="toggle" @click="toggleSignUpMode">
                  Sign up</a
                >
              </div>
              <!-- 表单 -->
              <div class="actual-form">
                <form @submit.prevent="handleLogin">
                  <div class="input-wrap1">
                    <input
                      type="text"
                      minlength="3"
                      autocomplete="off"
                      required
                      :key="inputFields[0].id"
                      class="input-field"
                      :class="{ active: inputFields[0].isActive }"
                      @focus="handleFocus(inputFields[0])"
                      @blur="handleBlur(inputFields[0])"
                      v-model="inputFields[0].value"
                    />
                    <label>Name</label>
                  </div>
                  <div class="input-wrap1">
                    <input
                      type="password"
                      autocomplete="off"
                      required
                      :key="inputFields[1].id"
                      class="input-field"
                      :class="{ active: inputFields[1].isActive }"
                      @focus="handleFocus(inputFields[1])"
                      @blur="handleBlur(inputFields[1])"
                      v-model="inputFields[1].value"
                    />
                    <label>Password</label>
                  </div>
                  <input
                    type="submit"
                    value="Sign In"
                    class="sign-btn"
                    @submit.prevent="handleLogin"
                  />
                  <input
                    type="submit"
                    value="Back to Home"
                    class="back-btn"
                    @click="go_back"
                  />
                </form>
                <p class="text">
                  忘记密码?
                  <a href="#" @click.prevent="find_lost_password">找回密码</a>
                </p>
              </div>
            </form>
            <!--sign-up-->
            <form action="index.html" autocomplete="off" class="sign-up-form">
              <div class="logo2">
                <img :src="`${imgUrl}/assets/flashq.svg`" alt="log2" />
                <h4>闪电问卷</h4>
              </div>
              <div class="heading">
                <h2>注册</h2>
                <h6>Already have an account?</h6>
                <a href="#" class="toggle" @click="toggleSignUpMode">
                  Sign in</a
                >
              </div>
              <!-- 表单 -->
              <div class="actual-form">
                <form @submit.prevent="signUp">
                  <div class="input-wrap2">
                    <input
                      type="text"
                      minlength="3"
                      autocomplete="off"
                      required
                      :key="inputFields[2].id"
                      class="input-field"
                      :class="{ active: inputFields[2].isActive }"
                      @focus="handleFocus(inputFields[2])"
                      @blur="handleBlur(inputFields[2])"
                      v-model="inputFields[2].value"
                    />
                    <label>Name</label>
                  </div>
                  <div class="input-wrap2">
                    <input
                      type="email"
                      autocomplete="off"
                      required
                      :key="inputFields[3].id"
                      class="input-field"
                      :class="{ active: inputFields[3].isActive }"
                      @focus="handleFocus(inputFields[3])"
                      @blur="handleBlur(inputFields[3])"
                      v-model="inputFields[3].value"
                    />
                    <label>Email</label>
                  </div>
                  <div class="input-wrap2" prop="newPassword">
                    <input
                      type="password"
                      autocomplete="off"
                      required
                      :key="inputFields[4].id"
                      class="input-field"
                      :class="{ active: inputFields[4].isActive }"
                      @focus="handleFocus(inputFields[4])"
                      @blur="handleBlur(inputFields[4])"
                      v-model="inputFields[4].value"
                    />
                    <label>Password</label>
                  </div>
                  <div class="input-wrap2" prop="confirmPassword">
                    <input
                      type="password"
                      autocomplete="off"
                      required
                      :key="inputFields[5].id"
                      class="input-field"
                      :class="{ active: inputFields[5].isActive }"
                      @focus="handleFocus(inputFields[5])"
                      @blur="handleBlur(inputFields[5])"
                      v-model="inputFields[5].value"
                    />
                    <label>Confirm Password</label>
                  </div>
                  <p v-if="passwordsMatch === false" class="error-message">
                    Passwords do not match!
                  </p>
                  <div class="input-wrap2" prop="">
                    <input
                      type="test"
                      autocomplete="off"
                      :required="isRequired"
                      :key="inputFields[6].id"
                      class="input-field"
                      :class="{ active: inputFields[6].isActive }"
                      @focus="handleFocus(inputFields[6])"
                      @blur="handleBlur(inputFields[6])"
                      v-model="inputFields[6].value"
                    />
                    <label>Verification Code</label>
                  </div>
                  <button
                    type="button"
                    v-if="isSended"
                    class="verification-code"
                    @click="getVerificationCode"
                  >
                    Get Verification Code
                  </button>
                  <button v-else disabled="true" class="verification-code">
                    {{ clock.time_code }}s后重新发送
                  </button>
                  <input
                    type="submit"
                    value="Sign Up"
                    class="sign-btn"
                    @submit.prevent="signUp"
                  />
                </form>
                <p class="text">
                  我已经阅读并同意
                  <a href="#" @click.prevent="terms_of_service">服务条款</a>和
                  <a href="#" @click.prevent="privacy_agreement">隐私协议</a>
                </p>
              </div>
            </form>
          </div>
          <!-- 轮播 -->
          <div class="carousel">
            <div class="images-wrapper">
              <img
                :src="`${imgUrl}/assets/${images[currentIndex].url}`"
                alt=""
                class="images"
              />
            </div>
            <div class="text-slider">
              <div class="text-wrap">
                <div
                  class="text-group"
                  :style="{
                    transform: `translateY(${-currentIndex * 2.2}rem)`,
                  }"
                >
                  <h2>闪电问卷</h2>
                  <h2>前所未有的</h2>
                  <h2>问卷体验</h2>
                </div>
              </div>
              <div class="bullets">
                <span
                  v-for="bullet in images"
                  :key="'bullet-' + bullet.index"
                  :class="{ active: currentIndex === bullet.index }"
                  @click="moveSlider(bullet.index)"
                ></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </body>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive } from "vue";
// import { useStore } from 'vuex'
import { useRouter } from "vue-router";
import { useRoute } from 'vue-router';
import {
  setUserId,
  getUserId,
  setUserAvatarURL,
  getUserEmail,
  setUserEmail,
  setUserMoney,
  imgUrl,
} from "../../http/cookies";
import {
  loginapi,
  getVerificationCodeapi,
  signUpapi,
} from "../../api/account/login";
import { ElMessageBox } from "element-plus";
const router = useRouter();
const route = useRoute()

//实现点击输入框后的样式变换

let answer_id = route.query.answer_id;

const inputFields = ref([
  { id: 1, value: "", isActive: false },
  { id: 2, value: "", isActive: false },
  { id: 3, value: "", isActive: false },
  { id: 4, value: "", isActive: false },
  { id: 5, value: "", isActive: false },
  { id: 6, value: "", isActive: false },
  { id: 7, value: "", isActive: false },
]);

function handleFocus(input) {
  input.isActive = true; // 当输入框获得焦点时，激活 active 类
}

function handleBlur(input) {
  if (input.value === "") {
    input.isActive = false; // 如果输入框没有内容，移除 active 类
  }
}

const passwordsMatch = computed(() => {
  return (
    inputFields.value[4].value === inputFields.value[5].value ||
    inputFields.value[5].value === ""
  );
});

//login提交
const handleLogin = async () => {
  console.log("尝试登录");
  console.log("用户名:", inputFields.value[0].value);
  console.log("密码:", inputFields.value[1].value);
  const formData = new FormData();
  formData.append("username", inputFields.value[0].value);
  formData.append("password", inputFields.value[1].value); // 注意这里使用的是 password1，与后端匹配

  try {
    loginapi(formData).then((response) => {
      console.log("登录成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      const username = response.data.username;
      const useremail = response.data.email;
      const picture_url = response.data.picture_url;
      const user_money = response.data.Flash_coin;
      switch (statusCode) {
        case 1:
          // alert("登录成功！");

          console.log("返回用户名:", username);
          console.log("返回邮箱:", useremail);
          console.log("返回头像:", picture_url);
          console.log("返回钱:", user_money);
          setUserId(username);
          console.log("用户名:", getUserId());
          setUserEmail(useremail);
          console.log("邮箱:", getUserEmail());
          setUserAvatarURL(picture_url);
          // router.push("/home");
          setUserMoney(user_money);
          ElMessageBox.alert("登录成功", "Success!", {
            confirmButtonText: "确定",
            callback: () => {
              console.log("answer_id", answer_id)
              if(answer_id != undefined && answer_id != -1){
                router.push({ name: 'answer', query: { q_id: answer_id } });
              }
              else{
                router.push("/home");
              }
            },
          });
          break;

        case -1:
          alert("请检查填写的内容！");
          break;

        case 2:
          alert("用户已登录！");
          break;

        case 3:
          alert("用户名不存在！");
          break;

        case 4:
          alert("用户名或密码错误！");
          break;

        case 5:
          alert("用户未通过邮件确认，请及时确认！");
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
  console.log("用户名:", inputFields.value[2].value);
  console.log("邮箱:", inputFields.value[3].value);
  console.log("密码:", inputFields.value[4].value);
  console.log("确认密码:", inputFields.value[5].value);

  const formData = new FormData();
  formData.append("username", inputFields.value[2].value);
  formData.append("password1", inputFields.value[4].value); // 注意这里使用的是 password1，与后端匹配
  formData.append("password2", inputFields.value[5].value);
  formData.append("email", inputFields.value[3].value);
  try {
    getVerificationCodeapi(formData).then((response) => {
      console.log("获取邮箱验证码成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          alert("获取成功！");
          isSended.value = !isSended.value;
          clock.time_code = 10;
          startCountDown();
          break;

        case -1:
          alert("请检查填写的内容！");
          break;

        case 2:
          alert("用户信息已被占有！");
          break;

        case 3:
          alert("用户邮箱已被占有！");
          break;

        case 4:
          alert("密码不合法！必须包含英文字母和数字,长度8~18位");
          break;

        case 5:
          alert("前后密码不一致！");
          break;

        case 6:
          alert("验证码发送失败！");
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

//sigup提交
const signUp = async () => {
  console.log("尝试注册");
  console.log("验证码:", inputFields.value[6].value);
  const formData = new FormData();
  formData.append("code", inputFields.value[6].value);
  try {
    signUpapi(formData).then((response) => {
      console.log("发送注册成功:", response.data);
      // 处理响应数据，例如保存token，跳转页面等
      const statusCode = response.data.status_code;
      switch (statusCode) {
        case 1:
          ElMessageBox.alert("注册成功", "Success!", {
            confirmButtonText: "确定",
            callback: () => {
              location.reload();
            },
          });
          // location.reload();
          break;

        case 2:
          alert("验证码无效！");
          break;

        case 3:
          alert("验证码过期！");
          break;

        default:
          alert("未知错误，请稍后重试");
      }
    });
  } catch (error) {
    console.error("注册失败:", error);
    // 处理错误，显示错误信息等
  }
};

//切换sign_in和sign_up

const isSignUpMode = ref(false);

function toggleSignUpMode() {
  isSignUpMode.value = !isSignUpMode.value;
}

//轮播图

const currentIndex = ref(0);
const images = [
  { id: 1, url: "login1.png", index: 0 },
  { id: 2, url: "login2.png", index: 1 },
  { id: 3, url: "login5.png", index: 2 },
];

function moveSlider(index) {
  currentIndex.value = index;
}

// 自动轮播功能
let intervalId = null;
const startAutoPlay = () => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.length;
  }, 3000); // 每3秒切换图片
};

const stopAutoPlay = () => {
  if (intervalId) {
    clearInterval(intervalId);
  }
};

onMounted(() => {
  startAutoPlay();
});

onUnmounted(() => {
  stopAutoPlay();
});

//实现服务条款

const terms_of_service = () => {
  // 在这里可以执行点击服务条款后的其他操作，然后进行页面跳转
  // router.push("/terms_of_service"); // 将'/terms'替换为服务条款页面的路由路径
  window.open(
    "https://flash-questionnaire.github.io/archives/服务条款",
    "_blank"
  );
};

const privacy_agreement = () => {
  // 在这里可以执行点击隐私协议后的其他操作，然后进行页面跳转
  // router.push("/privacy_agreement");
  window.open(
    "https://flash-questionnaire.github.io/archives/隐私协议",
    "_blank"
  );
};

const find_lost_password = () => {
  // 在这里可以执行点击忘记密码后的其他操作，然后进行页面跳转
  router.push("/changePw");
};

const go_back = () => {
  // 在这里可以执行点击忘记密码后的其他操作，然后进行页面跳转
  router.push("/home");
};
</script>

<style scoped>
*,
*::after,
*::before {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

body {
  font-family: "Poppins", sans-serif;
}

main {
  width: 100%;
  overflow: hidden;
  min-height: 100vh;
  padding: 2rem;
  background-color: #72adff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.error-message {
  margin-bottom: 15px;
  color: red;
}
.box {
  width: 100%;
  max-width: 1275px;
  height: 800px;
  background-color: #fff;
  position: relative;
  border-radius: 3.3rem;
  box-shadow: 0 60px 40px -30px rgba(0, 0, 0, 0.27);
}

.inner-box {
  position: absolute;
  width: calc(100% - 4.1rem);
  height: calc(100% - 4.1rem);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.forms-wrap {
  position: absolute;
  height: 100%;
  width: 45%;
  left: 0;
  top: 0;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  transition: 0.8s ease-in-out;
}

form {
  max-width: 260px;
  width: 100%;
  margin: 0 auto;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  grid-column: 1/2;
  grid-row: 1/2;
  transition: opacity 0.02s 0.4s;
}

form.sign-up-form {
  opacity: 0;
  pointer-events: none;
}

.logo1 {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px; /* 可调整logo与边界的距离 */
}

.logo1 img {
  height: 27px;
  margin-right: 0.3rem;
  width: 27px;
}

.logo1 h4 {
  font-size: 1.4rem;
  letter-spacing: -0.5px;
  color: #151111;
}

.logo2 {
  display: flex;
  position: absolute;
  top: 0;
  right: 0;
  padding: 10px; /* 可调整logo与边界的距离 */
}

.logo2 img {
  height: 27px;
  margin-right: 0.3rem;
  width: 27px;
}

.logo2 h4 {
  font-size: 1.4rem;
  letter-spacing: -0.5px;
  color: #151111;
}

.heading h2 {
  font-size: 2.4rem;
  font-weight: 600;
  color: #151111;
}

.heading h6 {
  color: #bababa;
  font-weight: 400;
  font-size: 0.9rem;
  display: inline;
}

.toggle {
  color: #151111;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: 0.3s;
}

.toggle:hover {
  color: #8371fd;
}

.input-wrap1 {
  position: relative;
  height: 50px;
  margin-bottom: 2rem;
}

.input-wrap2 {
  position: relative;
  height: 37px;
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.input-field {
  position: absolute;
  width: 100%;
  height: 100%;
  background: none;
  border: none;
  outline: none;
  border-bottom: 1px solid #bbb;
  padding: 0;
  font-size: 0.95rem;
  color: #151111;
  transition: 0.4s;
}

label {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.95rem;
  color: #bbb;
  pointer-events: none;
  transition: 0.4s;
}

.input-field.active {
  border-bottom-color: #151111;
}

.input-field.active + label {
  font-size: 0.75rem;
  top: -2px;
}

.verification-code {
  display: inline-block;
  width: 50%;
  height: 43px;
  background-color: hsl(205, 78%, 44%);
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 0.8rem;
  font-size: 0.8rem;
  margin-bottom: 2rem;
  transition: 0.3s;
}

.verification-code:hover {
  background-color: #8371fd;
}

.sign-btn {
  display: inline-block;
  width: 100%;
  height: 43px;
  background-color: #151111;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 0.8rem;
  font-size: 0.8rem;
  margin-bottom: 4rem;
  transition: 0.3s;
}

.back-btn {
  display: inline-block;
  left: 0;
  width: 50%;
  height: 43px;
  background-color: #151111;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 0.8rem;
  font-size: 0.8rem;
  margin-bottom: 2rem;
  transition: 0.3s;
}

.back-btn:hover {
  background-color: #8371fd;
}

.sign-btn:hover {
  background-color: #8371fd;
}

.text {
  color: #bbb;
  font-size: 0.9rem;
}

.text a {
  color: #bbb;
  transition: 0.3s;
}

.text a:hover {
  color: #8371fd;
}

main.sign-up-mode form.sign-in-form {
  opacity: 0;
  pointer-events: none;
}

main.sign-up-mode form.sign-up-form {
  opacity: 1;
  pointer-events: all;
}

main.sign-up-mode .forms-wrap {
  left: 55%;
}

main.sign-up-mode .carousel {
  left: 0%;
}

.carousel {
  background-color: #8cdcfc;
  border-radius: 2rem;
  padding: 2rem;
  overflow: hidden;
  position: absolute;
  height: 100%;
  width: 55%;
  left: 45%;
  top: 0;
  /* background-color: #ffe0d2; */
  border-radius: 2rem;
  display: grid;
  transition: 0.8s ease-in-out;
  overflow: hidden;
  position: relative;
  grid-template-rows: auto 1fr;
}

.images-wrapper {
  display: grid;
  grid-template-columns: 2fr;
  grid-template-rows: 1fr;
  width: 70%;
  height: 70%;
  margin: auto;
}

.images {
  display: grid;
  place-items: center; /* 居中项 */
  height: 40vh;
  width: 100%; /* 确保图片宽度填充容器 */
  grid-column: 1/2;
  grid-row: 1/2;
  opacity: 1; /* 确保图片完全不透明 */
  transition: opacity 0.3s, transform 0.5s;
}
.image.show {
  display: block;
}

.text-slider {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.text-wrap {
  max-height: 2.2rem;
  overflow: hidden;
  margin-bottom: 2.5rem;
}

.text-group {
  display: flex;
  flex-direction: column;
  text-align: center;
  transform: translateY(0);
  transition: 0.5s;
}

.text-group h2 {
  line-height: 2.2rem;
  font-weight: 600;
  font-size: 1.6rem;
}

.bullets {
  display: flex;
  align-items: center;
  justify-content: center;
}

.bullets span {
  display: block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 0.2rem;
  background-color: #aaa;
  margin: 0 0.25rem;
  cursor: pointer;
  transition: 0.3s;
}

.bullets span.active {
  width: 1.1rem;
  background-color: #151111;
  border-radius: 1rem;
}

@media (max-width: 850px) {
  .box {
    height: auto;
    max-width: 550px;
    overflow: hidden;
  }
  .inner-box {
    position: static;
    transform: none;
    width: revert;
    height: revert;
    padding: 2rem;
  }

  .forms-wrap {
    position: revert;
    width: 100%;
    height: 100%;
  }

  form {
    max-width: revert;
    padding: 1.5rem, 2.5rem, 2rem;
    transition: transform 0.8s ease-in-out, opacity 0.45s linear;
  }

  .heading {
    margin: 2rem 0;
  }
  form.sign-up-form {
    transform: translateX(100%);
  }
  main.sign-up-mode form.sign-in-form {
    transform: translateX(-100%);
  }

  main.sign-up-mode form.sign-up-form {
    transform: translateX(0%);
  }

  .carousel {
    position: revert;
    height: auto;
    width: 100%;
    padding: 3rem 2rem;
    display: flex;
  }

  .images-wrapper {
    display: none;
  }

  .images {
    display: grid;
    place-items: center; /* 居中项 */
    height: 40vh;
    grid-column: 1/2;
    grid-row: 1/2;
    opacity: 0; /* 确保图片完全不透明 */
    transition: opacity 0.3s, transform 0.5s;
  }

  .text-slider {
    width: 100%;
  }
}

@media (max-width: 530px) {
  main {
    padding: 1rem;
  }
  .box {
    border-radius: 2rem;
  }
  .inner-box {
    padding: 1rem;
  }

  .image {
    display: grid;
    place-items: center; /* 居中项 */
    height: 40vh;
    grid-column: 1/2;
    grid-row: 1/2;
    opacity: 1; /* 确保图片完全不透明 */
    transition: opacity 0.3s, transform 0.5s;
  }

  .carousel {
    padding: 1.5rem 1rem;
    border-radius: 1.6rem;
  }
  .text-wrap {
    margin-bottom: 1rem;
  }
  .text-group h2 {
    font-size: 1.2rem;
  }
  form {
    padding: 1rem 2rem 1.5rem;
  }
}
</style>
