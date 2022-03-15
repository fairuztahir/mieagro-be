// Styles
import 'vuetify/styles'
import '@/styles/overrides.sass'

// Vuetify
import { createVuetify, ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const lightColors = {
  background: '#EEE',
  primary: '#4CAF50',
  secondary: '#9C27b0',
  accent: '#9C27b0',
  info: '#00CAE3'
  // surface: '#EEE'
}

const darkColors = {
  background: '#525151',
  surface: '#363636',
  primary: '#6200EE',
  'primary-darken-1': '#3700B3',
  secondary: '#03DAC6',
  'secondary-darken-1': '#018786',
  error: '#B00020',
  info: '#2196F3',
  success: '#4CAF50',
  warning: '#FB8C00'
}

const lightTheme: ThemeDefinition = {
  dark: false,
  colors: lightColors
}

const darkTheme: ThemeDefinition = {
  dark: false,
  colors: darkColors
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      dark: darkTheme,
      light: lightTheme
    }
  }
})

export default vuetify
