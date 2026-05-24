// Import global styles
import './assets/main.css';

// Import Vue core and application root
import { createApp } from 'vue';
import App from './App.vue';

// Import router for routing
import router from './router';

// Import Axios for API calls
import axios from 'axios';

// Set the base URL for Axios
axios.defaults.baseURL = 'http://localhost:5000'; // Replace with your backend URL

// Add a request interceptor to include the JWT token in headers
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle errors globally
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized errors (e.g., redirect to login)
      localStorage.removeItem('adminToken');
      router.push('/admin');
    }
    return Promise.reject(error);
  }
);

// Create Vue app instance
const app = createApp(App);

// Use plugins and libraries
app.use(router);

// Mount the app to the DOM
app.mount('#app');

// Display a console message when the app successfully mounts
console.info('%cQuiz App successfully started!', 'color: #42b983; font-size: 16px;');