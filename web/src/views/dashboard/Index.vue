<template>
  <v-app>
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import HelloWorld from '@/components/HelloWorld.vue'
export default {
  name: 'DashboardIndex',

  components: {
    HelloWorld
  },

  data: () => ({
    expandOnHover: false
  })
}
</script>
