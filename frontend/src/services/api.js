import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function getSampleCases() {
  const { data } = await axios.get(`${BASE_URL}/sample_cases`)
  return data
}

export async function postPredict(payload) {
  const { data } = await axios.post(`${BASE_URL}/predict`, payload)
  return data
}