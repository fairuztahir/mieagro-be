<template>
  <v-app id="dashboard" :theme="theme" class="app-container">
    <DashboardCoreDrawer :rail="rail" @title="updateAppBar" />
    <DashboardCoreAppBar :title="titleName" @rail="updateDrawer" />
    <DashboardCoreView />
    <DashboardCoreFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, ref } from 'vue'
import DashboardCoreDrawer from './DrawerLayout.vue'
import DashboardCoreAppBar from './AppBar.vue'
import DashboardCoreView from './ViewLayout.vue'
import DashboardCoreFooter from './FooterLayout.vue'
export default defineComponent({
  name: 'DashboardLayout',
  components: {
    DashboardCoreDrawer,
    DashboardCoreAppBar,
    DashboardCoreView,
    DashboardCoreFooter
  },
  setup() {
    const data = reactive({
      titleName: 'Dashboard',
      rail: true
    })

    const theme = ref('light')

    return {
      ...toRefs(data),
      theme,
      toggleTheme: () => (theme.value = theme.value === 'light' ? 'dark' : 'light')
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

<style lang="sass">
.app-container
  min-height: 100vh
  max-width: 100%
  position: relative
  flex-direction: column
  -webkit-box-flex: 1
  -webkit-box-direction: normal
  display: flex
</style>
