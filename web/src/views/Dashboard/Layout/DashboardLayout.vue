<template>
  <v-app :theme="theme">
    <DashboardCoreDrawer :rail="rail" @title="updateAppBar" />
    <DashboardCoreAppBar :title="titleName" @rail="updateDrawer" />
    <DashboardCoreView />
    <DashboardCoreFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
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
    const data = reactive({
      titleName: 'Dashboard',
      theme: 'light',
      rail: true
    })

    return {
      ...toRefs(data),
      toggleTheme: () => (data.theme = data.theme === 'light' ? 'dark' : 'light')
    }
  },
  methods: {
    updateDrawer(event: boolean) {
      this.rail = event
    },
    updateAppBar(event: string) {
      this.titleName = event
    }
  }
})
</script>
