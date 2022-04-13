<template>
  <MaterialCard
    :icon="icon ? icon : 'mdi-clipboard-text'"
    :color="color ? color : 'primary'"
    :title="title"
    class="px-5 py-3"
  >
    <v-row>
      <v-col cols="12" class="ml-auto">
        <v-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="primary--text" width="15px" v-if="index">NO.</th>
                <template v-for="(h, i) in header" :key="i">
                  <th :class="tblRowStyle(i).header" @click="sort(h.key, h.type, h.sort)">
                    <v-spacer v-if="h.sort">
                      <a>
                        {{ String(h.label).toUpperCase() }}
                        <v-icon size="12" v-if="sortLogic === 'asc' && show === h.key">mdi-arrow-down-thin</v-icon>
                        <v-icon size="12" v-else-if="sortLogic === 'desc' && show === h.key">mdi-arrow-up-thin</v-icon>
                      </a>
                    </v-spacer>
                    <v-spacer v-else>
                      {{ String(h.label).toUpperCase() }}
                    </v-spacer>
                  </th>
                </template>
              </tr>
            </thead>
            <tbody>
              <template v-if="datatable.length > 0">
                <tr v-for="(d, indexNo) in datatable" :key="indexNo">
                  <td class="font-weight-light" v-if="index">{{ incrementNum(indexNo) }}</td>
                  <template v-for="(h, i) in header" :key="i">
                    <td :class="tblRowStyle(i).body">
                      {{
                        formatType(
                          d[String(h.key).toLowerCase()],
                          h?.type,
                          h?.preSymbol,
                          h?.postSymbol,
                          h?.decimalPlace,
                          h?.smallCap
                        )
                      }}
                    </td>
                  </template>
                </tr>
              </template>

              <tr v-else>
                <td
                  v-if="index"
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
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
import MaterialCard from '@/components/MaterialCard.vue'
import moment from 'moment'

export default defineComponent({
  name: 'MaterialRegularTable',
  components: {
    MaterialCard
  },
  props: {
    data: {
      type: Object,
      required: true
    },
    header: {
      type: Object,
      required: true
    },
    title: {
      type: String,
      required: false,
      default: () => 'Table Title'
    },
    index: {
      type: Boolean,
      required: false
    },
    icon: {
      type: String,
      required: false
    },
    color: {
      type: String,
      required: false
    }
  },
  setup(props) {
    const capitalize = (s: string) => {
      return (
        s
          .toLowerCase()
          .split(' ')
          .map((str) => str.charAt(0).toUpperCase() + str.slice(1))
          .join(' ') || ''
      )
    }

    const table = reactive({
      num: 1,
      page: 1,
      datatable: props.data,
      sortLogic: 'asc',
      show: ''
    })

    const sort = (key: string, type?: string, sort?: boolean) => {
      if (sort)
        if (table.sortLogic === 'asc') {
          if (type === 'number' || type === 'double')
            table.datatable.sort((a: any, b: any) => a[`${key}`] - b[`${key}`])
          else
            table.datatable.sort((a: any, b: any) => (a[`${key}`].toLowerCase() > b[`${key}`].toLowerCase() ? 1 : -1))
          table.sortLogic = 'desc'
          table.show = key
        } else if (table.sortLogic === 'desc') {
          if (type === 'number' || type === 'double')
            table.datatable.sort((a: any, b: any) => b[`${key}`] - a[`${key}`])
          else
            table.datatable.sort((a: any, b: any) => (b[`${key}`].toLowerCase() > a[`${key}`].toLowerCase() ? 1 : -1))
          table.sortLogic = 'asc'
          table.show = key
        }
    }

    function incrementNum(i: string) {
      return table.page * table.num + Number(i)
    }

    function tblRowStyle(i: string) {
      if (Number(i) === props.header.length - 1) {
        return { header: 'primary--text text-right', body: 'font-weight-light text-right' }
      }
      return { header: 'primary--text', body: 'font-weight-light' }
    }

    function formatType(
      value: any,
      type = '',
      preSymbol?: string,
      postSymbol?: string,
      decimalPlace = 2,
      smallCap = false
    ) {
      switch (type) {
        case 'date':
          return moment(value).format('ll')
        case 'datetime':
          return moment(value).format('lll')
        case 'int':
        case 'number':
          if (preSymbol) return preSymbol + toCommas(value)
          else if (postSymbol) return toCommas(value) + postSymbol
          else return toCommas(value)
        case 'float':
        case 'double':
          if (preSymbol) return preSymbol + decimalWithPlaces(value, decimalPlace)
          else if (postSymbol) return decimalWithPlaces(value, decimalPlace) + postSymbol
          else return decimalWithPlaces(value, decimalPlace)
        default:
          if (smallCap) return String(value).toLowerCase()
          else return capitalize(value)
      }
    }

    function toCommas(value: number) {
      return value.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
    }

    function decimalWithPlaces(value: number, digit: number) {
      return value.toLocaleString('en-US', { maximumFractionDigits: digit })
    }

    return {
      capitalize,
      ...toRefs(table),
      sort,
      incrementNum,
      tblRowStyle,
      formatType
    }
  }
})
</script>

<style lang="sass" scoped>
.no-record-style
  color: #999
.hid-icon
  display: none
</style>
