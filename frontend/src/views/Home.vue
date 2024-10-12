<template>
  <v-card>
    <MediaFileDetection />
  </v-card>
</template>

<script>
import MediaFileDetection from "@/components/MediaFileDetection"

export default {
  name: "Home",
  components: {
    MediaFileDetection,
  },
  data() {
    return {
      tab: null,
    }
  },
}
</script>
