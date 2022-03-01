<template>
  <v-main>
    <router-view />

    <dashboard-core-footer />
  </v-main>
</template>

<script>
import DashboardCoreFooter from './Footer.vue'
export default {
  name: 'DashboardCoreView',
  components: {
    DashboardCoreFooter
  }
}
</script>
