<template>
  <v-app>
    <DashboardCoreDrawer />
    <DashboardCoreAppBar :title="titleName" />
    <DashboardCoreView />
    <DashboardCoreFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DashboardCoreDrawer from './DrawerLayout.vue'
import DashboardCoreAppBar from './AppBar.vue'
import DashboardCoreView from './ViewLayout.vue'
import DashboardCoreFooter from './FooterLayout.vue'
export default defineComponent({
  components: {
    DashboardCoreDrawer,
    DashboardCoreAppBar,
    DashboardCoreView,
    DashboardCoreFooter
  },
  data: () => ({
    titleName: 'Home'
  })
  // setup() {
  //   const title = ref('Home')

  //   // expose to template and other options API hooks
  //   return {
  //     title
  //   }
  // }
  // props: {
  //   title: String
  // }
  // data() {
  //   return {
  //     titleName: this.pageTitle
  //   }
  // }
})
</script>
