<template>
  <v-footer app bottom>
    <v-container class="d-flex flex-column core-footer">
      <v-row align="center" no-gutters>
        <v-col v-for="(link, i) in links" :key="i" class="text-center mb-sm-0 mb-5 hidden-sm-and-down" cols="auto">
          <a
            :href="link.href"
            class="mr-0 grey--text text--darken-3"
            rel="noopener"
            target="_blank"
            v-text="link.text"
          />
        </v-col>

        <v-spacer class="hidden-sm-and-down" />

        <v-col cols="12" md="auto">
          <div class="body-1 font-weight-light pt-6 pt-md-0 text-center">&copy; 2022, <a href="#">MIE AGRO</a></div>
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

<style lang="sass" scoped>
.core-footer
  a
    font-size: .825rem
    font-weight: 500
    text-decoration: none
    text-transform: uppercase

.v-footer
  border-top: 1px solid #e7e7e7 !important
  background-color: #f5f5f5 !important

.v-container
  padding-left: 16px
  padding-right: 16px
  padding-top: 10px !important
  padding-bottom: 10px !important
</style>
