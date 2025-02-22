<template>
  <div class="root">
    <RouterView></RouterView>
  </div>
</template>

<script setup>
  import { RouterView } from 'vue-router';
</script>

<style>
.root{
  width:100%;
  height: 100%;
  position: fixed;
  background: rgb(249, 251, 255) center center !important;
  background-size: 100% 100% !important;
  overflow: scroll;
}

.root::-webkit-scrollbar {
  display: none;
}

body {
  margin: 0;
  padding: 0;
}
</style>
