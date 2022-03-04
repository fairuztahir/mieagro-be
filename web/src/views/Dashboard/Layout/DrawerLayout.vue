<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent app>
    <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" title="John Leider"> </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <div v-for="(item, i) in items" :key="i">
        <v-list-item
          :prepend-icon="item.icon"
          :title="item.title"
          :value="item.title"
          @click="titleUpdate(item.title)"
          :to="item.page"
        ></v-list-item>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
export default defineComponent({
  props: {
    rail: Boolean,
    title: Function
  },
  setup(props, context) {
    const data = reactive({
      drawer: true,
      items: [
        { title: 'Dashboard', icon: 'mdi-home-city', page: '/dashboard' },
        { title: 'My Account', icon: 'mdi-account', page: '/' },
        { title: 'Users', icon: 'mdi-account-group-outline', page: '/' }
      ]
    })

    return {
      ...toRefs(data),
      titleUpdate: (value: string) => context.emit('title', value)
    }
  }
})
</script>
