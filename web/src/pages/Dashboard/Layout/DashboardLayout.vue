<template>
  <v-app>
    <dashboard-core-drawer />
    <dashboard-core-app-bar />
    <dashboard-core-view />
    <dashboard-core-footer />
  </v-app>
</template>

<script>
import DashboardCoreDrawer from './Drawer.vue'
import DashboardCoreAppBar from './AppBar.vue'
import DashboardCoreView from './View.vue'
import DashboardCoreFooter from './Footer.vue'
export default {
  name: 'DashboardLayout',
  components: {
    DashboardCoreDrawer,
    DashboardCoreAppBar,
    DashboardCoreView,
    DashboardCoreFooter
  },
  data: () => ({
    expandOnHover: false
  })
}
</script>
