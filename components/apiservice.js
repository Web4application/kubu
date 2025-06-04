import axios from 'axios';

const apiService = axios.create({
    baseURL: 'http://localhost:8080/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const analyzeText = async (text) => {
    const response = await apiService.post('/analyze', { text });
    return response.data;
};
