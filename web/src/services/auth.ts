import { reactive, toRefs, watch } from 'vue'
import { useApi } from './api'
import { useMainStore } from '@/stores'

const AUTH_KEY = 'f_token'
export const AUTH_TOKEN = 'token'

// interface Plan {
//   id: number
//   name: string
// }

// interface Subscription {
//   id: string
//   expiresAt: Date
//   renewsAt: Date
//   plan: Plan
// }

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

export const fetchKey = () => {
  return AUTH_KEY
}

if (token) {
  const { loading, error, data, get } = useApi('v1/auth/user', token)
  state.authenticating = true

  get().catch((error) => console.log(error))

  watch([loading], () => {
    if (error.value) {
      const main = useMainStore()
      main.removeToken()
      state.user = undefined
    } else if (data.value) {
      state.user = data.value.data
    }

    state.authenticating = false
  })
}

export const useAuth = () => {
  const main = useMainStore()
  const setUser = (payload: User, remember: boolean): void => {
    if (remember) main.addToken(payload[AUTH_TOKEN])
    state.user = payload
    state.error = undefined
  }

  const logout = (): Promise<void> => {
    main.removeToken()
    return Promise.resolve((state.user = undefined))
  }

  return {
    setUser,
    logout,
    ...toRefs(state)
  }
}
