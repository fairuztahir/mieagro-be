<template>
  <v-app>
    <DashboardCoreDrawer />
    <DashboardCoreAppBar />
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
    expandOnHover: false
  })
})
</script>
