<template>
  <div>
    <BAlert :model-value="true">Default Alert</BAlert>
    
    <l-map :zoom="13" :center="[47.4979, 19.0402]" style="height: 500px; width: 100%">
      <l-tile-layer :url="tileUrl" :attribution="attribution" />
      <l-marker :lat-lng="[47.4979, 19.0402]" @click="doStuff()"/>
    </l-map>

  </div>
</template>

<script>
import { BAlert } from 'bootstrap-vue-next';
import { LMap, LTileLayer, LMarker  } from '@vue-leaflet/vue-leaflet';

export default {
  name: 'App',
  components: {
    BAlert, LMap, LTileLayer, LMarker
  },
  data() {
    return {
      tileUrl: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution: "&copy; OpenStreetMap contributors"
    }
  },
  methods: {
    doStuff() {
      console.log("bla")
    }
  }
}
</script>

<style>

</style>