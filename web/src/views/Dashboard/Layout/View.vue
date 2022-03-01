<template>
  <v-main>
    <v-container fluid>
      <router-view></router-view>
    </v-container>
  </v-main>
  <v-spacer />
  <dashboard-core-footer />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DashboardCoreFooter from './Footer.vue'
export default defineComponent({
  components: {
    DashboardCoreFooter
  },
})
</script>
