<template>
  <v-row class="center-vertical ma-auto">
    <v-col cols="12" md="4" sm="6" xs="5">
      <material-card class="v-card-profile pt-3" :avatar="avatar">
        <v-card-text class="text-center">
          <h4 class="display-1 mb-1 grey--text">LOGIN PAGE</h4>

          <h4 class="display-2 font-weight-light mb-3 black--text">Welcome to MIE Agro System</h4>

          <v-form @submit.prevent="submit">
            <v-row>
              <v-col cols="12" md="12">
                <v-text-field
                  color="#000"
                  label="Email"
                  prepend-icon="mdi-email"
                  variant="underlined"
                  class="mt-2 font-weight-light grey--text"
                  v-model="email"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="12">
                <v-text-field
                  color="#000"
                  label="Password"
                  prepend-icon="mdi-lock"
                  :append-icon="showpass ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showpass ? 'text' : 'password'"
                  variant="underlined"
                  class="font-weight-light grey--text"
                  @click:append="showpass = !showpass"
                  v-model="challenge"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <v-btn color="primary" class="mr-0 mt-3 font-weight-light" type="submit" :disabled="loading" @click="submit">
            LogIn
          </v-btn>
        </v-card-text>
      </material-card>
    </v-col>
  </v-row>
  <v-snackbar v-model="snackbar" multi-line :timeout="timeout">
    <div class="font-weight-light center-vertical">{{ String(text).toLowerCase() }}</div>

    <template v-slot:actions>
      <v-btn color="pink" icon="mdi-alpha-x-circle-outline" variant="text" @click="snackbar = false"> </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, toRefs } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
import { useApi } from '@/services/api'
import { useAuth } from '@/services/auth'
import { useRouter } from 'vue-router'

interface LoginPayload {
  email: string
  challenge: string
  rememberMe: boolean
}

export default defineComponent({
  name: 'LoginPage',
  components: {
    MaterialCard
  },
  setup() {
    const showpass = ref(false)
    const avatar = ref('/test_logo.png')
    const { loading, data, post, errorMessage } = useApi('v1/login')

    const { setUser } = useAuth()
    const router = useRouter()

    const payload = reactive<LoginPayload>({
      email: '',
      challenge: '',
      rememberMe: true
    })

    const snack = reactive({
      text: '',
      snackbar: false,
      timeout: 2500
    })

    // https://dev.to/adamcowley/how-to-build-an-authentication-into-a-vue3-application-200b
    // https://github.com/adam-cowley/twitch-project/blob/master/ui/src/views/Login.vue

    // https://www.bezkoder.com/vue-3-authentication-jwt/
    // https://github.com/bezkoder/vue-3-authentication-jwt/tree/master/src/services

    const submit = () => {
      post(payload)
        .then(() => {
          if (data.value && data.value.status == 200) {
            setUser(data.value.data, payload.rememberMe)
            router.push({ name: 'Dashboard' })
          } else {
            // MARK: prompt error message
            snack.text = data.value.message
            snack.snackbar = true
          }
        })
        .catch((error) => {
          console.log('ERR:', error.message)
          snack.text = error.message
          snack.snackbar = true
        })
    }

    return {
      showpass,
      avatar,
      loading,
      submit,
      errorMessage,
      ...toRefs(payload),
      ...toRefs(snack)
    }
  }
})
</script>

<style lang="sass" scoped>
.center-vertical
  justify-content: center
  align-items: center

.v-card-text
  opacity: inherit !important
</style>
