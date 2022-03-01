<template>
  <v-app-bar id="app-bar" absolute app color="transparent" flat height="75">
    <v-toolbar-title class="hidden-sm-and-down font-weight-light" text="test" />

    <v-spacer />

    <div class="mx-3" />

    <v-btn class="ml-2" min-width="0" text to="/">
      <v-icon>mdi-view-dashboard</v-icon>
    </v-btn>

    <v-btn class="ml-2" min-width="0" text to="/">
      <v-icon>mdi-account</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({})
</script>
