<template>
  <div class="page-container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'DashboardLayout'
}
</script>

<style lang="scss" scoped>
.md-app {
  height: 100vh;
  border: 1px solid rgba(#000, 0.12);
}

// Demo purposes only
.md-drawer {
  width: 230px;
  max-width: calc(100vw - 125px);
}
</style>
