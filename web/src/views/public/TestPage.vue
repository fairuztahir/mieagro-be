<template>
  <div class="flex-content">
    <MaterialExpandCard
      title="Warm Sweater"
      desc="Men's Clothes"
      currency="$"
      :size="sizes"
      @add-cart="addCart"
      @check-out="checkOut"
    ></MaterialExpandCard>
  </div>
  <v-snackbar v-model="snackbar" multi-line :timeout="timeout">
    <div class="font-weight-light center-vertical">{{ String(text).toLowerCase() }}</div>

    <template v-slot:actions>
      <v-btn color="pink" icon="mdi-alpha-x-circle-outline" variant="text" @click="snackbar = false"> </v-btn>
    </template>
  </v-snackbar>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
import MaterialExpandCard from '@/components/MaterialExpandCard.vue'
export default defineComponent({
  name: 'TestPage',
  components: {
    MaterialExpandCard
  },
  setup() {
    const sizes = [
      {
        id: 1,
        value: 'XS',
        status: true,
        price: 199.99
      },
      {
        id: 2,
        value: 'S',
        status: true,
        price: 201
      },
      {
        id: 3,
        value: 'M',
        status: true,
        price: 217.9
      },
      {
        id: 4,
        value: 'L',
        status: true,
        price: 227.99
      },
      {
        id: 5,
        value: 'XL',
        status: true,
        price: 238.3
      },
      {
        id: 6,
        value: '2XL',
        status: false,
        price: 248.99
      },
      {
        id: 7,
        value: '3XL',
        status: false,
        price: 258.99
      }
    ]

    const data = reactive({
      selected: Number(undefined),
      text: 'Please select product options to proceed.',
      snackbar: false,
      timeout: 2500
    })

    function addCart(event: number) {
      data.selected = event
      if (event === undefined) data.snackbar = true
      console.log('addCart', event)
    }

    function checkOut(event: number) {
      data.selected = event
      console.log('checkOut', event)
      if (event === undefined) data.snackbar = true
    }

    return {
      sizes,
      ...toRefs(data),
      addCart,
      checkOut
    }
  }
})
</script>
<style lang="scss">
.flex-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 74vh;
}
</style>
