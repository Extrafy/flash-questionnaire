<template>
    <div style="width: 100%; height: 60px; position: absolute; left: 0; top: 0; background-color: white; box-shadow: 0px 0px 2px grey inset; opacity: 0.9;">
        <img :src="`${imgUrl}/assets/flashq.svg`" alt="SVG" class="logo" style="position: absolute; top:5px; left:0; width: 50px; height: 50px;">
        <span style="position: absolute; top:0; left: 60px; color:rgb(38, 111, 185); font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size:25px; height: 60px; line-height: 60px;cursor: pointer;" @click="toHome()">flashq.net</span>
        <el-avatar class="avatar" @click="go_user" shape="square" :size="40" :src="avatar_url"/>
    </div>
</template>

<script>
import { getUserId, getUserAvatarURL,imgUrl } from '../../http/cookies';
import { ElAvatar } from "element-plus";
export default {
    name: "ConsoleHeader",
    components:{
        ElAvatar,
    },
    data() {
        return {
            imgUrl: imgUrl,
            login_status: false,
            avatar_url: "https://s2.loli.net/2024/05/14/goXsDLbJqTMwUka.png"
        };
    },
    methods :{
        go_user(){
            this.$router.push('/person');
        },
        toHome(){
            this.$router.push('/home');
        }
    },
    mounted() {
    if (getUserId() !== undefined) {
        this.avatar_url = "https://s2.loli.net/2024/05/14/goXsDLbJqTMwUka.png";
        if (getUserAvatarURL() !== undefined)
            this.avatar_url = getUserAvatarURL();
    }
  },
}
</script>

<style scoped>
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
</style>