<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

const topScores = ref([]);

onMounted(async () => {
  console.log('Home page mounted');
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.status === 200) {
      // Sort scores in descending order
      const sortedScores = response.data.scores.sort((a, b) => b.score - a.score);
      // Take the top 10 scores
      topScores.value = sortedScores.slice(0, 10);
    } else {
      console.error('Failed to fetch quiz info:', response);
    }
  } catch (error) {
    console.error('Error fetching quiz info:', error);
  }
});
</script>

<template>
  <div class="home-container text-center">
    <!-- Hero Section -->
    <div class="hero-section text-center mb-5">
      <h1 class="hero-title">🎓 Test tes connaissances</h1>
      <p class="hero-tagline">🎉 Prêt à relever le défi ?</p>
      <router-link to="/new-quiz" class="btn btn-primary btn-lg mt-4 btn-hover">
        Démarrer le quiz !
      </router-link>
    </div>

    <!-- Top Scores Section -->
    <div class="card shadow p-4 mb-5 animate-fade-in">
      <h1 class="text-primary mb-4">🏆 Classement des 10 meilleurs scores</h1>
      <ul class="list-group">
        <li
          v-for="(scoreEntry, index) in topScores"
          :key="index"
          class="list-group-item d-flex justify-content-between align-items-center animate-list"
        >
          <span>
            <strong>{{ index + 1 }}.</strong> {{ scoreEntry.playerName }}
          </span>
          <span class="badge bg-success">{{ scoreEntry.score }}</span>
        </li>
      </ul>
    </div>

    <!-- Promotional Banner -->
    <div class="promo-banner text-center mb-5">
      <p>🎉 Don't miss out! Join our Monthly Quiz Challenge now!</p>
    </div>
  </div>
</template>

<style scoped>
/* Container Styling */
.home-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

/* Hero Section */
.hero-section {
  padding: 50px 20px;
  background: linear-gradient(135deg, #007bff, #00c6ff);
  color: white;
  text-align: center;
  border-radius: 12px;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: bold;
}

.hero-tagline {
  font-size: 1.2rem;
  margin-top: 10px;
  opacity: 0.9;
}

/* Card Styling */
.card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Header Styling */
h1 {
  font-family: 'Roboto', sans-serif;
  font-size: 1.8rem;
}

/* List Group Items Styling */
.list-group-item {
  border: none;
  background-color: #f8f9fa;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.list-group-item:hover {
  transform: scale(1.02);
  background-color: #e9ecef;
}

/* Badge Styling */
.badge {
  font-size: 1rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(90deg, #28a745, #218838);
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  color: white;
}

/* Button Hover Effect */
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
.animate-fade-in {
  animation: fadeIn 1s ease-in-out;
}

.animate-slide-in {
  animation: slideIn 1s ease-out;
}

.animate-list {
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: calc(0.1s * var(--list-index, 0));
}

/* Keyframes */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Promotional Banner */
.promo-banner {
  background: linear-gradient(90deg, #ff6f61, #ff9a8b);
  color: white;
  padding: 15px;
  font-size: 1.2rem;
  border-radius: 12px;
  font-weight: bold;
}
</style>
