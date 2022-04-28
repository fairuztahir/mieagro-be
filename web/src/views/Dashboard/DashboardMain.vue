<template>
  <div class="pa-4">
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          color="info"
          icon="mdi-twitter"
          title="Followers"
          value="+245"
          sub-icon="mdi-clock"
          sub-text="Just Updated"
        />
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          color="primary"
          icon="mdi-poll"
          title="Visitors"
          value="75.521"
          sub-icon="mdi-tag"
          sub-text="Tracked from Google Analytics"
        />
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          color="success"
          icon="mdi-store"
          title="Revenue"
          value="$ 34,245"
          sub-icon="mdi-calendar"
          sub-text="Last 24 Hours"
        />
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <MaterialStatsCard
          color="orange"
          icon="mdi-sofa"
          title="Bookings"
          value="184"
          sub-icon="mdi-alert"
          sub-icon-color="red"
          sub-text="Get More Space..."
        />
      </v-col>
    </v-row>
    <v-row>
      <template v-for="(data, i) in catalogue" :key="i">
        <v-col cols="12" sm="6" lg="3" v-bind="i">
          <MaterialImage :image="data.image">
            <!-- <template v-slot:reveal-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" size="12" icon v-on="props">
                  <v-icon > mdi-refresh </v-icon>
                </v-btn>
              </template>

              <span>Refresh</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" light icon v-on="props" size="12">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>

              <span>Change Date</span>
            </v-tooltip>
          </template> -->

            <h4 class="card-title font-weight-light mt-2 ml-2">{{ data.title }}</h4>

            <p class="d-inline-flex font-weight-light ml-2 mt-1">{{ data.desc }}</p>

            <template v-slot:actions>
              <v-col cols="12" class="px-0">
                <v-divider />
              </v-col>
              <v-chip
                class="mx-2 font-weight-light chip-content"
                size="x-small"
                label
                :color="data.active ? 'success' : 'error'"
              >
                {{ data.active ? 'Active' : 'Inactive' }}
              </v-chip>
            </template>
          </MaterialImage>
        </v-col>
      </template>
    </v-row>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MaterialStatsCard from '@/components/MaterialStatsCard.vue'
import MaterialImage from '@/components/MaterialImageCard.vue'
export default defineComponent({
  name: 'DashboardPage',
  components: {
    MaterialStatsCard,
    MaterialImage
  },
  setup() {
    const catalogue = [
      {
        title: 'Catalogue One',
        desc: 'Description for catalogue number one. This line supposedly longer than others.',
        image: 'prod1.jpg',
        active: true
      },
      {
        title: 'Catalogue Two',
        desc: 'Description for catalogue number two.',
        image: 'prod2.jpg',
        active: false
      },
      {
        title: 'Catalogue Three',
        desc: 'Description for catalogue number three.',
        image: 'prod3.jpg',
        active: true
      },
      {
        title: 'Catalogue Four',
        desc: 'Description for catalogue number four.',
        image: 'prod4.jpg',
        active: true
      }
    ]

    return {
      catalogue
    }
  }
})
</script>
<style lang="sass" scoped>
.chip-content
  top: -10px
</style>
