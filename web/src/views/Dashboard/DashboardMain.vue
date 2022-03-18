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
          title="Website Visits"
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
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MaterialStatsCard from '@/components/MaterialStatsCard.vue'
export default defineComponent({
  name: 'DashboardMain',
  components: {
    MaterialStatsCard
  }
})
</script>
