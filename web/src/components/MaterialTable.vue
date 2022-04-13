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
              <template v-if="data.length > 0">
                <tr v-for="(d, indexNo) in data" :key="indexNo">
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
    <v-row>
      <v-col class="d-flex mt-2" cols="12" md="2" sm="12">
        <!-- <v-select
          v-model="selectRows"
          :items="selectItems"
          :color="color ? color : 'primary'"
          density="compact"
          label="No of rows"
          variant="outlined"
        ></v-select> -->
        <v-autocomplete
          v-model="selectRows"
          :items="selectItems"
          :color="color ? color : 'primary'"
          density="compact"
          variant="outlined"
          label="No of rows"
        ></v-autocomplete>
      </v-col>
      <v-col cols="12" md="6" sm="12" class="ml-auto d-flex justify-end mt-2">
        <v-pagination
          v-model="page"
          :length="totalPage"
          :total-visible="totalVisible"
          :size="size"
          :color="color ? color : 'primary'"
          rounded
          border
        ></v-pagination>
      </v-col>
    </v-row>
  </MaterialCard>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, computed, watch } from 'vue'
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
    totalPage: {
      type: Number,
      required: true
    },
    pageSize: Function,
    icon: {
      type: String,
      required: false
    },
    color: {
      type: String,
      required: false
    },
    sortBy: Function,
    pages: Function
  },
  setup(props, context) {
    const capitalize = (s: string) => {
      return (
        s
          .toLowerCase()
          .split(' ')
          .map((str) => str.charAt(0).toUpperCase() + str.slice(1))
          .join(' ') || ''
      )
    }
    const selectItems = [5, 10, 20, 40]

    const pagination = reactive({
      num: 1,
      page: 1,
      totalVisible: computed(() => {
        if (screen.width <= 540) {
          return 1
        }
        return 5
      }),
      size: 'x-small',
      selectRows: 10,
      sortLogic: 'asc',
      show: ''
    })

    const sort = (key: string, type?: string, sort?: boolean) => {
      if (sort)
        if (pagination.sortLogic === 'asc') {
          pagination.show = key
          sortByUpdate(key, pagination.sortLogic)
          pagination.sortLogic = 'desc'
        } else if (pagination.sortLogic === 'desc') {
          pagination.show = key
          sortByUpdate(key, pagination.sortLogic)
          pagination.sortLogic = 'asc'
        }
      // else {
      //   pagination.sortLogic = 'desc'
      //   pagination.show = key
      //   sortParamUpdate('created_at')
      //   sortByUpdate(pagination.sortLogic)
      // }
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

    const sortByUpdate = (key: string, value: string) => context.emit('sortBy', { sortParam: key, sortBy: value })

    function toCommas(value: number) {
      return value.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
    }

    function decimalWithPlaces(value: number, digit: number) {
      return value.toLocaleString('en-US', { maximumFractionDigits: digit })
    }

    function setPage(value: number) {
      context.emit('pages', value)
    }

    function rowUpdate(value: number) {
      pagination.page = 1
      context.emit('pageSize', value)
    }

    watch(
      () => pagination.page,
      (currentValue, oldValue) => {
        // console.log(currentValue)
        // console.log(oldValue)
        if (currentValue !== oldValue) setPage(currentValue)
      }
    )

    watch(
      () => pagination.selectRows,
      (currentValue, oldValue) => {
        if (currentValue !== oldValue) rowUpdate(currentValue)
      }
    )

    return {
      capitalize,
      ...toRefs(pagination),
      incrementNum,
      tblRowStyle,
      formatType,
      sort,
      selectItems
    }
  }
})
</script>

<style lang="sass" scoped>
.no-record-style
  color: #999
</style>
