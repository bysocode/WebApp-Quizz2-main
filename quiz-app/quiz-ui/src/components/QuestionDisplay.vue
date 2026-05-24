<template>
  <div class="question-container card shadow-sm p-4">
    <!-- Question Title -->
    <h2 class="question-title text-primary mb-3">{{ currentQuestion.title }}</h2>

    <!-- Question Text -->
    <p class="question-text mb-4">{{ currentQuestion.text }}</p>

    <!-- Associated Image -->
    <div class="question-image mb-4" v-if="currentQuestion.image">
      <img :src="currentQuestion.image" alt="Image associée à la question" />
    </div>

    <!-- Possible Answers -->
    <ul class="answers-list">
      <li
        v-for="(answer, index) in currentQuestion.possibleAnswers"
        :key="index"
        class="answer-item"
      >
        <button
          class="answer-button"
          @click="$emit('answer-clicked', index)"
        >
          {{ answer.text }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// Define props
const props = defineProps({
  currentQuestion: Object,
});

// Define emitted events
const emit = defineEmits(['answer-clicked']);
</script>

<style scoped>
/* Container Styling */
.question-container {
  max-width: 700px;
  margin: 2rem auto;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.question-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Question Title */
.question-title {
  font-family: 'Roboto', sans-serif;
  font-size: 1.8rem;
  color: #007bff;
  text-align: center;
}

/* Question Text */
.question-text {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #333;
  text-align: center;
}

/* Image Styling */
.question-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: contain;
  border: 2px solid #ddd;
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.question-image img:hover {
  transform: scale(1.05);
  border-color: #007bff;
}

/* Answers List */
.answers-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.answer-item {
  margin-bottom: 1rem;
}

/* Answer Button Styling */
.answer-button {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  background-color: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 8px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
}

.answer-button:hover {
  background-color: #007bff;
  color: #ffffff;
  transform: translateY(-2px);
}

.answer-button:active {
  transform: translateY(0);
}
</style>
