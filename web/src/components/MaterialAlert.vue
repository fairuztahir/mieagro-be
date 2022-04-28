<template>
  <v-alert class="v-alert--material" :color="color">
    <template v-if="icon" v-slot:prepend>
      <v-icon :aria-hidden="false" :color="color" class="v-alert__icon elevation-6">
        {{ icon }}
      </v-icon>
    </template>

    <slot />
  </v-alert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'MaterialAlert',
  props: {
    icon: String,
    color: String
  }
})
</script>

<style lang="sass">
.v-alert--material
  margin-top: 32px

  .v-alert__icon
    top: -36px
  .v-alert__close
    // background: #fff
    // border-color: #fff
    border-radius: 50%

  .v-alert__dismissible
    align-self: flex-start
    margin: 0 !important
    padding: 0 !important
</style>
