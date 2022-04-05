<template>
  <MaterialCard icon="mdi-clipboard-text" :title="title" class="px-5 py-3">
    <v-row>
      <v-col cols="12" class="ml-auto">
        <v-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="primary--text" width="15px" v-if="numbering" @click="sort('no')">No.</th>
                <template v-for="(h, i) in header" :key="i">
                  <th :class="tblRowStyle(i).header">{{ capitalize(h.label) }}</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(d, index) in data" :key="index" v-if="data.length > 0">
                <td class="font-weight-light" v-if="numbering">{{ incrementNum(index) }}</td>
                <template v-for="(h, i) in header" :key="i">
                  <td :class="tblRowStyle(i).body">{{ formatDate(d[String(h.key).toLowerCase()], h.type) }}</td>
                </template>
              </tr>

              <tr v-else>
                <td
                  v-if="numbering"
                  :colspan="header.length + 1"
                  class="font-weight-light text-center pa-4 no-record-style"
                >
                  <v-icon class="pr-4">mdi-card-bulleted-off-outline</v-icon> No Record Found.
                </td>
                <td v-else :colspan="header.length" class="font-weight-light text-center pa-4 no-record-style">
                  <v-icon class="pr-4">mdi-card-bulleted-off-outline</v-icon> No Record Found.
                </td>
              </tr>
            </tbody>
          </template>
        </v-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="d-flex mt-2" cols="12" md="2" sm="12">
        <v-select
          :items="displayNo"
          color="primary"
          density="compact"
          label="No of rows"
          variant="outlined"
          v-model="selectRows"
          @update:modelValue="RowUpdate"
        ></v-select>
      </v-col>
      <v-col cols="12" md="6" sm="12" class="ml-auto d-flex justify-end mt-2">
        <v-pagination
          v-model="page"
          :length="totalPage"
          :total-visible="totalVisible"
          :size="size"
          :color="color"
          rounded
          border
        ></v-pagination>
      </v-col>
    </v-row>
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, computed } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
import moment from 'moment'

export default defineComponent({
  name: 'MaterialTable',
  components: {
    MaterialCard
  },
  props: {
    data: {
      type: Object,
      required: true,
      default: () => []
    },
    header: {
      type: Object,
      required: true,
      default: () => []
    },
    title: {
      type: String,
      required: false,
      default: () => 'Table Title'
    },
    numbering: {
      type: Boolean,
      required: false,
      default: () => false
    },
    totalPage: {
      type: Number,
      required: true
    },
    pageSize: Function
  },
  setup(props, context) {
    const capitalize = (s: String) => (s && s[0].toUpperCase() + s.slice(1)) || ''

    const pagination = reactive({
      num: 1,
      page: 1,
      // totalPage: 4,
      totalVisible: computed(() => {
        if (screen.width <= 540) {
          return 1
        }
        return 5
      }),
      size: 'x-small',
      color: 'primary',
      displayNo: ['5', '10', '20', '40'],
      selectRows: String(10)
    })

    const sort = (header: String) => {
      console.log('test')
    }

    function incrementNum(i: string) {
      return pagination.page * pagination.num + Number(i)
    }

    function tblRowStyle(i: string) {
      if (Number(i) === props.header.length - 1) {
        return { header: 'primary--text text-right', body: 'font-weight-light text-right' }
      }
      return { header: 'primary--text', body: 'font-weight-light' }
    }

    function formatDate(value: string, type: string = '') {
      if (type == 'date') return moment(value).format('YYYY-MM-DD')
      else if (type == 'datetime') return moment(value).format('YYYY-MM-DD HH:mm:ss')
      else return value
    }

    return {
      capitalize,
      ...toRefs(pagination),
      sort,
      incrementNum,
      tblRowStyle,
      RowUpdate: (value: string) => {
        context.emit('pageSize', value)
      },
      formatDate
    }
  }
})
</script>

<style lang="sass" scoped>
.no-record-style
  color: #999
</style>
