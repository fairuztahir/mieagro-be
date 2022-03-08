<template>
  <v-main>
    <v-container fluid class="fill-height">
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

<style lang="sass" scoped>
.route-enter-active,
.route-leave-active
  transition: opacity 0.3s ease

.route-enter-from,
.route-leave-to
  opacity: 0

// .route-enter-from
//   opacity: 0
//   transform: translateX(100px)

// .route-enter-active
//   transition: all 0.3s ease-out

// .route-leave-to
//   opacity: 0
//   transform: translateX(-100px)

// .route-leave-active
//   transform: all 0.3s ease-in
</style>
