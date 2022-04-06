<template>
  <v-app-bar absolute app color="transparent" flat height="75">
    <v-btn class="hidden-sm-and-down v-nanake" elevation="1" :icon="btnImg.icon" small @click="drawerUpdate" />

    <v-toolbar-title class="hidden-sm-and-down font-weight-light ml-4" :text="title" />

    <v-spacer />

    <div class="mx-3" />

    <v-btn class="mx-2 changebg" dark min-width="0" to="/admin/dashboard">
      <v-icon icon="mdi-view-dashboard"></v-icon>
    </v-btn>
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn class="mx-2 changebg" dark min-width="0" v-bind="props">
          <v-icon icon="mdi-account"></v-icon>
        </v-btn>
      </template>
      <v-list class="drop-menu-user">
        <v-list-item v-for="(item, i) in items" :key="i" link :to="item.page">
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
export default defineComponent({
  props: {
    title: String,
    rail: Function
  },
  setup(props, context) {
    const btnImg = reactive({ icon: 'mdi-view-quilt', status: true })

    const drawerUpdate = () => {
      if (btnImg.status) {
        btnImg.icon = 'mdi-dots-vertical'
        btnImg.status = false
      } else {
        btnImg.icon = 'mdi-view-quilt'
        btnImg.status = true
      }

      context.emit('rail', btnImg.status)
    }

    const items = ref([
      { title: 'My Profile', page: '/' },
      { title: 'Logout', page: '/admin/logout' }
    ])

    return {
      btnImg,
      items,
      drawerUpdate
    }
  }
})
</script>

<style lang="sass" scoped>
.changebg
  background-color: transparent

.drop-menu-user
  right: 45px
.v-theme--light.v-nanake
  background: #fff
.v-theme--dark.v-nanake
  background: rgb(104 89 69)
</style>
