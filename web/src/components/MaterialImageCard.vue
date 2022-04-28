<template>
  <v-hover v-slot="{ isHovering, props }">
    <MaterialCard class="v-card--material-chart" :elevation="isHovering ? 4 : 1" v-bind="props" color="transparent">
      <template v-slot:image>
        <v-img
          :src="image"
          :class="isHovering ? 'img-lift lift-up-bg elevation-6' : 'img-lift elevation-6'"
          v-bind="props"
          cover
        ></v-img>
      </template>

      <slot name="reveal-actions" />

      <slot />

      <slot name="actions" />
    </MaterialCard>
  </v-hover>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
export default defineComponent({
  name: 'MaterialImageCard',
  inheritAttrs: false,
  components: {
    MaterialCard
  },
  props: {
    image: {
      type: String,
      default: () => 'prod1.jpg'
    }
  }
})
</script>

<style lang="sass">
.v-card--material-chart
  p
    color: #999
    font-size: 0.8em

  .v-card--material__heading
    max-height: 185px

    .ct-label
      color: inherit
      opacity: .7
      font-size: 0.975rem
      font-weight: 100

    .ct-grid
      stroke: rgba(255, 255, 255, 0.2)

    .ct-series-a .ct-point,
    .ct-series-a .ct-line,
    .ct-series-a .ct-bar,
    .ct-series-a .ct-slice-donut
        stroke: rgba(255,255,255,.8)

    .ct-series-a .ct-slice-pie,
    .ct-series-a .ct-area
        fill: rgba(255,255,255,.4)
.img-lift
  position: relative
  top: 0
  transition: top ease 0.3s
  border-radius: 3%
.lift-up-bg
  top: -30px
  bottom: -30px
</style>
