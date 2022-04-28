<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent expand-on-hover app mobile-break-point="960">
    <v-list>
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
        :title="user?.name"
        subtitle="test@gmail.com"
      >
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav v-model:opened="open">
      <div v-for="(item, i) in items" :key="i" active-color="primary">
        <template v-if="!(Object.keys(item.child).length > 0)">
          <v-list-item
            :prepend-icon="item.icon"
            :title="item.title"
            :value="item.title"
            @click="titleUpdate(item.title)"
            :to="item.page"
          ></v-list-item>
        </template>
        <template v-else>
          <v-list-group>
            <template v-slot:activator="{ props }">
              <v-list-item
                v-bind="props"
                :prepend-icon="item.icon"
                :title="item.title"
                :value="item.title"
              ></v-list-item>
            </template>
            <div class="groupcolor">
              <v-list-item
                v-for="(child, i) in item.child"
                :key="i"
                :value="child.title"
                :title="child.title"
                :prepend-icon="child.icon"
                @click="titleUpdate(item.title)"
                :to="child.page"
                class="v-list-group--items"
              ></v-list-item>
            </div>
          </v-list-group>
        </template>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, watch } from 'vue'
import { useAuth } from '@/services/auth'

export default defineComponent({
  props: {
    rail: Boolean,
    title: Function
  },
  setup(props, context) {
    const { user } = useAuth()
    const userChild = [
      { title: 'User Profile', icon: 'mdi-face-man-shimmer', page: '/admin/users/profile' },
      { title: 'Test', icon: 'mdi-view-dashboard', page: '/admin/dashboard' }
    ]
    const data = reactive({
      drawer: true,
      items: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', page: '/admin/dashboard', child: [] },
        { title: 'Tables', icon: 'mdi-clipboard-text', page: '/admin/table', child: [] },
        { title: 'Notifications', icon: 'mdi-bell', page: '/admin/notifications', child: [] },
        { title: 'Typography', icon: 'mdi-format-font', page: '/admin/typography', child: [] },
        { title: 'Icons', icon: 'mdi-chart-bubble', page: '/admin/icons', child: [] },
        { title: 'Settings', icon: 'mdi-cog-outline', page: '/admin/settings', child: [] },
        { title: 'Users', icon: 'mdi-account-circle', page: '', child: userChild }
      ],
      open: []
    })

    watch(
      () => props.rail,
      (rail, prevRail) => {
        console.log('test', rail, prevRail)
      }
    )

    return {
      user,
      ...toRefs(data),
      titleUpdate: (value: string) => context.emit('title', value)
    }
  }
})
</script>

<style lang="sass" scoped>
.v-list-group
  overflow-x: hidden
  overflow-y: hidden

.v-list-group--prepend
  --parent-padding: 0px

.v-list-group--items
  --indent-padding: 0px

.v-theme--light .groupcolor
  background: #ebfff3
  // background: #ebfaff
.v-theme--dark .groupcolor
  background: #6354406e
  // background: #22342d
</style>
