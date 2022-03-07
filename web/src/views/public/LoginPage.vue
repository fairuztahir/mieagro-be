<template>
  <v-row justify="center" class="no-scroll-page">
    <v-col cols="12" md="4"></v-col>
    <v-col cols="12" md="4">
      <material-card class="v-card-profile pt-3" :avatar="avatar">
        <v-card-text class="text-center">
          <h4 class="display-1 mb-1 grey--text">LOGIN PAGE</h4>

          <h4 class="display-2 font-weight-light mb-3 black--text">Welcome to MIE Agro System</h4>

          <v-form>
            <v-row>
              <v-col cols="12" md="12">
                <v-text-field
                  color="#000"
                  label="Email"
                  prepend-icon="mdi-email"
                  variant="underlined"
                  class="mt-2 font-weight-light grey--text"
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
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <v-btn color="primary" rounded class="mr-0 mt-3 font-weight-light"> Login </v-btn>
        </v-card-text>
      </material-card>
    </v-col>
    <v-col cols="12" md="4"></v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
export default defineComponent({
  components: {
    MaterialCard
  },
  setup() {
    const showpass = ref(false)
    const avatar = ref('/test_logo.png')

    return {
      showpass,
      avatar
    }
  }
})
</script>

<style scoped>
.no-scroll-page {
  height: 87vh;
  /* justify-content: center;
  align-items: center; */
}
</style>
