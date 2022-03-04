<template>
  <v-app-bar absolute app color="transparent" flat height="75">
    <!-- <v-toolbar-title class="hidden-sm-and-down font-weight-light" text="test" /> -->
    <v-app-bar-title class="hidden-sm-and-down font-weight-light">{{ title }}</v-app-bar-title>

    <v-spacer />

    <div class="mx-3" />

    <v-btn class="mx-2" dark min-width="0" to="/">
      <v-icon icon="mdi-view-dashboard" color="primary"></v-icon>
    </v-btn>
    <v-btn class="mx-2" dark min-width="0" to="/">
      <v-icon icon="mdi-account" color="primary"></v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  props: {
    title: String
  }
})
</script>
