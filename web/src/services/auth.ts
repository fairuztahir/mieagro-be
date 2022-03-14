import { computed, inject, reactive, toRefs, watch } from 'vue'
import { useApi, useApiWithAuth } from './api'

const AUTH_KEY = 'f_token'
export const AUTH_TOKEN = 'token'

interface Plan {
  id: number
  name: string
}

interface Subscription {
  id: string
  expiresAt: Date
  renewsAt: Date
  plan: Plan
}

interface User {
  name: string
  email: string
  [AUTH_TOKEN]: string
  // subscription?: Subscription
}

interface AuthState {
  authenticating: boolean
  user?: User
  error?: Error
}

const state = reactive<AuthState>({
  authenticating: false,
  user: undefined,
  error: undefined
})

// Read access token from local storage?
const token = window.localStorage.getItem(AUTH_KEY)

if (token) {
  const { loading, error, data, get } = useApi('/v1/login')
  state.authenticating = true

  get({}, { headers: { Authorization: `Bearer ${token}` } })

  watch([loading], () => {
    if (error.value) {
      window.localStorage.removeItem(AUTH_KEY)
    } else if (data.value) {
      state.user = data.value
    }

    state.authenticating = false
  })
}

export const useAuth = () => {
  const setUser = (payload: User, remember: boolean): void => {
    if (remember) {
      window.localStorage.setItem(AUTH_KEY, payload[AUTH_TOKEN])
    }

    state.user = payload
    state.error = undefined
  }

  const logout = (): Promise<void> => {
    window.localStorage.removeItem(AUTH_KEY)
    return Promise.resolve((state.user = undefined))
  }

  return {
    setUser,
    logout,
    ...toRefs(state)
  }
}
