import axios from "axios";

const isProduction = process.env.NODE_ENV === "production"
console.log(isProduction)
const instance = axios.create({
  baseURL: `http://${isProduction ? 'localhost' : '0.0.0.0:8000'}/api/v1/`,
});

export default instance;
