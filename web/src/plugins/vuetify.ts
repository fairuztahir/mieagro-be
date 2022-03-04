// Styles
// import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '@/styles/overrides.sass'

// Vuetify
import { createVuetify, ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const theme = {
  primary: '#4CAF50',
  secondary: '#9C27b0',
  accent: '#9C27b0',
  info: '#00CAE3'
  // background: '#EEE',
  // surface: '#EEE'
}

// colors: {
//   background: '#9E9E9E',
//   surface: '#FFFFFF',
//   primary: '#6200EE',
//   'primary-darken-1': '#3700B3',
//   secondary: '#03DAC6',
//   'secondary-darken-1': '#018786',
//   error: '#B00020',
//   info: '#2196F3',
//   success: '#4CAF50',
//   warning: '#FB8C00'
// }

const myCustomLightTheme: ThemeDefinition = {
  // dark: false,
  colors: theme
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      dark: myCustomLightTheme,
      light: myCustomLightTheme
    }
  }
})

export default vuetify
