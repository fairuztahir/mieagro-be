<template>
  <div class="loading"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'

export default defineComponent({
  setup() {
    const { logout } = useAuth()
    const router = useRouter()
    logout().then(() => router.push({ name: 'Home' }))
  }
})
</script>
