<template>
  <v-app-bar absolute app color="transparent" flat height="75">
    <v-btn class="ml-3" elevation="1" :icon="btnImg.icon" small @click="customChange" />

    <!-- <v-app-bar-title class="hidden-sm-and-down font-weight-light">{{ title }}</v-app-bar-title> -->
    <v-toolbar-title class="hidden-sm-and-down font-weight-light" :text="title" />

    <v-spacer />

    <div class="mx-3" />

    <v-btn class="mx-2" dark min-width="0" to="/">
      <v-icon icon="mdi-view-dashboard"></v-icon>
    </v-btn>
    <v-btn class="mx-2" dark min-width="0" to="/">
      <v-icon icon="mdi-account"></v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
export default defineComponent({
  props: {
    title: String,
    rail: Function
  },
  setup() {
    const btnImg = reactive({ icon: 'mdi-dots-vertical', status: false })

    return {
      btnImg
    }
  },
  methods: {
    customChange() {
      if (!this.btnImg.status) this.btnImg.icon = 'mdi-view-quilt'
      else this.btnImg.icon = 'mdi-dots-vertical'

      this.btnImg.status = !this.btnImg.status
      this.$emit('rail', !this.btnImg.status)
    }
  }
})
</script>
