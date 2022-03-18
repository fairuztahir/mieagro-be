<template>
  <v-app id="home" :theme="theme" class="app-container">
    <div class="squares square1"></div>
    <!-- <div class="squares square2"></div> -->
    <div class="squares square3"></div>
    <div class="squares square4"></div>
    <div class="squares square5"></div>
    <div class="squares square6"></div>
    <DashboardCoreAppBar />
    <DashboardCoreView />
    <DashboardCoreFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import DashboardCoreAppBar from './AppBar.vue'
import DashboardCoreView from './ViewLayout.vue'
import DashboardCoreFooter from './FooterLayout.vue'
export default defineComponent({
  name: 'WebLayout',
  components: {
    DashboardCoreAppBar,
    DashboardCoreView,
    DashboardCoreFooter
  },
  setup() {
    const theme = ref('light')

    return {
      theme,
      toggleTheme: () => (theme.value = theme.value === 'light' ? 'dark' : 'light')
    }
  }
})
</script>

<style lang="sass" scoped>
.v-application
  // background: linear-gradient(87deg, rgb(205, 250, 168), rgb(255, 255, 255))
  background: linear-gradient(87deg, #2dd4bf, #f0fdfa)
</style>

<style lang="css">
* {
  scrollbar-width: thin;
  scrollbar-color: rgb(221, 220, 218) rgb(228, 228, 227);
}

*::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
*::-webkit-scrollbar-track {
  background: rgb(228, 228, 227);
  width: 5px;
  height: 5px;
}
*::-webkit-scrollbar-thumb {
  background-color: rgb(190, 190, 190);
  border-radius: 5px;
  border: 0px rgb(221, 220, 218);
}

@keyframes move-left-right {
  0% {
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(10px);
  }
  100% {
    transform: translateX(-10px);
  }
}

.app-container .squares {
  animation: move-left-right 1s infinite;
  background: #ba54f5;
  background: -webkit-linear-gradient(0deg, #04a791 0%, #19ad8b 100%);
  background: -o-linear-gradient(0deg, #04a791 0%, #19ad8b 100%);
  background: -moz-linear-gradient(0deg, #04a791 0%, #19ad8b 100%);
  background: linear-gradient(0deg, #04a791 0%, #19ad8b 100%);
  position: absolute;
  transition: 0.5s ease-out;
  overflow: hidden;
  border-radius: 20%;
}

.app-container .squares.square1 {
  animation: move-left-right 4s infinite;
  height: 300px;
  width: 300px;
  opacity: 0.5;
  left: 3%;
  top: -200px;
  /* top: -21%; */
}

.app-container .squares.square2 {
  animation: move-left-right 6s infinite;
  height: 400px;
  width: 400px;
  opacity: 0.1;
  right: -5%;
  top: -12%;
}

.app-container .squares.square3 {
  animation: move-left-right 5s infinite;
  height: 200px;
  width: 200px;
  opacity: 0.1;
  left: -5%;
  bottom: 2%;
}

.app-container .squares.square4 {
  animation: move-left-right 6s infinite;
  height: 250px;
  width: 250px;
  opacity: 0.1;
  left: 22%;
  bottom: 20%;
}

.app-container .squares.square5 {
  animation: move-left-right 9s infinite;
  left: 10%;
  top: 35%;
  height: 80px;
  width: 80px;
  opacity: 0.2;
}

.app-container .squares.square6 {
  animation: move-left-right 3s infinite;
  width: 300px;
  height: 300px;
  right: -5%;
  bottom: 0%;
  opacity: 0.1;
}
</style>
