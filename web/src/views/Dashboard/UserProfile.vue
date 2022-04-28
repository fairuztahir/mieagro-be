<template>
  <div class="pa-4">
    <v-row class="center-vertical ma-auto">
      <template v-for="(info, i) in avatars" :key="i">
        <v-col cols="12" md="3" sm="6" v-if="info.variant !== ''">
          <v-hover v-slot="{ isHovering, props }">
            <material-card
              class="v-card-profile pt-3"
              :avatar="info.image"
              :elevation="isHovering ? 4 : 1"
              v-bind="props"
            >
              <v-card-text class="text-center">
                <h4 class="display-1 mb-1 grey--text reduced-height">{{ info.title }}</h4>
                <h4 class="display-2 font-weight-light mb-3 black--text">{{ info.content }}</h4>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                  dolore magna aliqua.
                </p>
                <v-row>
                  <v-col cols="12" sm="12" md="12" class="text-center">
                    <v-btn
                      color="primary"
                      variant="outlined"
                      class="font-weight-light"
                      type="submit"
                      v-if="info.variant === 'outlined'"
                    >
                      Profile
                    </v-btn>
                    <v-btn
                      color="primary"
                      variant="contained-text"
                      class="font-weight-light"
                      type="submit"
                      v-else-if="info.variant === 'contained-text'"
                    >
                      Profile
                    </v-btn>
                    <v-btn
                      color="primary"
                      variant="text"
                      class="font-weight-light"
                      type="submit"
                      v-else-if="info.variant === 'text'"
                    >
                      Profile
                    </v-btn>
                    <v-btn color="primary" class="font-weight-light" type="submit" v-else> Profile </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </material-card>
          </v-hover>
        </v-col>
      </template>
    </v-row>

    <v-row class="pt-4">
      <template v-for="(info, i) in avatars" :key="i">
        <v-col cols="12" sm="3" md="2" class="d-flex justify-space-around">
          <MaterialAvatarCircle
            size="small"
            :image="info.image"
            :title="info.title"
            :content="info.content"
            :textBtn="info.textBtn"
            :url="info.url"
            v-bind="i"
          ></MaterialAvatarCircle>
        </v-col>
      </template>
    </v-row>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import MaterialAvatarCircle from '@/components/MaterialAvatarCircle.vue'
import MaterialCard from '@/components/MaterialCard.vue'
export default defineComponent({
  name: 'UserProfile',
  components: {
    MaterialAvatarCircle,
    MaterialCard
  },
  setup() {
    const avatars = [
      {
        image: 'tom.jpg',
        title: 'Tom Cruise',
        content: 'UI/UX Developer',
        textBtn: 'Hire me',
        url: 'http://localhost/#/admin/users/profile',
        variant: 'contained'
      },
      {
        image: 'taylor.jpg',
        title: 'Taylor Swift',
        content: 'Backend Developer',
        textBtn: 'Hire me',
        url: 'http://localhost/#/admin/users/profile',
        variant: 'outlined'
      },
      {
        image: 'brad.jpg',
        title: 'Brad Pitt',
        content: 'UI/UX Developer',
        textBtn: 'Hire me',
        url: 'http://localhost/#/admin/users/profile',
        variant: ''
      },
      {
        image: 'han.jpg',
        title: 'Han Ye Seul',
        content: 'Manager',
        textBtn: 'Call me',
        url: 'http://localhost/#/admin/users/profile',
        variant: 'text'
      },
      {
        image: 'mo.jpg',
        title: 'Mo Salah',
        content: 'QA Tester',
        textBtn: 'Hire me',
        url: 'http://localhost/#/admin/users/profile',
        variant: ''
      },
      {
        image: 'siti.jpg',
        title: 'Siti Nara',
        content: 'Software Engineer',
        textBtn: 'Hire me',
        url: 'http://localhost/#/admin/users/profile',
        variant: 'contained-text'
      }
    ]

    function setVariants(value: string) {
      return value !== '' ? String(value) : 'text'
    }
    return {
      avatars,
      setVariants
    }
  }
})
</script>
<style lang="sass">
.reduced-height
  margin-top: -30px
</style>
