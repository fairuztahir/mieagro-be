<template>
  <MaterialCard icon="mdi-clipboard-text" :title="title" class="px-5 py-3">
    <v-row>
      <v-col cols="12" class="ml-auto">
        <v-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="primary--text" width="15px" @click="sort('no')">No.</th>
                <template v-for="(h, i) in header" :key="i">
                  <th :class="headerRowStyle(i)">{{ capitalize(h.name) }}</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(d, index) in data" :key="index">
                <td class="font-weight-light">{{ incrementNum(index) }}</td>
                <template v-for="(h, i) in header" :key="i">
                  <td :class="bodyRowStyle(i)">{{ d[String(h.name).toLowerCase()] }}</td>
                </template>
              </tr>
            </tbody>
          </template>
        </v-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="ml-auto d-flex justify-end mt-2">
        <v-pagination v-model="page" :length="totalPage" :total-visible="totalVisible" rounded border :size="size"></v-pagination>
      </v-col>
    </v-row>
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, computed } from 'vue'
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
    // page: {
    //   type: Number,
    //   required: false,
    //   default: 2
    // },
    // totalPage: {
    //   type: Number,
    //   required: false,
    //   default: 5
    // }
  },
  setup(props) {
    const capitalize = (s: String) => (s && s[0].toUpperCase() + s.slice(1)) || ''

    const pagination = reactive({
      num: 1,
      page: 1,
      totalPage: 4,
      totalVisible: computed(() => {
        if (screen.width <= 540) {
          return 1
        }
        return 5
      }),
      size: 'x-small'
    })

    const sort = (header: String) => {
      console.log('test')
    }

    function incrementNum(i: string) {
      return pagination.page * pagination.num + Number(i)
    }

    function headerRowStyle(i: string) {
      if (Number(i) === props.header.length - 1) {
        return 'primary--text text-right'
      }
      return 'primary--text'
    }

    function bodyRowStyle(i: string) {
      if (Number(i) === props.header.length - 1) {
        return 'font-weight-light text-right'
      }
      return 'font-weight-light'
    }

    return {
      capitalize,
      ...toRefs(pagination),
      sort,
      incrementNum,
      headerRowStyle,
      bodyRowStyle
    }
  }
})
</script>
