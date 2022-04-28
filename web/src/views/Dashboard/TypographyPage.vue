<template>
  <material-headline heading="Typography" link="styles/text-and-typography" />
  <v-row align="center" justify="center">
    <v-col cols="12">
      <material-card icon="mdi-clipboard-text" color="primary" title="Material Dashboard Heading">
        <v-card-text>
          <v-container class="pa-0" fluid>
            <v-row v-for="(t, i) in typography" :key="i" align="center">
              <v-col cols="1" md="3">
                <span class="display-note" v-text="t[0]" />
              </v-col>

              <v-col cols="8">
                <component :is="t[2]" :class="i">
                  <template v-if="i !== 'blockquote'">
                    {{ t[1] }}
                  </template>

                  <p v-if="i === 'blockquote'">"{{ t[1] }}"</p>
                  <small v-if="i === 'blockquote'"> - Fairuz Tahir, Software Developer</small>

                  <template v-if="i === 'small'">
                    <br />
                    <small>Use 'small' tag for the headers</small>
                  </template>
                </component>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </material-card>
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
import MaterialHeadline from '@/components/MaterialHeadline.vue'
export default defineComponent({
  components: {
    MaterialHeadline,
    MaterialCard
  },
  setup() {
    const leader =
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    const leaderShort = leader.slice(0, 105) + '...'
    const material = 'Fortune Favors The Bold'
    const small = 'Header with small subtitle'
    const data = reactive({
      typography: {
        'display-4': ['Display 4', material, 'h1'],
        'display-3': ['Display 3', material, 'h2'],
        'display-2': ['Display 2', material, 'h3'],
        'display-1': ['Display 1', material, 'h4'],
        headline: ['Headline', material, 'h5'],
        'title text-uppercase': ['Title', material, 'h6'],
        '': ['Paragraph', leader, 'p'],
        blockquote: ['Quote', leader, 'blockquote'],
        'text--disabled': ['Muted Text', leaderShort, 'p'],
        'primary--text': ['Primary Text', leaderShort, 'p'],
        'info--text': ['Info Text', leaderShort, 'p'],
        'success--text': ['Success Text', leaderShort, 'p'],
        'warning--text': ['Warning Text', leaderShort, 'p'],
        'danger--text': ['Danger Text', leaderShort, 'p'],
        small: ['Small Tag', small, 'h2']
      }
    })

    return {
      ...toRefs(data)
    }
  }
})
</script>
<style lang="scss">
.display-note {
  bottom: 10px;
  color: #c0c1c2;
  display: block;
  font-weight: 400;
  font-size: 13px;
  line-height: 13px;
  left: 0;
  margin-left: 20px;
  width: 260px;
}
.v-dialog .v-overlay__content {
  max-height: inherit;
}
</style>
