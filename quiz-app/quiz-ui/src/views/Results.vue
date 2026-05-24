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
  
  const router = useRouter();
  
  // State
  const results = ref(null); // Store quiz results
  const errorMessage = ref(''); // Store error messages
  
  // Fetch results when the component is mounted
  onMounted(() => {
    // Retrieve the results from route state
    if (router.currentRoute.value.state?.results) {
      results.value = router.currentRoute.value.state.results;
      localStorage.setItem('quizResults', JSON.stringify(results.value));
    } else {
    const savedResults = localStorage.getItem('quizResults');
    if (savedResults) {
      results.value = JSON.parse(savedResults);
    } else {
      errorMessage.value = 'No results found. Please complete the quiz first.';
    }
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