<template>
  <MaterialCard icon="mdi-clipboard-text" :title="title" class="px-5 py-3">
    <v-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left" width="15px">No.</th>
            <template v-for="h in header" :key="h.name">
              <th class="text-left">{{ capitalize(h.name) }}</th>
            </template>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(d, index) in data" :key="index">
            <td class="font-weight-light">{{ num++ }}</td>
            <template v-for="h in header" :key="h">
              <td class="font-weight-light">{{ d[String(h.name).toLowerCase()] }}</td>
            </template>
          </tr>
        </tbody>
      </template>
    </v-table>
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
export default defineComponent({
  name: 'MaterialTable',
  components: {
    MaterialCard
  },
  props: {
    data: {
      type: Object,
      required: false,
      default: []
    },
    header: {
      type: Object,
      required: false,
      default: []
    },
    title: {
      type: String,
      required: false,
      default: 'Table Title'
    }
  },
  setup() {
    const capitalize = (s: String) => (s && s[0].toUpperCase() + s.slice(1)) || ''
    const num = 1

    return {
      capitalize,
      num
    }
  }
})
</script>
