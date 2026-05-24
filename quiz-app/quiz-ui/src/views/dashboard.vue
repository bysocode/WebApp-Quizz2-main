<template>
  <div class="dashboard-container card shadow-lg p-5 mx-auto">
    <h1 class="text-center text-primary">Admin Dashboard</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center mt-4">
      <p class="spinner-text">Loading questions...</p>
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger mt-4 d-flex justify-content-between align-items-center">
      {{ errorMessage }}
      <button @click="fetchAllQuestions" class="btn btn-secondary btn-sm ms-2">Retry</button>
    </div>

    <!-- Questions List -->
    <div v-if="!isLoading && questions.length > 0" class="mt-4">
      <h2 class="text-center mb-4 text-secondary">Manage Questions</h2>
      <ul class="list-group">
        <li
          v-for="question in questions"
          :key="question.id"
          class="list-group-item d-flex justify-content-between align-items-center flex-wrap"
        >
          <span class="question-text">{{ question.text }}</span>
          <div class="action-buttons">
            <button
              @click="goToUpdateQuestion(question.id)"
              class="btn btn-warning btn-sm me-2"
            >
              Update
            </button>
            <button
              @click="deleteQuestion(question.id)"
              class="btn btn-danger btn-sm"
            >
              Delete
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- No Questions Found -->
    <div v-if="!isLoading && questions.length === 0" class="mt-4 text-center">
      <p class="text-muted">No questions found. Start adding some!</p>
    </div>

    <!-- Buttons -->
    <div class="mt-4 d-flex justify-content-center flex-wrap gap-3">
      <button @click="goToAddQuestion" class="btn btn-success btn-lg shadow-sm">
        Add Question
      </button>
      <button @click="deleteAllQuestions" class="btn btn-danger btn-lg shadow-sm">
        Delete All Questions
      </button>
      <button @click="deleteAllParticipations" class="btn btn-danger btn-lg shadow-sm">
        Delete All Participations
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const questions = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const router = useRouter();

const fetchAllQuestions = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const quizInfoResponse = await quizApiService.getQuizInfo();
    if (!quizInfoResponse || quizInfoResponse.status !== 200) {
      throw new Error('Failed to fetch quiz info.');
    }

    const totalQuestions = quizInfoResponse.data.size;
    const fetchedQuestions = [];
    for (let position = 1; position <= totalQuestions; position++) {
      const questionResponse = await quizApiService.getQuestionByPosition(position);
      if (questionResponse && questionResponse.status === 200) {
        fetchedQuestions.push(questionResponse.data);
      } else {
        console.warn(`Failed to fetch question at position ${position}`);
      }
    }

    questions.value = fetchedQuestions;
  } catch (error) {
    errorMessage.value = 'An error occurred while fetching questions.';
    console.error('Error fetching questions:', error);
  } finally {
    isLoading.value = false;
  }
};

const deleteQuestion = async (questionId) => { /* unchanged */ };
const deleteAllQuestions = async () => { /* unchanged */ };
const deleteAllParticipations = async () => { /* unchanged */ };
const goToAddQuestion = () => { router.push('/admin/add-question'); };
const goToUpdateQuestion = (questionId) => { router.push(`/admin/update-question/${questionId}`); };

onMounted(() => {
  fetchAllQuestions();
});
</script>

<style scoped>
/* Updated Container Styling */
.dashboard-container {
  max-width: 1000px;
  margin-top: 50px;
  border-radius: 16px;
  background-color: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  padding: 25px;
  transition: transform 0.3s ease;
}

.dashboard-container:hover {
  transform: translateY(-5px);
}

/* Header Styling */
h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 600;
  color: #007bff;
}

/* Spinner Text */
.spinner-text {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 10px;
}

/* Question Item Styling */
.list-group-item {
  font-size: 1rem;
  padding: 1.2rem;
  border: 1px solid #e9ecef;
  margin-bottom: 0.8rem;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.list-group-item:hover {
  background-color: #f1f3f5;
  transform: translateY(-3px);
}

/* Question Text */
.question-text {
  flex: 1;
  margin-right: 10px;
  font-size: 1rem;
  font-weight: 500;
  color: #343a40;
}

/* Buttons Styling */
.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn {
  font-size: 0.9rem;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-success {
  background-color: #28a745;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  border: none;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-warning {
  background-color: #ffc107;
  border: none;
}

.btn-warning:hover {
  background-color: #e0a800;
}

/* Align Buttons in Footer */
.d-flex.gap-3 {
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

/* Alert Styling */
.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  font-weight: 500;
  display: flex;
  align-items: center;
}
</style>
