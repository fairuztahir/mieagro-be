<template>
  <v-main>
    <v-container fill-height fluid>
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
