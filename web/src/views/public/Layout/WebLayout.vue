<template>
  <v-app id="home" :theme="theme">
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

<style scoped>
.v-application {
  background-color: rgb(215, 252, 207, 0.87);
}
</style>
