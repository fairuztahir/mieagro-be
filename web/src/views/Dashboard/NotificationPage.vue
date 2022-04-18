<template>
  <material-headline heading="Alerts" link="components/alerts" />
  <v-row>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-text>
          <sub-heading subheading="Notification Style" />

          <material-alert color="info"> This is a plain notification. </material-alert>
          <material-alert color="info" closable> This is a notification with close button. </material-alert>
          <material-alert color="success" closable icon="mdi-bell">
            This is a notification with close button and icon and have many lines. You can see that the icon and the
            close button are always vertically aligned. This is a beautiful notification. So you don't have to worry
            about the style.
          </material-alert>
          <material-alert color="warning" closable icon="mdi-bell">
            You can see that the icon and the close button are always vertically aligned. This is a beautiful
            notification. So you don't have to worry about the style.
          </material-alert>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-text>
          <sub-heading subheading="Notification states" />

          <material-alert v-for="color in colors" :key="color" :color="color" closable>
            <span class="text-uppercase" v-text="color" /> — This is a regular alert made with the color of "{{
              color
            }}"
          </material-alert>

          <material-alert color="secondary" closable>
            <span>PRIMARY</span> — This is a regular alert made with the color "secondary"
          </material-alert>

          <material-alert color="pink darken-1" closable>
            <span>PINK DARKEN-1</span> — This is a regular alert made with the color "pink darken-1"
          </material-alert>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12">
      <v-card>
        <v-card-text class="text-center">
          <sub-heading class="text-center" subheading="Snackbar Locations" />

          <v-row class="mt-n12" justify="center">
            <v-col cols="10" lg="8">
              <v-row>
                <v-col v-for="dir in directions" :key="dir" cols="4">
                  <v-btn color="secondary" default class="v-btn--block font-weight-light" @click="randomColor(dir)">
                    {{ dir }}
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <v-spacer class="mt-2" />
          <sub-heading class="text-center" subheading="Dialogs" />

          <v-row class="mt-n12" justify="center">
            <v-col cols="10" lg="8">
              <v-row>
                <v-col cols="4">
                  <v-btn color="secondary" default rounded @click="dialog = true" class="font-weight-light">
                    Classic Dialog
                  </v-btn>
                </v-col>
                <v-col cols="4">
                  <v-btn color="info" default rounded @click="dialog2 = true" class="font-weight-light white">
                    Notice Modal
                  </v-btn>
                </v-col>
                <v-col cols="4">
                  <v-btn color="pink darken-1" default rounded @click="dialog3 = true" class="font-weight-light white">
                    Small Alert Modal
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <material-snackbar
    v-model="snackbar"
    :type="color"
    v-bind="{
      [posY]: true,
      [posX]: true
    }"
    @value="updateSnackBar"
  >
    <span class="font-weight-bold">&nbsp;OHAYO&nbsp;</span> — a notification msg for your template.
  </material-snackbar>

  <v-row>
    <v-dialog v-model="dialog">
      <v-card class="text-center">
        <v-card-title>
          Dialog Title

          <v-spacer />

          <v-icon aria-label="Close" @click="dialog = false"> mdi-close </v-icon>
        </v-card-title>

        <v-card-text>
          Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind
          texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A
          small river named Duden flows by their place and supplies it with the necessary regelialia. It is a
          paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing
          has no control about the blind texts it is an almost unorthographic life One day however a small line of blind
          text by the name of Lorem Ipsum decided to leave for the far World of Grammar.
        </v-card-text>

        <v-card-actions>
          <v-spacer />

          <v-btn color="error" text @click="dialog = false"> Close </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>

  <v-dialog v-model="dialog2">
    <v-card>
      <v-card-title>
        How do you become an affiliate?

        <v-spacer />

        <v-icon aria-label="Close" @click="dialog2 = false"> mdi-close </v-icon>
      </v-card-title>

      <v-card-text class="body-1 text-center">
        <v-row>
          <v-col cols="12" md="8">
            <div>
              <div>
                <strong>1. Register</strong>
              </div>

              <div class="grey--text">
                The first step is to create an account at Company Name. You can choose a social network or go for the
                classic version, whatever works best for you.
              </div>
            </div>
          </v-col>

          <v-col class="hidden-sm-and-down" md="4">
            <v-sheet>
              <v-img src="" height="100" width="200" />
            </v-sheet>
          </v-col>

          <v-col cols="12" md="8">
            <div>
              <div>
                <strong>2. Apply</strong>
              </div>

              <div class="grey--text">
                The first step is to create an account at <a href="">company name</a>. You can choose a social network
                or go for the classic version, whatever works best for you.
              </div>
            </div>
          </v-col>

          <v-col class="hidden-sm-and-down" md="4">
            <v-sheet>
              <v-img src="" height="100" width="200" />
            </v-sheet>
          </v-col>

          <v-col cols="12">
            If you have more questions, don't hesitate to contact us or send us a tweet @companyname. We're here to
            help!
          </v-col>
        </v-row>

        <v-btn class="mt-6" color="info" depressed default rounded @click="dialog2 = false"> Sounds good </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-dialog v-model="dialog3">
    <v-card>
      <v-card-title>
        Are you sure?

        <v-spacer />

        <v-icon aria-label="Close" @click="dialog3 = false"> mdi-close </v-icon>
      </v-card-title>

      <v-card-text class="pb-6 pt-12 text-center">
        <v-btn class="mr-3" text @click="dialog3 = false"> Nevermind </v-btn>

        <v-btn color="success" text @click="dialog3 = false"> Yes </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs, watch } from 'vue'
import MaterialHeadline from '@/components/MaterialHeadline.vue'
import SubHeading from '@/components/Subheading.vue'
import MaterialAlert from '@/components/MaterialAlert.vue'
import MaterialSnackbar from '@/components/MaterialSnackbar.vue'
export default defineComponent({
  components: {
    MaterialHeadline,
    SubHeading,
    MaterialAlert,
    MaterialSnackbar
  },
  setup() {
    const colors = ['info', 'success', 'warning', 'error']

    const data = reactive({
      color: 'info',
      dialog: false,
      dialog2: false,
      dialog3: false,
      direction: 'top center',
      directions: ['top left', 'top center', 'top right', 'bottom left', 'bottom center', 'bottom right'],
      snackbar: false,
      posX: 'center',
      posY: 'top'
    })

    function randomColor(dir: any) {
      data.color = colors[Math.floor(Math.random() * colors.length)]
      data.direction = dir
      data.snackbar = true
    }

    watch(
      () => data.direction,
      (currentValue, oldValue) => {
        if (currentValue !== oldValue) {
          const position = data.direction.split(' ')
          data.posY = position[0]
          data.posX = position[1]
        }
      }
    )

    function updateSnackBar(event: boolean) {
      data.snackbar = event
    }

    return {
      colors,
      ...toRefs(data),
      randomColor,
      updateSnackBar
    }
  }
})
</script>
<style lang="sass" scoped>
.white
  color: #fff !important
.center-vertical
  justify-content: center
  align-items: center
.v-overlay
  justify-content: center
  align-items: center
</style>
