<template>
  <main class="app-main">
    <RouterView />
  </main>
</template>

<script setup>
import { computed } from 'vue';

// 토큰 존재 여부 계산
const showNavbar = computed(() => !!localStorage.getItem('token'));
// console.log(showNavbar.value);
</script>

<style scoped>

.app-main {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100vh; /* 화면 높이를 고정 */
  background-color: #1F509A; /* home.vue와 일치 */
  position: relative; /* 자식 요소의 위치 제어 */
  overflow: hidden; /* 불필요한 스크롤 방지 */
}


</style>
