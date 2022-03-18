<template>
  <div class="pa-4">
    <MaterialTable :title="title" :header="header" :data="groupData" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
import MaterialTable from '@/components/MaterialTable.vue'
export default defineComponent({
  components: {
    MaterialTable
  },
  setup() {
    const data = [
      {
        no: 1,
        name: 'Dakota Rice',
        country: 'Niger',
        city: 'Oud-Turnhout',
        salary: '$36,738'
      },
      {
        no: 2,
        name: 'Minverva Hooper',
        country: 'Curaçao',
        city: 'Sinaas-Waas',
        salary: '$23,789'
      },
      {
        no: 3,
        name: 'Sage Rodriguez',
        country: 'Netherlands',
        city: 'Baileux',
        salary: '$56,142'
      }
    ]

    const table1 = reactive({
      title: 'Test Table',
      header: [
        {
          name: 'no'
        },
        {
          name: 'Name'
        },
        {
          name: 'Country'
        },
        {
          name: 'City'
        },
        {
          name: 'Salary'
        }
      ],
      groupData: data
    })

    return {
      ...toRefs(table1)
    }
  }
})
</script>
