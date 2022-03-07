<template>
  <v-row justify="center" class="no-scroll-page">
    <v-col cols="12" md="4"></v-col>
    <v-col cols="12" md="4">
      <material-card
        class="v-card-profile pt-3"
        avatar="https://demos.creative-tim.com/vue-material-dashboard/img/marc.aba54d65.jpg"
      >
        <v-card-text class="text-center">
          <h5 class="display-1 mb-1 grey--text">Login Page</h5>

          <h4 class="display-2 font-weight-light mb-3 black--text">Welcome to MIE Agro System</h4>

          <!-- <p class="font-weight-light grey--text">
            Don't be scared of the truth because we need to restart the human foundation in truth And I love you like
            Kanye loves Kanye I love Rick Owens’ bed design but the back is...
          </p> -->
          <v-form>
            <v-row>
              <v-col cols="12" md="11">
                <v-text-field
                  color="#000"
                  label="Email"
                  prepend-icon="mdi-email"
                  variant="underlined"
                  class="font-weight-light grey--text"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="11">
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
          <v-btn color="primary" rounded class="mr-0"> Login </v-btn>
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

    return {
      showpass
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
