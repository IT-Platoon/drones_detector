<template>
    <div class="mx-auto pt-2 w-75 text-center">
        <div class="align-between">
            <div class="mt-2">
            <p class="text-h5">
                Детекция компьютерных комплектующих
            </p>
            <p class="font-weight-medium">
                Для получения предсказания выберите файлы
            </p>
            <InputFile @predict="sendFiles"/>
            </div>

            <div class="mt-5 custom-text-20" v-if="this.detection">
            ID вашей задачи на детекцию: <p class="text-h5">{{ this.detection.id }} <v-btn @click="copyText" icon="mdi-content-copy" variant="text"></v-btn></p>
            </div>

            <div class="mt-10 custom-text-20 flex-row">
            Если известен ID вашей детекции введите его для просмотра результатов
            </div>
            <div class="d-flex">
            <v-text-field v-model="this.detectionUUID" class="mx-auto w-75" placeholder="Введите ID вашей детекции" outlined clearable></v-text-field>
            <v-btn dark color="teal-lighten-4" class="ml-1 mt-2" @click="checkDetection">Проверить</v-btn>
            </div>
        </div>

        <v-snackbar
            v-model="this.snackbar"
            :timeout="this.timeout"
            :color="this.snackbarColor"
        >
            {{ this.errorText }}
        </v-snackbar>

        <ListDetectionItems
            v-if="this.detection"
            :detectionTask="this.detection"
            @downloadResults="downloadResults"
        />
    </div>
</template>

<script>
import InputFile from "@/components/InputFile"
import ListDetectionItems from "@/components/ListDetectionItems"
import PredictService from "@/services/predict.service.js"

export default {
  name: "MediaFileDetection",
  components: {
    InputFile,
    ListDetectionItems,
  },
  data() {
    return {
      detection: null,
      errorText: "",
      snackbar: false,
      snackbarColor: "red",
      timeout: 5000,
      detectionUUID: "",
    }
  },
  methods: {
    async sendFiles(files) {
      let form = new FormData()
      files.forEach(file => {
        form.append('files', file, file.name)
      });

      this.detection = null
      this.detectionUUID = ""
      try {
        const response = await PredictService.sendFiles(form)
        this.detection = response.data
        this.snackbarColor = "green"
        this.errorText = "Задача на детекцию успешно создана. Дождитесь ее окончания"
      } catch (_error) {
        this.errorText = _error.response.data.detail
        this.snackbar = true
        this.snackbarColor = "red"
      }
    },
    async checkDetection() {
      if (!this.detectionUUID || !this.detectionUUID.length) {
        this.errorText = "Введите UUID детекции"
        this.snackbar = true
        this.snackbarColor = "red"
        return
      }

      this.detection = null
      try {
        const response = await PredictService.checkDetection(this.detectionUUID)
        this.detection = response.data
      } catch (_error) {
        this.errorText = _error.response.data.detail
        this.snackbar = true
        this.snackbarColor = "red"
      }
    },
    async downloadResults() {
      try {
        const response = await PredictService.downloadDetectionResult(this.detectionUUID)
        this.errorText = "Результаты детекции сейчас начнут скачиваться"
        this.snackbar = true
        this.snackbarColor = "green"
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        const file_name = `${this.detectionUUID}.zip`;
        link.href = url;
        link.setAttribute('download', file_name);
        document.body.appendChild(link);
        link.click();
        resolve(response.data);
      } catch (_error) {
        this.errorText = _error.response.data.detail
        this.snackbar = true
        this.snackbarColor = "red"
      }
    },
    async copyText() {
      await navigator.clipboard.writeText(this.detection?.id || this.detectionUUID);
    }
  }
}
</script>

<style scoped>
.custom-text-20 {
  font-size: 20px;
}
.align-between {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: space-around;
}
</style>
