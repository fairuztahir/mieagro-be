<template>
  <div class="pa-4">
    <MaterialRegularTable
      icon="mdi-poll"
      color="secondary"
      title="Regular Table"
      :header="regularHeader"
      :data="regularData"
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
        salary: '$36,738'
      },
      {
        name: 'Minverva Hooper',
        country: 'Curaçao',
        city: 'Sinaas-Waas',
        salary: '$23,789'
      },
      {
        name: 'Sage Rodriguez',
        country: 'Netherlands',
        city: 'Baileux',
        salary: '$56,142'
      }
    ]

    const regularHeader = [
      {
        name: 'Name',
        key: 'name',
        sorting: false
      },
      {
        name: 'Country',
        key: 'country',
        sorting: false
      },
      {
        name: 'City',
        key: 'city',
        sorting: false
      },
      {
        name: 'Salary',
        key: 'salary',
        sorting: false
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
          name: 'Name',
          key: 'name',
          sorting: false
        },
        {
          name: 'Email',
          key: 'email',
          sorting: false
        },
        {
          name: 'Created At',
          key: 'created_at',
          sorting: false
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

    const { loading, data, get, errorMessage } = useApiWithAuth('v1/users')

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
                table1.totalPage = Number(calc.toFixed(0)) + 1
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

    // MARK: Destroy data
    onUnmounted(() => {
      table1.groupData = []
      table1.title = ''
      table1.header = []
    })

    return {
      regularHeader,
      regularData,
      ...toRefs(table1),
      getDisplayRows
    }
  }
})
</script>
