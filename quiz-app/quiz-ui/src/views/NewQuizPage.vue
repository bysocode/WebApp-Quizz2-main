<template>
  <div class="start-quiz-container card shadow p-5 mx-auto mt-5 animate-fade-in">
    <h1 class="text-center text-primary mb-4">🎉 Démarrer un nouveau quiz</h1>
    <p class="text-center text-muted">
      Bienvenue sur la page pour participer à un nouveau quiz !
    </p>

    <!-- Form Section -->
    <div class="form-group mt-4">
      <label for="username" class="form-label fw-bold">Saisissez votre nom :</label>
      <input
        type="text"
        id="username"
        class="form-control input-glow"
        placeholder="Entrez votre nom"
        v-model="username"
      />
      <small v-if="errorMessage" class="text-danger">{{ errorMessage }}</small>
      <button
        class="btn btn-primary w-100 mt-4 btn-hover"
        @click="startNewQuiz"
      >
        🚀 Lancer le quiz
      </button>
    </div>

    <!-- Return Link -->
    <div class="text-center mt-4">
      <router-link to="/" class="btn btn-secondary btn-lg btn-hover">
        Retour à l'accueil
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const errorMessage = ref('');
const router = useRouter();

const startNewQuiz = () => {
  if (username.value.trim() === '') {
    errorMessage.value = 'Veuillez entrer un nom pour démarrer le quiz !';
    return;
  }

  // Clear previous quiz data
  localStorage.removeItem('quizAnswers');

  // Save the player's name in localStorage
  localStorage.setItem('playerName', username.value);

  console.log('Starting new quiz with', username.value);

  // Redirect to the first question
  router.push('/questions/1');
};
</script>

<style scoped>
/* Container Styling */
.start-quiz-container {
  max-width: 600px;
  background: linear-gradient(to bottom right, #ffffff, #f9f9f9);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  animation: fadeIn 1s ease-in-out;
}

/* Header Styling */
h1 {
  font-size: 2.2rem;
  font-weight: bold;
  color: #007bff;
}

p {
  font-size: 1.1rem;
  color: #6c757d;
}

/* Input Field Styling */
.input-glow {
  font-size: 1rem;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ced4da;
  transition: box-shadow 0.3s ease;
}

.input-glow:focus {
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
  border-color: #007bff;
  outline: none;
}

/* Button Styling */
button {
  font-size: 1rem;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* Hover Effect on Buttons */
.btn-hover {
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.btn-hover::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transform: skewX(-20deg);
  transition: left 0.5s ease;
  z-index: -1;
}

.btn-hover:hover::after {
  left: 100%;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
