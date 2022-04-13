<template>
  <div class="display-2 font-weight-light col col-12 text-left text--primary pa-0 mb-8">
    <h5 class="font-weight-light">
      {{ subheading }}
      <template v-if="text">
        <span class="subtitle-1" v-text="text" />
      </template>
    </h5>

    <div class="pt-2">
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'Subheading',

  props: {
    subheading: {
      type: String,
      default: ''
    },
    text: {
      type: String,
      default: ''
    }
  }
})
</script>
