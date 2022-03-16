<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent app mobile-break-point="960">
    <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" :title="user?.name"> </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <div v-for="(item, i) in items" :key="i" :value="item" active-color="primary">
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
import { useAuth } from '@/services/auth'

export default defineComponent({
  props: {
    rail: Boolean,
    title: Function
  },
  setup(props, context) {
    const { user } = useAuth()
    const data = reactive({
      drawer: true,
      items: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', page: '/admin/dashboard' },
        { title: 'My Account', icon: 'mdi-account', page: '/login' },
        { title: 'Settings', icon: 'mdi-cog-outline', page: '/admin/settings' }
      ]
    })

    return {
      user,
      ...toRefs(data),
      titleUpdate: (value: string) => context.emit('title', value)
    }
  }
})
</script>
