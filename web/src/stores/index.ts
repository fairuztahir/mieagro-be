import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { fetchKey } from '@/services/auth'

export const useMainStore = defineStore('main', {
  state: () => {
    return {
      token: useStorage(fetchKey(), '')
    }
  },
  getters: {
    getToken(state) {
      return state.token
    },
    emptyToken(state) {
      return state.token.length <= 0
    }
  },
  actions: {
    async addToken(value: string) {
      this.token = value
    },
    async removeToken(value = '') {
      this.token = value
    }
  }
})
