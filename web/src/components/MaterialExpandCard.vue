<template>
  <v-card :class="isMobile ? 'card-mobile' : 'card'" elevation="1">
    <div :class="isMobile ? 'imgBx-mobile' : 'imgBx'">
      <v-img :src="image ? image : 'sweater.png'" cover></v-img>
    </div>
    <div :class="isMobile ? 'details-mobile' : 'details'">
      <h3>
        {{ title }} <br />
        <span>{{ desc }}</span>
      </h3>
      <h4>Product Details</h4>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deleniti quae.</p>
      <template v-if="Object(size).length">
        <h4>Size</h4>
        <!-- <ul class="size">
          <template v-for="data in size" :key="data">
            <li v-bind="data" v-if="data.status">{{ data.value }}</li>
          </template>
        </ul> -->

        <v-item-group selected-class="bg-purple" v-model="sizeValue">
          <template v-for="data in size" :key="data">
            <v-item v-slot="{ isSelected, selectedClass, toggle }">
              <v-btn
                :class="[selectedClass, 'mr-2 mb-1 font-weight-light']"
                @click="toggle"
                size="x-small"
                color="#fff"
                :variant="isSelected ? 'contained' : 'outlined'"
                v-if="data.status"
                :value="data.value"
                >{{ data.value }}</v-btn
              >
            </v-item>
          </template>
        </v-item-group>
      </template>
      <v-row>
        <v-col cols="12" md="12" sm="12">
          <div :class="isMobile ? 'group-mobile' : 'group'">
            <h2>
              <sup>{{ currency }}</sup
              >{{ price }}<small>{{ decimal }}</small>
            </h2>

            <div>
              <v-btn class="quantity-btn" icon="mdi-plus" variant="outlined" size="x-small" @click="increment"></v-btn>
              <label>{{ quantity }}</label>
              <v-btn class="quantity-btn" icon="mdi-minus" variant="outlined" size="x-small" @click="decrement"></v-btn>
            </div>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <v-btn class="font-weight-light" variant="outlined" size="small" color="#fff" @click="submitCart"
            >Add Cart</v-btn
          >
          <v-btn
            class="checkout-btn font-weight-light"
            variant="contained-flat"
            size="small"
            color="#fff"
            @click="submitCheckout"
            >CheckOut</v-btn
          >
        </v-col>
      </v-row>

      <!-- <div class="group">
        <h2>
          <sup>{{ currency }}</sup
          >{{ price }}<small>{{ decimal }}</small>
        </h2>
        <v-btn class="font-weight-light" variant="contained-flat" size="small" color="#fff" @click="submitCart">Add Cart</v-btn>
      </div> -->
    </div>
  </v-card>
</template>
<script lang="ts">
import { defineComponent, toRefs, reactive, watch, computed } from 'vue'
export default defineComponent({
  name: 'MaterialExpandCard',
  components: {},
  props: {
    addCart: Function,
    checkOut: Function,
    size: {
      type: Object,
      default: () => ({})
    },
    image: String,
    title: {
      type: String,
      default: 'Warm Sweater'
    },
    desc: {
      type: String,
      default: "Men's Clothes"
    },
    currency: {
      type: String,
      default: '$'
    }
  },
  setup(props, context) {
    const toggle = reactive({
      sizeValue: undefined,
      price: '0',
      decimal: '.00',
      quantity: 1
    })

    watch(
      () => toggle.sizeValue,
      (currentValue, oldValue) => {
        if (currentValue !== oldValue) getPricing(currentValue)
      }
    )

    function getPricing(curr: number) {
      if (Object(props.size).length) {
        if (toggle.sizeValue !== undefined) getDecimalPart(props.size[curr].price)
        else getDecimalPart(0.0)
      }
    }

    function getDecimalPart(num: number) {
      num = (Math.round((num + Number.EPSILON) * 100) / 100) * toggle.quantity
      if (Number.isInteger(num)) {
        toggle.decimal = '.00'
        toggle.price = num.toString()
      } else {
        const setround = num.toFixed(2)
        const priceArr = setround.split('.')
        toggle.price = priceArr[0]
        if (priceArr[1].length < 2) toggle.decimal = '.' + priceArr[1] + '0'
        else toggle.decimal = '.' + priceArr[1]
      }
    }

    function increment() {
      if (toggle.quantity < 10) toggle.quantity = toggle.quantity + 1
      if (toggle.sizeValue !== undefined) getPricing(toggle.sizeValue)
    }

    function decrement() {
      if (toggle.quantity > 1) toggle.quantity = toggle.quantity - 1
      if (toggle.sizeValue !== undefined) getPricing(toggle.sizeValue)
    }

    return {
      ...toRefs(toggle),
      increment,
      decrement,
      submitCart: () => context.emit('addCart', toggle.sizeValue),
      submitCheckout: () => context.emit('checkOut', toggle.sizeValue)
    }
  },
  computed: {
    isMobile() {
      return this.$vuetify.display.smAndDown
    }
  }
})
</script>
<style lang="scss" scoped>
.card {
  position: relative;
  width: 300px;
  height: 380px;
  // background: #000;
  // box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1);
  display: flex;
  overflow: hidden;
  transition: 0.5s ease-in-out;
}
.card:hover {
  width: 600px;
}
.card .imgBx {
  position: relative;
  min-width: 300px;
  height: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 2;
}
.card .imgBx .v-img {
  max-width: 250px;
  transition: 0.5s ease-in-out;
}
.card:hover .imgBx .v-img {
  transform: rotate(-5deg) translateX(-10px);
}
.card .details {
  position: absolute;
  left: 0;
  min-width: 300px;
  height: 100%;
  background: #4ba9e9;
  display: flex;
  justify-content: center;
  padding: 20px;
  flex-direction: column;
  z-index: 1;
  transition: 0.5s ease-in-out;
}
.card:hover .details {
  left: 300px;
}
.card .details::before {
  content: '';
  position: absolute;
  left: 0;
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-left: 10px solid #fff;
}
.card .details h3 {
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 1.5em;
  line-height: 1em;
}
.card .details h3 span {
  font-size: 0.65em;
  font-weight: 300;
  text-transform: none;
  opacity: 0.85;
}
.card .details h4 {
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 0.9em;
  margin-top: 20px;
  margin-bottom: 10px;
  line-height: 1em;
}
.card .details p {
  color: #fff;
  opacity: 0.85;
  font-size: 0.8em;
}
.card .details .size {
  display: flex;
  gap: 10px;
}
.card .details .size li {
  list-style: none;
  color: #fff;
  font-size: 0.9em;
  width: 40px;
  height: 40px;
  border: 2px solid #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 500;
  opacity: 0.65;
  cursor: pointer;
}
.card .details .size li:hover {
  color: #4ba9e9;
  background: #fff;
  opacity: 1;
}
.card .details .group {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}
.card .details .group h2 {
  color: #fff;
  font-weight: 600;
  font-size: 2em;
}
.card .details .group h2 sup {
  font-weight: 300;
  font-size: 0.4em;
  top: -12px;
}
.card .details .group h2 small {
  font-size: 0.75em;
}
.card .details .group a {
  display: inline-flex;
  padding: 10px 25px;
  background: #fff;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: 500;
  color: #4ba9e9;
}
.card .details .group label {
  display: inline-flex;
  padding: 1px 7px;
  // background: #fff;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: 500;
  font-size: 1.35em;
  // color: #4ba9e9;
  color: #fff;
}
.checkout-btn {
  color: #4ba9e9;
  margin-left: 10px;
}
.quantity-btn {
  display: inline-flex;
  color: #fff;
}
.v-row {
  flex: 0 0 auto;
}

