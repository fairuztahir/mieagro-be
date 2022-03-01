<template>
  <v-app>
    <dashboard-core-drawer />
    <dashboard-core-app-bar />
    <dashboard-core-view />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DashboardCoreDrawer from './Drawer.vue'
import DashboardCoreAppBar from './AppBar.vue'
import DashboardCoreView from './View.vue'
export default defineComponent({
  name: 'DashboardLayout',
  components: {
    DashboardCoreDrawer,
    DashboardCoreAppBar,
    DashboardCoreView
  },
  data: () => ({
    expandOnHover: false
  })
})
</script>
