<template>
  <v-footer app bottom fixed class="d-flex flex-column">
    <div class="text-black text-body-1 font-weight-light pt-6 pt-md-0 text-right">
      &copy; {{ new Date().getFullYear() }} — <a to="/">Mie Agro</a>
    </div>
  </v-footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({})
</script>

