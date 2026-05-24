<template>
  <div class="question-manager-container mx-auto mt-5">
    <!-- Question Progress -->
    <h1 class="text-center text-primary mb-4">
      Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
    </h1>

    <!-- Question Display -->
    <QuestionDisplay
      :question="currentQuestion"
      @answer-clicked="answerClickedHandler"
      class="mb-4"
    />

    <!-- Navigation Buttons -->
    <div class="d-flex justify-content-between">
      <button
        @click="goToPreviousQuestion"
        class="btn btn-secondary"
        :disabled="currentQuestionPosition === 1"
      >
        Précédent
      </button>
      <button
        @click="goToNextQuestion"
        class="btn btn-primary"
        :disabled="currentQuestionPosition === totalNumberOfQuestions"
      >
        Suivant
      </button>
      <button @click="endQuiz" class="btn btn-danger">Terminer le quiz</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from '../components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';

// Reactive state
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);

// Load the initial question when the component mounts
onMounted(async () => {
  await loadQuestionByPosition(currentQuestionPosition.value);
});

// Function to load a question by position
async function loadQuestionByPosition(position) {
  try {
    const response = await quizApiService.getQuestion(position);
    if (response.status === 200) {
      currentQuestion.value = response.data;
      totalNumberOfQuestions.value = response.data.totalQuestions; // Ensure the API includes this field
    }
  } catch (error) {
    console.error('Erreur lors du chargement de la question :', error);
  }
}

// Handler for when an answer is clicked
function answerClickedHandler(answerIndex) {
  console.log(`Réponse sélectionnée : ${answerIndex}`);
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    goToNextQuestion();
  } else {
    endQuiz();
  }
}

// Navigate to the next question
function goToNextQuestion() {
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  }
}

// Navigate to the previous question
function goToPreviousQuestion() {
  if (currentQuestionPosition.value > 1) {
    currentQuestionPosition.value--;
    loadQuestionByPosition(currentQuestionPosition.value);
  }
}

// End the quiz
function endQuiz() {
  console.log('Quiz terminé');
  // Redirect or display a summary page
}
</script>

<style scoped>
/* Styles for the Question Manager */
.question-manager-container {
  max-width: 800px;
  padding: 2rem;
  background: linear-gradient(to bottom right, #ffffff, #f9f9f9);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2rem;
  font-weight: bold;
}

button {
  font-size: 1rem;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

button:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  transform: translateY(-2px);
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

.btn-danger {
  background-color: #dc3545;
  border: none;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>
