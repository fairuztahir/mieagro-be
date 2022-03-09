<template>
  <v-app id="home" :theme="theme" class="app-container">
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
  // height: 100vh
  // background-color: rgb(215, 252, 207, 0.87)
</style>

<style>
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
</style>
