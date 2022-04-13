<template>
  <div class="pa-4">
    <MaterialRegularTable
      icon="mdi-poll"
      color="secondary"
      title="Regular Table"
      :header="regularHeader1"
      :data="regularData1"
    />

    <v-spacer class="py-3"></v-spacer>

    <MaterialRegularTable
      icon="mdi-account-tie"
      color="#f7f4b0"
      title="Regular Table With Index"
      :header="regularHeader"
      :data="regularData"
      :index="true"
    />

    <v-spacer class="py-3"></v-spacer>

    <MaterialTable
      :title="title"
      :header="header"
      :data="groupData"
      :numbering="numbering"
      :total-page="totalPage"
      @page-size="getDisplayRows"
      @sort-by="updateSortBy"
      @pages="getDisplayPage"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, onMounted, onUnmounted } from 'vue'
import MaterialTable from '@/components/MaterialTable.vue'
import MaterialRegularTable from '@/components/MaterialRegularTable.vue'
import { useApiWithAuth } from '@/services/api'

interface DataPayload {
  pageSize: number
  page: number
  sortParam: string
  sortBy: string
}

export default defineComponent({
  components: {
    MaterialRegularTable,
    MaterialTable
  },
  setup() {
    // Regular table setup
    const regularData = [
      {
        name: 'Dakota Rice',
        country: 'Niger',
        city: 'Oud-Turnhout',
        salary: 36738,
        kpi: 0.123
      },
      {
        name: 'Minverva Hooper',
        country: 'Curaçao',
        city: 'Sinaas-Waas',
        salary: 23789,
        kpi: 60.003
      },
      {
        name: 'faiRUZ Tahir',
        country: 'malaysia',
        city: 'puncak alam',
        salary: 1623700,
        kpi: 1290.896
      },
      {
        name: 'Sage Rodriguez',
        country: 'Netherlands',
        city: 'Baileux',
        salary: 56142,
        kpi: 70
      }
    ]

    const regularHeader = [
      {
        label: 'Name',
        key: 'name',
        sort: true
      },
      {
        label: 'Country',
        key: 'country',
        sort: false
      },
      {
        label: 'City',
        key: 'city',
        sort: false
      },
      {
        label: 'Salary',
        key: 'salary',
        sort: false,
        type: 'number',
        preSymbol: '$'
      },
      {
        label: 'KPI',
        key: 'kpi',
        sort: false,
        type: 'double',
        decimalPlace: 3,
        postSymbol: ' %'
      }
    ]

    // Regular table setup
    const regularData1 = [
      {
        name: 'Dakota Rice',
        country: 'Niger',
        city: 'Oud-Turnhout',
        salary: 36738,
        kpi: 0.123
      },
      {
        name: 'Minverva Hooper',
        country: 'Curaçao',
        city: 'Sinaas-Waas',
        salary: 23789,
        kpi: 60.003
      },
      {
        name: 'faiRUZ Tahir',
        country: 'malaysia',
        city: 'puncak alam',
        salary: 1623700,
        kpi: 1290.896
      },
      {
        name: 'Sage Rodriguez',
        country: 'Netherlands',
        city: 'Baileux',
        salary: 56142,
        kpi: 70
      }
    ]

    const regularHeader1 = [
      {
        label: 'Name',
        key: 'name',
        sort: true
      },
      {
        label: 'Country',
        key: 'country',
        sort: true
      },
      {
        label: 'City',
        key: 'city',
        sort: true
      },
      {
        label: 'Salary',
        key: 'salary',
        sort: true,
        type: 'number',
        preSymbol: '$'
      },
      {
        label: 'KPI',
        key: 'kpi',
        sort: true,
        type: 'double',
        decimalPlace: 3,
        postSymbol: ' %'
      }
    ]

    // Pagination Table setup
    const payload: DataPayload = {
      pageSize: 10,
      page: 1,
      sortParam: 'created_at',
      sortBy: 'desc'
    }

    const table1 = reactive({
      title: 'Table With Pagination',
      header: [
        {
          label: 'Name',
          key: 'name',
          sort: true
        },
        {
          label: 'Email',
          key: 'email',
          sort: true,
          smallCap: true
        },
        {
          label: 'Created At',
          key: 'created_at',
          sort: true,
          type: 'date'
        }
      ],
      groupData: [],
      numbering: false,
      totalPage: 1,
      payload
    })

    // MARK: Get data when mounted page
    onMounted(() => {
      fetchRecords()
    })

    const { data, get, errorMessage } = useApiWithAuth('v1/users')

    function fetchRecords() {
      get(payload)
        .then(() => {
          if (data.value && data.value.status == 200) {
            table1.groupData = data.value.data
            if (data.value.total <= payload.pageSize) {
              table1.totalPage = 1
            } else {
              const calc = data.value.total / payload.pageSize
              if (calc % 2 == 0) {
                table1.totalPage = calc
              } else {
                let a = calc | 0
                table1.totalPage = a + 1
              }
            }
          } else {
            // MARK: prompt error message
            console.log('ERR', errorMessage.value, data.value.message)
          }
        })
        .catch((error) => {
          console.log('ERR:', error.message)
        })
    }

    function getDisplayRows(event: string) {
      payload.pageSize = Number(event)
      fetchRecords()
    }

    function getDisplayPage(event: string) {
      payload.page = Number(event)
      fetchRecords()
    }

    function updateSortBy(event: DataPayload) {
      payload.sortParam = String(event.sortParam)
      payload.sortBy = String(event.sortBy)
      fetchRecords()
    }

    // MARK: Destroy data
    onUnmounted(() => {
      table1.groupData = []
      table1.title = ''
      table1.header = []
    })

    return {
      regularHeader,
      regularData,
      regularHeader1,
      regularData1,
      ...toRefs(table1),
      getDisplayRows,
      updateSortBy,
      getDisplayPage
    }
  }
})
</script>
