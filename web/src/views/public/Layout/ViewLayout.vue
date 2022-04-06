<template>
  <v-main>
    <v-container fluid>
      <router-view v-slot="{ Component, route }">
        <transition :name="route.meta.transition || 'route'" mode="out-in">
          <div :key="route.name" v-if="validateComponent(Component)">
            <component :is="Component" :key="route.meta.usePathKey ? route.path : undefined"></component>
          </div>
        </transition>
      </router-view>
    </v-container>
    <v-spacer />
  </v-main>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  setup() {
    function validateComponent(value: any) {
      if (value != undefined) return true
      else return false
    }
    return {
      validateComponent
    }
  }
})
</script>
