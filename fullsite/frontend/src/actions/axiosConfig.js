import axios from 'axios';

const axiosConfig = axios.create({
baseURL: 'http://localhost:8000',
headers: {Authorization: `Token ${localStorage.getItem('token')}`}
});

export default axiosConfig;