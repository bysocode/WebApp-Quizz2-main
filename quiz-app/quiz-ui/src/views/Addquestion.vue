<template>
  <div class="add-question-container card shadow p-4 mx-auto">
    <h1 class="text-center text-primary">Add Question</h1>

    <!-- Go Back Button -->
    <button @click="goBack" class="btn btn-secondary mb-4">
      ← Go Back
    </button>

    <!-- Form -->
    <form @submit.prevent="submitQuestion">
      <!-- Text -->
      <div class="mb-3">
        <label for="text" class="form-label">Question Text</label>
        <input
          type="text"
          v-model="question.text"
          id="text"
          class="form-control"
          placeholder="Enter the question text"
          required
        />
      </div>

      <!-- Title -->
      <div class="mb-3">
        <label for="title" class="form-label">Question Title</label>
        <input
          type="text"
          v-model="question.title"
          id="title"
          class="form-control"
          placeholder="Enter the question title"
          required
        />
      </div>

      <!-- Image Upload -->
      <div class="mb-3">
        <label for="image" class="form-label">Question Image</label>
        <input
          type="file"
          id="image"
          class="form-control"
          accept="image/*"
          @change="handleImageUpload"
        />
      </div>

      <!-- Position -->
      <div class="mb-3">
        <label for="position" class="form-label">Position</label>
        <input
          type="number"
          v-model="question.position"
          id="position"
          class="form-control"
          placeholder="Enter the question position"
          required
        />
      </div>

      <!-- Possible Answers -->
      <div class="mb-3">
        <label class="form-label">Possible Answers (Exactly 4)</label>
        <div
          v-for="(answer, index) in question.possibleAnswers"
          :key="index"
          class="mb-2"
        >
          <div class="input-group">
            <input
              type="text"
              v-model="answer.text"
              class="form-control"
              placeholder="Enter answer text"
              required
            />
            <div class="input-group-text">
              <input
                type="radio"
                v-model="correctAnswerIndex"
                :value="index"
                class="form-check-input"
              />
              <label class="form-check-label ms-2">Correct</label>
            </div>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary w-100">Submit</button>
    </form>

    <!-- Success Message -->
    <div v-if="isSuccess" class="alert alert-success mt-4">
      Question added successfully!
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger mt-4">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const router = useRouter();

// Question data
const question = ref({
  text: '',
  title: '',
  image: '',
  position: 1,
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
  ],
});

// Track the correct answer index
const correctAnswerIndex = ref(null);

// State
const isSuccess = ref(false);
const errorMessage = ref('');

// Handle image upload
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      question.value.image = e.target.result; // Set the Base64 string
    };
    reader.readAsDataURL(file); // Convert the image to Base64
  }
};

// Submit the question
const submitQuestion = async () => {
  try {
    // Validate at least one correct answer
    if (correctAnswerIndex.value === null) {
      errorMessage.value = 'Please select the correct answer.';
      return;
    }

    // Mark the correct answer
    question.value.possibleAnswers.forEach((answer, index) => {
      answer.isCorrect = index === correctAnswerIndex.value;
    });

    // Validate all answers have text
    const hasEmptyAnswer = question.value.possibleAnswers.some(
      (answer) => !answer.text.trim()
    );
    if (hasEmptyAnswer) {
      errorMessage.value = 'All answers must have text.';
      return;
    }

    // Call the API to add the question
    const response = await quizApiService.addQuestion(question.value);
    if (response && response.status === 200) {
      isSuccess.value = true;
      errorMessage.value = '';
      setTimeout(() => {
        router.push('/admin/dashboard'); // Redirect to the dashboard after success
      }, 2000);
    } else {
      errorMessage.value = 'Failed to add the question.';
    }
  } catch (error) {
    errorMessage.value = 'An error occurred while adding the question.';
    console.error('Error adding question:', error);
  }
};

// Go back to the previous page
const goBack = () => {
  router.go(-1); // Go back to the previous page
};
</script>

<style scoped>
.add-question-container {
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

.form-label {
  font-weight: 500;
}

.input-group-text {
  background-color: #f8f9fa;
}

.alert {
  border-radius: 8px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
