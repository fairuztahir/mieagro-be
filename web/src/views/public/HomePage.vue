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
/* .content {
    height: 100vh;
}
.v-application {
    background-color: rgb(215, 252, 207);
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
} */
</style>
