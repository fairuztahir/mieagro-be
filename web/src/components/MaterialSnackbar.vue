<template>
  <v-snackbar class="v-snackbar--material" :color="type">
    <slot />

    <v-btn color="white" size="18" @click="eventUpdate" class="ml-3">
      <v-icon :color="type">mdi-close</v-icon>
    </v-btn>
  </v-snackbar>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs, watch } from 'vue'
import MaterialAlert from '@/components/MaterialAlert.vue'
export default defineComponent({
  name: 'MaterialSnackbar',
  components: {
    MaterialAlert
  },
  props: {
    dismissible: {
      type: Boolean,
      default: true
    },
    type: {
      type: String,
      default: ''
    },
    value: Boolean
  },
  setup(props, context) {
    const data = reactive({
      internalValue: false,
      timeout: 3000
    })

    const eventUpdate = () => {
      data.internalValue = false
      context.emit('value', false)
    }

    return {
      ...toRefs(data),
      eventUpdate
    }
  }
})
</script>

<style lang="sass">
.v-snackbar--material
  margin-top: 32px
  margin-bottom: 32px

  .v-alert--material,
  .v-snack__wrapper
    border-radius: 0px

  .v-snack__content
    overflow: visible
    padding: 0
</style>
