<template>
  <v-app>
    <dashboard-core-view />
  </v-app>
</template>

<script>
import DashboardCoreView from './View.vue'
export default {
  name: 'DashboardLayout',
  components: {
    DashboardCoreView
  }
}
</script>
