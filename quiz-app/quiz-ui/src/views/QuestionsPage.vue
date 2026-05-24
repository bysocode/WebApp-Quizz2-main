<template>
  <div class="quiz-container mt-5">
    <!-- Question Card -->
    <div class="card p-4 shadow">
      <h1 class="text-center text-primary mb-4">📝 Question</h1>
      <p class="text-center text-muted">
        Vous répondez à la question ID : <span class="fw-bold">{{ questionId }}</span>
      </p>
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation mt-4 d-flex justify-content-between">
      <button class="btn btn-outline-secondary" @click="previousQuestion">
        Précédent
      </button>
      <button class="btn btn-primary" @click="nextQuestion">
        Suivant
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const questionId = ref(route.params.id); // Reactive reference for question ID

onMounted(() => {
  console.log('Question page mounted for ID:', questionId.value);
});

// Navigate to the previous question
const previousQuestion = () => {
  const prevId = parseInt(questionId.value) - 1;
  if (prevId > 0) {
    router.push(`/quiz/${prevId}`);
  } else {
    console.log('No previous question available.');
  }
};

// Navigate to the next question
const nextQuestion = () => {
  const nextId = parseInt(questionId.value) + 1;
  router.push(`/quiz/${nextId}`);
};
</script>

<style scoped>
.quiz-container {
  max-width: 700px;
  margin: auto;
  padding: 1rem;
  text-align: center;
}

.card {
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  font-family: 'Roboto', sans-serif;
  color: #0d6efd;
  font-size: 2rem;
}

.text-muted {
  font-size: 1rem;
}

.navigation button {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}
</style>
