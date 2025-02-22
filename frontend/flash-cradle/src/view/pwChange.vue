<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { changePw, getCode } from "../../api/account/pwchange"
import {imgUrl} from '../../http/cookies'
const isSended = ref(true);
const change = ref(true);
const triggerLogin = ref(false);
const timeToLogin = ref(0);
const router = useRouter();
const meg = reactive({
  emailMeg: "",
  pwMeg: "",
});
const inputFields = ref([
  { id: 1, value: "", isActive: false },
  { id: 2, value: "", isActive: false },
  { id: 3, value: "", isActive: false },
  { id: 4, value: "", isActive: false },
  { id: 5, value: "", isActive: false },
]);
function handleFocus(input) {
  input.isActive = true;
}
function handleBlur(input) {
  if (input.value === "") {
    input.isActive = false;
  }
}
const clock = reactive({
  time_code: 0,
  time_email_meg: 0,
  time_pw_meg: 0,
});
const timer = reactive({
  timer_code: null,
  timer_email_meg: null,
  timer_pw_meg: null,
});

const callBack = (num, errMeg) => {
  switch (num) {
    case 1:
      meg.emailMeg = errMeg;
      clock.time_email_meg = 5;
      startCountDown(2);
      break;
    case 2:
      meg.pwMeg = errMeg;
      clock.time_pw_meg = 5;
      startCountDown(3);
      break;
  }
};
const startCountDown = (num) => {
  switch (num) {
    case 1:
      if (timer.timer_code) clearInterval(timer.timer_code);
      timer.timer_code = setInterval(() => {
        clock.time_code--;
        if (clock.time_code === 0) {
          clearInterval(timer.timer_code);
          isSended.value = !isSended.value;
        }
      }, 1000);
      break;
    case 2:
      if (timer.timer_email_meg) clearInterval(timer.timer_email_meg);
      timer.timer_email_meg = setInterval(() => {
        clock.time_email_meg--;
        if (clock.time_email_meg === 0) {
          clearInterval(timer.timer_email_meg);
          meg.emailMeg = "";
        }
      }, 1000);
      break;
    case 3:
      if (timer.timer_pw_meg) clearInterval(timer.timer_pw_meg);
      timer.timer_pw_meg = setInterval(() => {
        clock.time_pw_meg--;
        if (clock.time_pw_meg === 0) {
          clearInterval(timer.timer_pw_meg);
          meg.pwMeg = "";
        }
      }, 1000);
      break;
  }
};
//延时跳转到登录
const delayJumpToLogin = () => {
  triggerLogin.value = !triggerLogin.value;
  let timerToLogin = null;
  timeToLogin.value = 3;
  if (timerToLogin) clearInterval(timerToLogin);
  timerToLogin = setInterval(() => {
    timeToLogin.value--;
    if (timeToLogin.value === 0) {
      clearInterval(timerToLogin);
      goLogin();
    }
  }, 1000);
};
const getVerifiedCode = () => {
  const userInfo = {
    username: inputFields.value[4].value,
    email: inputFields.value[0].value,
  };
  if(userInfo.username == null || userInfo.email == null)return;
  if(userInfo.username == "" || userInfo.email == "")return;
  isSended.value = !isSended.value;
  clock.time_code = 10;
  startCountDown(1);
  getCode(userInfo)
    .then((res) => {
      switch (res.data.status_code) {
        case 1:
          callBack(1, "邮件发送成功");
          change.value = false;
          break;
        case 2:
          callBack(1, "用户不存在");
          break;
        case 3:
          callBack(1, "验证码发送失败");
          break;
        case 4:
          callBack(1, "用户未进行邮箱绑定");
          break;
        case 5:
          callBack(1, "用户邮箱错误");
          break;
        case -1:
          callBack(1, "输入数据格式错误");
          break;
        case -2:
          callBack(1, "请求类型错误");
          break;
        default:
          break;
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
const changePassword = () => {
  if(inputFields.value[1].value == null)return;
  const verifyInfo = {
    code: inputFields.value[1].value,
    password_1: inputFields.value[2].value,
    password_2: inputFields.value[3].value,
  };
 changePw(verifyInfo)
    .then((res) => {
      switch (res.data.status_code) {
        case 1:
          callBack(2, "密码重设成功");
          delayJumpToLogin();
          break;
        case 2:
          callBack(2, "验证码错误");
          break;
        case 3:
          callBack(2, "验证码过期");
          break;
        case 4:
          callBack(2, "前后密码不一致");
          break;
        case 5:
          callBack(2, "新密码不合法");
          break;
        case -1:
          callBack(2, "输入数据格式错误");
          break;
        case -2:
          callBack(2, "请求类型错误");
          break;
        default:
          break;
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
const goLogin = () => {
  router.push("/login");
};
const goHome = () => {
  router.push("/");
};
</script>

<template>
  <body>
    <div class="main">
      <div class="getPw">
        <div class="heading" :class="{change:change}">
          <div class="logo">
            <img
              :src="`${imgUrl}/assets/flashq.png`"
              alt="logo"
              id="img-logo"
              @click.prevent="goHome"
            />
            <h2 id="logo-explain" @click.prevent="goHome">闪电问卷</h2>
          </div>
          <div class="head-title">
            <h2 id="head-title">修改密码</h2>
            <div class="head-title-meg">
              <h2 id="head-title-meg">remember the password?</h2>
              <a href="#" @click="goLogin" id="gotoLogin">sign in</a>
            </div>
          </div>
        </div>
        <div class="form-wrap">
          <div class="form-box">
            <form @submit.prevent="getVerifiedCode" class="email-form" v-if="change">
              <div class="form-group">
                <input
                  type="text"
                  autocomplete="off"
                  required
                  :key="inputFields[4].id"
                  @focus="handleFocus(inputFields[4])"
                  @blur="handleBlur(inputFields[4])"
                  class="form-control"
                  :class="{ active: inputFields[4].isActive }"
                  v-model="inputFields[4].value"
                />
                <label class="input-label">用户名</label>
              </div>
              <div class="form-group">
                <input
                  type="email"
                  autocomplete="off"
                  required
                  :key="inputFields[0].id"
                  @focus="handleFocus(inputFields[0])"
                  @blur="handleBlur(inputFields[0])"
                  class="form-control"
                  :class="{ active: inputFields[0].isActive }"
                  v-model="inputFields[0].value"
                />
                <label class="input-label">邮箱</label>
              </div>
              <div class="form-group">
                <button type="submit" v-if="isSended" class="btn">
                  发送验证码
                </button>
                <button v-else disabled="true" class="btn">
                  {{ clock.time_code }}s后重新发送
                </button>
              </div>
              <div class="err-message">
                {{ meg.emailMeg }}
              </div>
            </form>
            <form @submit.prevent="changePassword" class="password-form" v-else>
              <div class="form-group">
                <input
                  type="text"
                  autocomplete="off"
                  :key="inputFields[1].id"
                  @focus="handleFocus(inputFields[1])"
                  @blur="handleBlur(inputFields[1])"
                  class="form-control"
                  :class="{ active: inputFields[1].isActive }"
                  v-model="inputFields[1].value"
                />
                <label class="input-label">验证码</label>
              </div>
              <div class="form-group">
                <input
                  type="password"
                  autocomplete="off"
                  required
                  :key="inputFields[2].id"
                  @focus="handleFocus(inputFields[2])"
                  @blur="handleBlur(inputFields[2])"
                  class="form-control"
                  :class="{ active: inputFields[2].isActive }"
                  v-model="inputFields[2].value"
                />
                <label class="input-label">新密码</label>
              </div>
              <div class="form-group">
                <input
                  type="password"
                  autocomplete="off"
                  required
                  :key="inputFields[3].id"
                  @focus="handleFocus(inputFields[3])"
                  @blur="handleBlur(inputFields[3])"
                  class="form-control"
                  :class="{ active: inputFields[3].isActive }"
                  v-model="inputFields[3].value"
                />
                <label class="input-label">确认密码</label>
              </div>
              
              <div class="form-group">
                <button type="submit" class="btn">修改密码</button>
              </div>
              <div class="err-message">
                {{ meg.pwMeg }}
              </div>
            </form>
          </div>
        </div>
        <div v-if="triggerLogin" class="delayJumpToLogin">
          <span class="countTime">{{ timeToLogin }}</span
          >s后自动跳转至<a href="#" @click="goLogin()" id="delayJump">登录</a>
        </div>
      </div>
    </div>
  </body>
</template>

<style  scoped>
body {
  font-family: "Poppins", sans-serif;
}
.main {
  box-sizing: border-box;
  overflow: hidden;
  width: 100%;
  /* min-width: 400px; */
  min-height: 100vh;
  background-color: #72adff;
  display: flex;
  padding: 2rem;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}
.getPw {
  width: 100%;
  max-width: 1020px;
  height: 640px;
  padding: 2rem;
  position: relative;
  border-radius: 3.3rem;
  background-color: #ffffff;
  box-shadow: 0 60px 40px -30px rgba(0, 0, 0, 0.27);
}
.heading {
  width: 100%;
  display: block;
  display: absolute;
  margin-bottom: 5px;
}
.heading.change{
  width: 100%;
  display: block;
  display: absolute;
  margin-bottom: 30px;
}
.logo {
  display: flex;
  position: relative;
  top: 0;
  padding-bottom: 10px;
}
#img-logo {
  width: 100px;
  height: 100px;
  cursor: pointer;
}
#logo-explain {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  cursor: pointer;
}
.head-title {
  position: relative;
  top: -30px;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
}
#head-title {
  font-size: 2.4rem;
  font-weight: 600;
  color: #151111;
  margin: 0;
}
.head-title-meg {
  padding-top: 10px;
}
#head-title-meg {
  color: #bababa;
  font-weight: 400;
  font-size: 0.9rem;
  display: inline;
}
#gotoLogin {
  font-size: 0.9rem;
  font-weight: 500;
  color: #151111;
  cursor: pointer;
  text-decoration: none;
}
.middle {
  display: flex;
  justify-content: center;
  align-content: center;
  margin-bottom: 20px;
}
.changePage {
  color: #71b3e9;
}
.changePage.change {
  color: #e94f4f;
}
.form-wrap {
  padding: 0 auto;
  width: 100%;
  height: 55%;
}

.form-box {
  display: flex;
  align-content: center;
  justify-content: center;
  height: 100%;
}
.email-form,
.password-form {
  flex: 1;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.email-form {
  padding-right: 20px;
}
.jump-link {
  display: flex;
}

.form-group {
  display: flex;
  justify-content: center;
  align-content: center;
  position: relative;
  margin-bottom: 2.5rem;
  height: 37px;
}
.form-control {
  position: absolute;
  width: 40%;
  height: 100%;
  background-color: none;
  border: none;
  outline: none;
  border-bottom: 1px solid #bbb;
  padding: 0;
  font-size: 1.05rem;
  color: #151111;
  transition: 0.4s;
}
.form-control.active {
  border-bottom-color: #151111;
}
.input-label {
  position: absolute;
  left: 30%;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.95rem;
  color: #bbb;
  pointer-events: none;
  transition: 0.4s;
}
.form-control.active + .input-label {
  font-size: 1.05rem;
  top: -3px;
}
.btn {
  display: inline-block;
  height: 50px;
  width: 40%;
  border: none;
  border-radius: 5px;
  background-color: #87ceeb;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.5s ease, color 0.5s ease, box-shadow 0.5s ease;
  cursor: pointer;
}
.btn:hover {
  background-color: #71b3e9;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
  transition: none;
}
.err-message {
  color: #d83434;
  text-align: center;
}
.countTime {
  font: bold;
}
.delayJumpToLogin {
  text-align: center;
}
#delayJump {
  text-decoration: none;
  color: #71b3e9;
  cursor: pointer;
}
</style>
