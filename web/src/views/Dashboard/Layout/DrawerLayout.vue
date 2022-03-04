<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent app >
    <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" title="John Leider">
    </v-list-item>

    <v-divider></v-divider>

    <!-- <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-home-city" title="Home" value="home"></v-list-item>
      <v-list-item prepend-icon="mdi-account" title="My Account" value="account"></v-list-item>
      <v-list-item prepend-icon="mdi-account-group-outline" title="Users" value="users"></v-list-item>
    </v-list> -->
    <v-list density="compact" nav>
      <div v-for="(item, i) in items" :key="i">
        <v-list-item :prepend-icon="item.icon" :title="item.title" :value="item.title" :to="item.page"></v-list-item>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
export default defineComponent({
  props: {
    rail: Boolean
  },
  setup() {
    const drawer = ref(true)
    const items =  ref([
        { title: 'Dashboard', icon: 'mdi-home-city', page: '/dashboard' },
        { title: 'My Account', icon: 'mdi-account', page: '/test' },
        { title: 'Users', icon: 'mdi-account-group-outline', page: '/test2' }
    ])
    return {
      drawer,
      items
    }
  },
})
</script>
