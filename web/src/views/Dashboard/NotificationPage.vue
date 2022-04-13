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
  </v-row>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import MaterialHeadline from '@/components/MaterialHeadline.vue'
import SubHeading from '@/components/Subheading.vue'
import MaterialAlert from '@/components/MaterialAlert.vue'
export default defineComponent({
  components: {
    MaterialHeadline,
    SubHeading,
    MaterialAlert
  }
})
</script>
