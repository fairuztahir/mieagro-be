<template>
  <v-app-bar absolute app color="transparent" flat height="75">
    <!-- <v-btn class="ml-3" elevation="1" :icon="btnImg.icon" small @click="drawerUpdate" /> -->
    <!-- <v-avatar size="x-large" class="ml-3" elevation="1">
      <img src="@/assets/miefoods.png" alt="MieFoods" />
    </v-avatar> -->
    <v-toolbar-title class="hidden-sm-and-down font-weight-light" :text="title" />

    <v-spacer />

    <div class="mx-3" />
    <v-hover v-slot="{ isHovering, props }">
      <v-btn stacked class="changebg" dark min-width="0" to="/login" v-bind="props">
        <v-icon icon="mdi-lock-open-variant" v-if="isHovering"></v-icon>
        <v-icon icon="mdi-lock-outline" v-else></v-icon>
      </v-btn>
    </v-hover>

    <v-hover v-slot="{ isHovering, props }">
      <v-btn stacked class="changebg" dark min-width="0" to="/" v-bind="props">
        <v-badge color="error" content="0" inline>
          <v-icon icon="mdi-heart" v-if="isHovering"></v-icon>
          <v-icon icon="mdi-heart-outline" v-else></v-icon>
        </v-badge>
      </v-btn>
    </v-hover>

    <v-hover v-slot="{ isHovering, props }">
      <v-btn stacked class="changebg mr-2" dark min-width="0" to="/" v-bind="props">
        <v-badge color="error" content="10" inline>
          <v-icon icon="mdi-cart" v-if="isHovering"></v-icon>
          <v-icon icon="mdi-cart-outline" v-else></v-icon>
        </v-badge>
      </v-btn>
    </v-hover>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
export default defineComponent({
  setup(props, context) {
    const btnImg = reactive({ icon: 'mdi-dots-vertical', status: false })

    const title = 'MIEFOODS'
    const drawerUpdate = () => {
      if (!btnImg.status) btnImg.icon = 'mdi-view-quilt'
      else btnImg.icon = 'mdi-dots-vertical'

      btnImg.status = !btnImg.status
    }

    return {
      title,
      btnImg,
      drawerUpdate
    }
  }
})
</script>

<style lang="sass" scoped>
.changebg
  background-color: transparent !important
// img {
//   width: 170%;
//   height: 170%;
// }
</style>
