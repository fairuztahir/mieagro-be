<template>
  <button @click="show = !show">Home</button>
  <Transition>
    <p v-if="show">hello</p>
  </Transition>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  data() {
    return {
      show: true
    }
  }
})
</script>

<style scoped>
.no-scroll-page {
  height: 87vh;
  /* justify-content: center;
  align-items: center; */
}
</style>
