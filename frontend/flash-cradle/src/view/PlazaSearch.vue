<template>
<div class="window">
    <div class="header">
        <div class="header-logo">
            <img :src="`${imgUrl}/assets/flashq.svg`" alt="SVG" class="logo">
            <span class="describe">查找问卷</span>
        </div>
        <div class="header-input">
            <input class="search-input" placeholder="请在此输入您想找的问卷" v-model="searchInput" ref="searchInputRef">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" style="color: lightgrey" @click="submitSearch"><path fill="currentColor" d="M9.5 16q-2.725 0-4.612-1.888T3 9.5t1.888-4.612T9.5 3t4.613 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l5.6 5.6q.275.275.275.7t-.275.7t-.7.275t-.7-.275l-5.6-5.6q-.75.6-1.725.95T9.5 16m0-2q1.875 0 3.188-1.312T14 9.5t-1.312-3.187T9.5 5T6.313 6.313T5 9.5t1.313 3.188T9.5 14"/></svg>
        </div>
    </div>
</div>
</template>

<script scoped>
import { imgUrl } from '../../http/cookies';
export default {
  name: 'PlazaSearch',
  data() {
    return {
        imgUrl: imgUrl,
      searchInput: '',
    };
  },
  created() {
    const inputParam = this.$route.query.input;
    if (inputParam) {
      this.searchInput = inputParam;
    }
  },
  methods: {
    submitSearch() {
        const inputContent = this.$refs.searchInputRef.value;
        this.$router.replace({ path: '/plaza/search', query: { input: inputContent} });
        this.searchInput=inputContent;
    },
  }
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
    font-family: Arial, Helvetica, sans-serif;
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
    left: 5px;
    min-width: 200px;
}
.logo {
    position: absolute;
    top: 10%;
    height: 80%;
}
.describe {
    position: absolute;
    top: 2px;
    left: 50px;
    font-size: 30px;
}
.header-input {
    position: absolute;
    left: 25%;
    text-align: center;
    padding: 0;
    width: 50vw;
    border: 0;
}
.search-input {
    position: absolute;
    top: 12px;
    left: 0px;
    font-size: 15px;
    text-indent: 10px;
    border: 1px solid grey;
    width: 50vw;
    height: 30px;
    border-radius: 5px;
}
.search-input:hover {
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
}
.search-input:focus{
    border: 1px solid #007bff;
}
.search-icon {
    position: absolute;
    top: 14px;
    right: -4px;
    width: 30px;
    height: 30px;
}
@media (max-width: 750px) {
    .describe {
        display: none;
    }
}
</style>