<template>
  <v-app :theme="theme">
    <DashboardCoreDrawer :rail="rail" />
    <DashboardCoreAppBar :title="titleName" @rail="updateparent" />
    <DashboardCoreView />
    <DashboardCoreFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
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

  setup() {
    const titleName = 'Dashboard'
    const theme = ref('light')
    const toggleTheme = () => (theme.value = theme.value === 'light' ? 'dark' : 'light')
    let rail = ref(true)

    return {
      titleName,
      theme,
      toggleTheme,
      rail
    }
  },
  methods: {
    updateparent(event: boolean) {
      this.rail = event
    }
  }
})
</script>
