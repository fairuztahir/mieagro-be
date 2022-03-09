<template>
  <v-footer app bottom fixed>
    <v-container class="d-flex flex-column core-footer">
      <v-row align="center" no-gutters>
        <v-spacer class="hidden-sm-and-down" />

        <v-col cols="12" md="auto">
          <div class="body-1 font-weight-light pt-6 pt-md-0 text-center">&copy; 2022, <a href="#">MIE AGRO</a>.</div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  setup() {
    const links = [
      {
        href: '#',
        text: 'About Us'
      },
      {
        href: '#',
        text: 'Blog'
      },
      {
        href: '#',
        text: 'Licenses'
      }
    ]

    return {
      links
    }
  }
})
</script>
