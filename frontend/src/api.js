import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

export async function sendChat(query, topK = 3) {
  const { data } = await api.post('/chat', { query, top_k: topK });
  return data;
}

export async function getSection(name) {
  const { data } = await api.get(`/sections/${name}`);
  return data;
}

export async function getStats() {
  const { data } = await api.get('/stats');
  return data;
}

export async function getHealth() {
  const { data } = await api.get('/health');
  return data;
}
