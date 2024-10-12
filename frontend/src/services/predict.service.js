import api from './api';

class PredictService {
  baseUrl = 'detection'

  async sendFiles(form) {
    return api.post(
      this.baseUrl,
      form,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        }
      }
    );
  }

  async checkDetection(uuid) {
    return api.get(
      `${this.baseUrl}/${uuid}`,
      {
        headers: {
          "Content-Type": "application/json",
        }
      }
    );
  }

  async downloadDetectionResult(uuid) {
    return api.get(
      `${this.baseUrl}/${uuid}/download`,
      {responseType: 'blob'},
    );
  }
}

export default new PredictService();
