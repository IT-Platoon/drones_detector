<template>
    <div class="pt-2">
      <v-btn
        color="teal-lighten-4"
        class="text-none"
        round
        depressed
        @click="onButtonClick"
      >
        {{ buttonText }}
      </v-btn>
      <input
        multiple
        chips
        ref="uploader"
        class="d-none"
        type="file"
        accept="image/* video/*"
        @change="onFileChanged"
      >
    </div>
    <div v-if="this.selectedFiles.length" class="pt-2">
        <v-btn 
            @click="predict"
            color="teal-lighten-4"
            round
            depressed
        >
            Сделать предсказание
        </v-btn>
    </div>
</template>

<script>
export default {
    data: () => ({
        defaultButtonText: 'Выберите файлы для предсказания',
        selectedFiles: [],
    }),
    computed: {
        buttonText() {
            return this.selectedFiles.length ? `${this.selectedFiles.length} файлов выбрано` : this.defaultButtonText
        }
    },
    methods: {
        onButtonClick() {
            this.$refs.uploader.click()
        },
        onFileChanged(e) {
            for (const file of e.target.files) {
                this.selectedFiles.push(file)
            }
        },
        predict() {
            this.$emit("predict", this.selectedFiles)
            this.selectedFiles = []
        }
    }
}
</script>

<style>
.v-icon--left {
  margin-right: 8px;
}
</style>