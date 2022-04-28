<template>
  <section class="mb-12 text-center">
    <h1 class="font-weight-light mb-2 headline" v-text="`Vuetify ${heading}`" />

    <span class="font-weight-light subtitle-1">
      Please checkout the
      <a
        :href="`https://next.vuetifyjs.com/en/${link}`"
        rel="noopener"
        target="_blank"
        class="secondary--text"
        style="text-decoration: none"
      >
        full documentation
      </a>
    </span>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'MaterialHeadline',
  props: {
    heading: {
      type: String,
      default: ''
    },
    link: {
      type: String,
      default: ''
    }
  }
})
</script>
