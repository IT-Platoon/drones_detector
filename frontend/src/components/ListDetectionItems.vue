<template>
    <div v-if="this.detectionTask.detection_items?.length" class="py-10">
        <div v-for="item of this.detectionTask.detection_items" :key="item.id" class="my-3 pa-5 bg-teal-lighten-5 rounded-lg">
            {{ item.origin_file.split("/")[item.origin_file.split("/").length - 1] }}
            <div v-if="item.classes?.length">Обнаруженные классы: {{ item.classes }}</div>
            <div v-else>Ничего не обнаружено</div>
            <div v-if="item.type === 'IMAGE'" class="d-flex">
                <v-img
                    class="mx-auto"
                    height="520"
                    width="520"
                    :src="item.origin_file"
                >
                    <template v-slot:placeholder>
                        <div class="d-flex align-center justify-center fill-height">
                            <v-progress-circular color="grey-lighten-4" indeterminate></v-progress-circular>
                        </div>
                    </template>
                </v-img>
                <v-img
                    class="mx-auto"
                    height="520"
                    width="520"
                    :src="item.predict_file"
                >
                    <template v-slot:placeholder>
                        <div class="d-flex align-center justify-center fill-height">
                            <v-progress-circular color="grey-lighten-4" indeterminate></v-progress-circular>
                        </div>
                    </template>
                </v-img>
            </div>
            <div v-else-if="item.type === 'VIDEO'">
                <video
                    :src="item.origin_file"
                    height="520"
                    width="640"
                    controls
                    type='video/webm'
                ></video>
                <video
                    :src="item.predict_file"
                    height="520"
                    width="640"
                    controls
                    type='video/webm'
                ></video>
            </div>
        </div>
        <v-btn @click="downloadResults" color="teal-lighten-4">Скачать результаты детекции</v-btn>
    </div>
</template>

<script>
export default {
    name: "ListDetectionItems",
    props: {
        detectionTask: {
            type: Object,
            required: true,
        },
    },
    methods: {
        async downloadResults(){
            this.$emit("downloadResults")
        }
    }
}
</script>