// Mobile view
.card-mobile {
  position: relative;
  width: 300px;
  height: 380px;
  display: block;
  overflow: hidden;
  transition: 0.5s ease-in-out;
}
.card-mobile:hover {
  height: 760px;
}
.card-mobile .imgBx-mobile {
  position: relative;
  min-height: 380px;
  width: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 2;
}
.card-mobile .imgBx-mobile .v-img {
  max-width: 250px;
  transition: 0.5s ease-in-out;
}
.card-mobile:hover .imgBx-mobile .v-img {
  transform: rotate(-5deg) translateX(-10px);
}
.card-mobile .details-mobile {
  position: absolute;
  top: 0;
  min-height: 380px;
  width: 100%;
  background: #4ba9e9;
  display: flex;
  justify-content: center;
  padding: 20px;
  flex-direction: column;
  z-index: 1;
  transition: 0.5s ease-in-out;
}
.card-mobile:hover .details-mobile {
  top: 380px;
}
.card-mobile .details-mobile::before {
  content: '';
  position: absolute;
  top: 0;
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-left: 10px solid transparent;
  border-top: 10px solid #fff;
  left: 49%;
}
.card-mobile .details-mobile h3 {
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 1.65em;
  line-height: 1em;
}
.card-mobile .details-mobile h3 span {
  font-size: 0.65em;
  font-weight: 300;
  text-transform: none;
  opacity: 0.85;
}
.card-mobile .details-mobile h4 {
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 0.9em;
  margin-top: 20px;
  margin-bottom: 10px;
  line-height: 1em;
}
.card-mobile .details-mobile p {
  color: #fff;
  opacity: 0.85;
  font-size: 0.8em;
}
.card-mobile .details-mobile .size-mobile {
  display: flex;
  gap: 10px;
}
.card-mobile .details-mobile .size-mobile li {
  list-style: none;
  color: #fff;
  font-size: 0.9em;
  width: 40px;
  height: 40px;
  border: 2px solid #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 500;
  opacity: 0.65;
  cursor: pointer;
}
.card-mobile .details-mobile .size-mobile li:hover {
  color: #4ba9e9;
  background: #fff;
  opacity: 1;
}
.card-mobile .details-mobile .group-mobile {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}
.card-mobile .details-mobile .group-mobile h2 {
  color: #fff;
  font-weight: 600;
  font-size: 2em;
}
.card-mobile .details-mobile .group-mobile h2 sup {
  font-weight: 300;
  font-size: 0.4em;
  top: -12px;
}
.card-mobile .details-mobile .group-mobile h2 small {
  font-size: 0.75em;
}
.card-mobile .details-mobile .group-mobile a {
  display: inline-flex;
  padding: 10px 25px;
  background: #fff;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: 500;
  color: #4ba9e9;
}
.card-mobile .details-mobile .group-mobile label {
  display: inline-flex;
  padding: 1px 7px;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: 500;
  font-size: 1.35em;
  color: #fff;
}
</style>
