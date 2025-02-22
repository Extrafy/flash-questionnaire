<template>
    <div class="window">
        <el-drawer title="功能列表" :with-header="true" :custom-class="'custom-drawer'" :direction="'ttb'" :size="270" v-model="drawer">
            <div class="drawer-element" @click="go_plaza">广场</div>
            <div class="drawer-element" @click="go_console">控制台</div>
            <div class="drawer-element" @click="go_help">帮助</div>
            <div class="drawer-element">关于</div>
        </el-drawer>
        <div class="header">
            <div class="header-logo">
                <img :src="`${imgUrl}/assets/flashq.svg`" alt="SVG" class="logo" @click="open_drawer" style="width:50px;height:50px;">
            </div>
            <div class="header-navigation">
                <span class="title">flashq.net</span>
                <div class="navigation-bar navigation-bar1" @click="go_plaza">广场</div>
                <div class="navigation-bar navigation-bar2" @click="go_console">控制台</div>
                <div class="navigation-bar navigation-bar3" @click="go_help">帮助</div>
                <div class="navigation-bar navigation-bar4" @click="go_about">关于</div>
            </div>
            <div class="header-login">
                <button v-if="!login_status" class="login-button" @click="go_login">登录/注册</button>
                <el-avatar v-if="login_status" class="avatar" @click="go_user" shape="square" :size="40" :src="avatar_url"/>
            </div>
        </div>
        <div class="body3">
            <div class="word3">
                <div style="font-size: 100px; color: white; font-family: Arial, Helvetica, sans-serif;">极速创建</div>
                <TextAnimation :dText="['调查问卷', '考试试卷', '报名表']" :fontSize="'100px'" :fontColor="'white'"></TextAnimation>
            </div>
            <img :src="`${imgUrl}/assets/icon3.png`" class="icon3"> 
        </div>
        <div class="body1">
            <div class="word1">
                <TextAnimation :dText="['手机端', '平板端', '电脑端']" :fontSize="'100px'" :fontColor="'rgb(38, 111, 185)'"></TextAnimation>
                <div style="font-size: 100px; color: rgb(38, 111, 185); font-family: Arial, Helvetica, sans-serif;">随处可用</div> 
            </div>
            <img :src="`${imgUrl}/assets/icon1.png`" class="icon1"> 
        </div>
        <div class="body2">
            <div class="word2">
                <TextAnimation :dText="['数据分析', '交叉分析']" :fontSize="'100px'" :fontColor="'rgb(38, 111, 185)'"></TextAnimation>
                <div style="font-size: 100px; color: rgb(38, 111, 185); font-family: Arial, Helvetica, sans-serif;">无所不能</div> 
            </div>
            <img :src="`${imgUrl}/assets/icon2.png`" class="icon2"> 
        </div>
    </div>
</template>

<script>
import TextAnimation from './TextAnimation.vue';
import { getUserId, getUserAvatarURL, imgUrl } from '../../http/cookies';
import { ElDrawer, ElAvatar } from 'element-plus';
export default {
  name: "HomeItem",
  components: {
    TextAnimation,
    ElDrawer,
    ElAvatar,
  },
  data() {
    return {
        imgUrl: imgUrl,
        login_status: false,
        drawer: false,
        avatar_url: "https://s2.loli.net/2024/05/14/goXsDLbJqTMwUka.png"
    };
  },
  mounted() {
    if (getUserId() !== undefined) {
        this.login_status = true;
        this.avatar_url = "https://s2.loli.net/2024/05/14/goXsDLbJqTMwUka.png";
        if (getUserAvatarURL() !== undefined)
            this.avatar_url = getUserAvatarURL();
    }
  },
  methods :{
    go_login(){
        this.$router.push('/login');
    },
    go_console(){
        this.$router.push('/console');
    },
    go_plaza(){
        window.open('/plaza', '_blank');
    },
    go_help(){
        window.open('https://flash-questionnaire.github.io/', '_blank');
    },
    go_about(){
        window.open('https://flash-questionnaire.github.io/archives/关于我们', '_blank');
    },
    go_user(){
        this.$router.push('/person');
    },
    open_drawer() {
        if (window.innerWidth <= 800)
            this.drawer=true;
    }
  }
  
};
</script>

