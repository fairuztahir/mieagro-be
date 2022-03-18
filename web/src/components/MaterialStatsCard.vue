<template>
  <MaterialCard :icon="icon" :color="color" class="v-card--material-stats">
    <template v-slot:after-heading>
      <v-spacer class="hidden-sm-and-down" />

      <div class="text-right">
        <v-list-item two-line>
          <v-list-item-header>
            <v-list-item-title class="grey--text font-weight-light">{{ title }}</v-list-item-title>
            <v-list-item-subtitle class="display-2 font-weight-light text--primary"
              >{{ value }} <small>{{ smallValue }}</small></v-list-item-subtitle
            >
          </v-list-item-header>
        </v-list-item>
      </div>
    </template>

    <v-col cols="12" class="px-0">
      <v-divider />
    </v-col>

    <v-icon :color="subIconColor" size="16" class="ml-2 mr-1">
      {{ subIcon }}
    </v-icon>

    <span :class="subTextColor" class="caption grey--text font-weight-light" v-text="subText" />
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MaterialCard from './MaterialCard.vue'
export default defineComponent({
  name: 'MaterialStatsCard',
  inheritAttrs: false,
  components: {
    MaterialCard
  },

  props: {
    color: {
      type: String,
      required: false
    },
    icon: {
      type: String,
      required: true
    },
    subIcon: {
      type: String,
      default: undefined
    },
    subIconColor: {
      type: String,
      default: undefined
    },
    subTextColor: {
      type: String,
      default: undefined
    },
    subText: {
      type: String,
      default: undefined
    },
    title: {
      type: String,
      default: undefined
    },
    value: {
      type: String,
      default: undefined
    },
    smallValue: {
      type: String,
      default: undefined
    }
  }
})
</script>

<style lang="sass">
.v-card--material-stats
  display: flex
  flex-wrap: wrap
  position: relative

  >div:first-child
    -webkit-box-pack: justify
    -ms-flex-pack: justify
    justify-content: space-between

  .v-card
    border-radius: 4px
    flex: 0 1 auto

  .v-card__text
    display: inline-block
    flex: 1 0 calc(100% - 120px)
    position: absolute
    top: 0
    right: 0
    width: 100%

  .v-card__actions
    flex: 1 0 100%

  .v-sheet
    border-radius: 4px
</style>
