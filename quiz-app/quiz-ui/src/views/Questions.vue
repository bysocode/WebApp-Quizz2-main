<template>
  <div>
    <div v-if="loading">Loading question...</div>
    <div v-else-if="errorMessage" class="text-danger">
      {{ errorMessage }}
      <button @click="fetchQuestion">Retry</button>
    </div>
    <div v-else>
      <h1>Question {{ question.position }}</h1>
      <p>{{ question.text }}</p>

      <!-- Display the Image (if available) -->
      <div v-if="question.image" class="question-image">
        <img :src="question.image" alt="Question Image" />
      </div>

      <!-- Display Possible Answers -->
      <ul>
        <li v-for="(answer, index) in question.possibleAnswers" :key="index">
          <button
            @click="selectAnswer(index)"
            :class="{ 'selected-answer': selectedAnswer === index }"
          >
            {{ answer.text }}
          </button>
        </li>
      </ul>

      <!-- Navigation Buttons -->
      <div>
        <button @click="goToPreviousQuestion" :disabled="!isPreviousQuestionAvailable" aria-label="Previous Question">
          Précédent
        </button>
        <button @click="goToNextQuestion" :disabled="!isNextQuestionAvailable" aria-label="Next Question">
          Suivant
        </button>
      </div>

      <!-- Finish Quiz Section -->
      <div v-if="isQuizFinished">
        <h2>Finish Quiz</h2>
        <button @click="submitQuiz" :disabled="isSubmitting">
          {{ isSubmitting ? 'Submitting...' : 'Submit Quiz' }}
        </button>
        <p v-if="submitErrorMessage" class="text-danger">{{ submitErrorMessage }}</p>
        <p v-if="submitSuccessMessage" class="text-success">{{ submitSuccessMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const route = useRoute();
const router = useRouter();

const question = ref({});
const loading = ref(true);
const errorMessage = ref('');
const totalQuestions = ref(0);
const answers = ref([]); // Store user's answers
const isSubmitting = ref(false);
const submitErrorMessage = ref('');
const submitSuccessMessage = ref('');
const selectedAnswer = ref(null); // Track the selected answer index

// Retrieve the player's name from localStorage
const playerName = ref(localStorage.getItem('playerName') || '');

// Computed property to check if the quiz is finished
const isQuizFinished = computed(() => {
  return answers.value.length === totalQuestions.value && !answers.value.includes(undefined);
});

// Computed property to check if the previous question is available
const isPreviousQuestionAvailable = computed(() => {
  return question.value.position > 1;
});

// Computed property to check if the next question is available
const isNextQuestionAvailable = computed(() => {
  return question.value.position < totalQuestions.value;
});

// Fetch total questions and current question
onMounted(async () => {
  await fetchTotalQuestions();
  await fetchQuestion();
});

// Watch for route changes to fetch the new question
watch(
  () => route.params.id,
  async (newId) => {
    await fetchQuestion();
  }
);

// Fetch total number of questions
const fetchTotalQuestions = async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.status === 200) {
      totalQuestions.value = response.data.size;
      // Initialize the answers array with a length equal to totalQuestions
      answers.value = new Array(totalQuestions.value).fill(undefined);
    }
  } catch (error) {
    console.error('Error fetching total questions:', error);
    errorMessage.value = 'Failed to fetch total questions. Please try again later.';
  }
};

// Fetch the current question
const fetchQuestion = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';

    const questionId = route.params.id;
    const response = await quizApiService.getQuestion(questionId);

    if (response && response.status === 200) {
      question.value = response.data;

      // Restore the selected answer for the current question
      const savedAnswer = answers.value[question.value.position - 1];
      selectedAnswer.value = savedAnswer !== undefined ? savedAnswer - 1 : null;
    } else {
      errorMessage.value = 'Failed to fetch question. Please try again later.';
    }
  } catch (error) {
    errorMessage.value = 'An error occurred. Please check your connection and try again.';
    console.error('Error fetching question:', error);
  } finally {
    loading.value = false;
  }
};


// Handle answer selection
const selectAnswer = (index) => {
  const questionId = route.params.id;
  answers.value[questionId - 1] = index + 1; // Store the answer (1-based index)
  selectedAnswer.value = index; // Set the selected answer index
  console.log('Selected answer:', index + 1);
  console.log('Answers so far:', answers.value);
};

// Navigate to the previous question
const goToPreviousQuestion = () => {
  if (isPreviousQuestionAvailable.value) {
    const previousQuestionId = parseInt(route.params.id) - 1;
    router.push(`/questions/${previousQuestionId}`);
  }
};

// Navigate to the next question
const goToNextQuestion = () => {
  if (isNextQuestionAvailable.value) {
    const nextQuestionId = parseInt(route.params.id) + 1;
    router.push(`/questions/${nextQuestionId}`);
  }
};

// Submit the quiz
const submitQuiz = async () => {
  if (!isQuizFinished.value) {
    submitErrorMessage.value = 'Please answer all questions before submitting.';
    return;
  }

  try {
    isSubmitting.value = true;
    submitErrorMessage.value = '';
    submitSuccessMessage.value = '';

    // Ensure the player's name is available
    if (!playerName.value) {
      submitErrorMessage.value = 'Player name is missing. Please start the quiz again.';
      return;
    }

    // Prepare the payload
    const payload = {
      playerName: playerName.value,
      answers: answers.value,
    };

    // Submit the quiz
    const response = await quizApiService.submitQuiz(payload);

    if (response && response.status === 200) {
      submitSuccessMessage.value = 'Quiz submitted successfully!';
      console.log('Quiz submission response:', response.data);
      localStorage.setItem('quizResults', JSON.stringify(response.data));
      // Pass the results to the results page via route state
      router.push({
        path: '/results',
        state: { results: response.data }, // Pass the results as route state
      });
    } else {
      submitErrorMessage.value = 'Failed to submit quiz. Please try again later.';
    }
  } catch (error) {
    submitErrorMessage.value = 'An error occurred. Please check your connection and try again.';
    console.error('Error submitting quiz:', error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Style for the selected answer button */
.selected-answer {
  background-color: #007bff; /* Blue background */
  color: white; /* White text */
  border: 2px solid #0056b3; /* Darker blue border */
}

/* Default button style */
button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #f8f9fa; /* Light gray background */
  color: #333; /* Dark text */
  border: 1px solid #ccc; /* Light gray border */
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

button:hover {
  background-color: #e9ecef; /* Slightly darker gray on hover */
}

/* Navigation buttons */
button[disabled] {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Question image styling */
.question-image {
  width: 100%;
  max-width: 500px;
  height: auto;
  margin: 0 auto;
  overflow: hidden;
}

.question-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
}

/* Error and success messages */
.text-danger {
  color: red;
}

.text-success {
  color: green;
}

/* Responsive design */
@media (max-width: 768px) {
  .question-image {
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .question-image {
    max-width: 200px;
  }
}
</style>