<style scoped>
    .drawer-element {
        font-size: 20px;
        font-family: "Arial";
        text-align: center;
        padding: 5px;
    }
    .drawer-element:hover {
        cursor:pointer;
        background-color: aliceblue;
    }
    .window {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow-x: hidden;
        overflow-y: scroll;
    }
    .header {
        width: 100%;
        height: 60px;
        line-height: 60px;
        position: sticky;
        z-index: 999;
        left: 0;
        top: 0;
        background-color: white;
        box-shadow: 0px 0px 2px grey inset;
        opacity: 0.9;
    }
    .header-logo {
        position: absolute;
        height: 100%;
        left: 0;
        
        min-width: 50px;
    }
    .logo {
        position: absolute;
        top: 10%;
        height: 80%;
    }
    .title {
        display: inline-block;
        color:rgb(38, 111, 185);
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight:420;
        font-size:25px;
    }
    .header-navigation {
        position: absolute;
        max-width: 55%;
        height: 100%;
        left: 60px;
    }
    .navigation-bar {
        display: inline-block;
        width:80px;
        max-width: 25%;
        height: 100%;
        font-family: "Arial";
        font-size: 18px;
        text-align: center;
    }
    .navigation-bar:hover {
        color: rgb(60, 138, 216);
        cursor: pointer;
    }
    .header-login {
        position: absolute;
        right: 0px;
        width: 120px;
    }
    .login-button {
        position: absolute;
        top: 11px;
        padding: 9px 17px;
        font-size: 16px;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        background-color: #007bff;
        transition: background-color 0.3s;
    }
    .login-button:hover {
        background-color: #0056b3;
    }
    .avatar {
        position: absolute;
        top: 11px;
        right: 10px;
        box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
        cursor: pointer;
    }
    .avatar:hover{
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
    }
    .body1, .body2, .body3 {
        position: absolute;
        left: 0;
        width: 100%;
        height: 100vh; 
    }
    .body1 {
        top: 200%;
        background: url(https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com/assets/greybg.png) center center;
        background-size: 100% auto;
    }
    .body2 {
        top: 100%;
        background: url(https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com/assets/tribg.png) center center;
        background-size: 100% auto;
    }
    .body3 {
        top: 0;
        background: url(https://flash-questionnaire-exp.oss-cn-beijing.aliyuncs.com/assets/bluebg.png) center center;
        background-size: 100% auto;
    }
    .word1, .word2, .word3 {
        position: absolute;
        top: 30%;
        left: 10%;
    }
    .icon1, .icon2, .icon3 {
        width: 50%;
        position: absolute;
        left: 45%;
        top: 20%;
    }
    .custom-drawer.el-drawer {
        transition: transform 0.3s; 
        overflow: hidden; 
    }
    .custom-drawer.el-drawer.el-drawer-fade-enter-active,
    .custom-drawer.el-drawer.el-drawer-fade-leave-active {
        transition: transform 0.3s;
    }
    @media (max-width: 1200px) {
        .icon1, .icon2, .icon3 {
            width: 40%;
            position: absolute;
            left: 60%;
            top: 30%;
        }
    }
    @media (max-width: 800px) {
        .word1, .word2, .word3 {
            position: absolute;
            top: 10%;
            left: 15%;
        }
        .icon1, .icon2, .icon3 {
            width: 70%;
            position: absolute;
            left: 15%;
            top: 50%;
        }
        .navigation-bar {
            display: none;
        }
        .animation {
            margin-top: 15%;
        }
        .animation-wrapper {
            padding-top: 20%;
        }
        .logo:hover {
            cursor: pointer;
        }  
    }
</style>