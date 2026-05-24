<template>
    <div class="results-container card shadow p-4 mx-auto">
      <h1 class="text-center text-primary">Quiz Results</h1>
  
      <!-- Display Player Name and Score -->
      <div v-if="results" class="mt-4">
        <p><strong>Player Name:</strong> {{ results.playerName }}</p>
        <p><strong>Score:</strong> {{ results.score }} / 10</p>
      </div>
  
      <!-- Error Message -->
      <div v-if="errorMessage" class="alert alert-danger mt-4">
        {{ errorMessage }}
      </div>
  
      <!-- Back to Home Button -->
      <button @click="goToHome" class="btn btn-primary w-100 mt-4">
        Back to Home
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import quizApiService from '@/services/QuizApiService';
  
  const router = useRouter();
  
  // State
  const results = ref(null); // Store quiz results
  const errorMessage = ref(''); // Store error messages
  
  // Fetch results when the component is mounted
  onMounted(async () => {
    try {
      // Retrieve the results from localStorage (or you can pass them via route params)
      const storedResults = localStorage.getItem('quizResults');
      if (storedResults) {
        results.value = JSON.parse(storedResults);
      } else {
        errorMessage.value = 'No results found. Please complete the quiz first.';
      }
    } catch (error) {
      errorMessage.value = 'An error occurred while fetching results.';
      console.error('Error fetching results:', error);
    }
  });
  
  // Navigate back to the home page
  const goToHome = () => {
    router.push('/');
  };
  </script>
  
  <style scoped>
  .results-container {
    max-width: 600px;
    margin-top: 50px;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    font-family: 'Roboto', sans-serif;
    font-size: 1.8rem;
  }
  
  .alert {
    border-radius: 8px;
  }
  
  .btn-primary {
    background-color: #007bff;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  </style>