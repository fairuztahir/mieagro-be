<template>
  <v-main>
    <v-container class="content" fluid>
      <router-view v-slot="{ Component, route }">
        <Transition name="route" mode="out-in">
          <div :key="route.name">
            <component :is="Component"></component>
          </div>
        </Transition>
      </router-view>
    </v-container>
    <v-spacer />
  </v-main>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({})
</script>

<style scoped>
.content {
  height: 85vh;
}

.route-enter-active,
.route-leave-active {
  transition: opacity 0.5s ease;
}

.route-enter-from,
.route-leave-to {
  opacity: 0;
}
</style>
