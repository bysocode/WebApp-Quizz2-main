<template>
  <div class="score-display card p-5 shadow mt-4 mx-auto">
    <h1 class="text-center text-success mb-4">🎉 Résultat du Quiz</h1>

    <!-- Player Information -->
    <div class="player-info mb-4 text-center">
      <p class="mb-2"><strong>Joueur :</strong> {{ score.playerName }}</p>
      <p class="mb-2"><strong>Score :</strong> {{ score.score }}</p>
    </div>

    <!-- Answer Summary -->
    <h2 class="text-primary mb-3">📝 Résumé des réponses</h2>
    <ul class="list-group">
      <li
        v-for="(summary, index) in score.answersSummaries"
        :key="index"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>Question {{ index + 1 }}</span>
        <span>
          <span v-if="summary.wasCorrect" class="badge bg-success">✅ Correct</span>
          <span v-else class="badge bg-danger">❌ Incorrect</span>
          <small class="text-muted">(Bonne réponse : {{ summary.correctAnswerPosition }})</small>
        </span>
      </li>
    </ul>

    <!-- Rankings -->
    <h2 class="text-primary mt-4 mb-3">📊 Classement</h2>
    <ul class="list-group">
      <li
        v-for="(entry, index) in rankings"
        :key="index"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>{{ index + 1 }}. {{ entry.playerName }}</span>
        <span>{{ entry.score }}</span>
      </li>
    </ul>

    <!-- Top Scores -->
    <h2 class="text-primary mt-4 mb-3">🏆 Meilleurs Scores</h2>
    <ul class="list-group">
      <li
        v-for="(entry, index) in topScores"
        :key="index"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>{{ index + 1 }}. {{ entry.playerName }}</span>
        <span>{{ entry.score }}</span>
      </li>
    </ul>

    <!-- Home Button -->
    <button @click="goToHome" class="btn btn-primary btn-lg mt-4">
      Retour à l'accueil
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

// Props for passing score data
const props = defineProps({
  score: {
    type: Object,
    required: true,
  },
});

// Reactive variables for rankings and top scores
const rankings = ref([]);
const topScores = ref([]);

// Vue Router for navigation
const router = useRouter();

// Fetch participations on component mount
onMounted(async () => {
  try {
    const { data, status } = await quizApiService.getAllParticipations();
    if (status === 200) {
      rankings.value = data.sort((a, b) => b.score - a.score); // Sort by descending score
      topScores.value = rankings.value.slice(0, 5); // Top 5 scores
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des données', error);
  }
});

// Navigate back to the home page
function goToHome() {
  router.push('/');
}
</script>

<style scoped>
/* Score Display Styling */
.score-display {
  max-width: 750px;
  background: linear-gradient(to right, #ffffff, #f9f9f9);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

/* Header Styling */
h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #4caf50;
}

h2 {
  font-size: 1.8rem;
  color: #007bff;
}

/* List Styling */
ul {
  padding: 0;
  list-style-type: none;
}

.list-group-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  margin-bottom: 10px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Badge Styling */
.badge {
  font-size: 1rem;
  padding: 0.5rem 0.8rem;
  border-radius: 12px;
}

/* Button Styling */
button {
  display: block;
  width: 100%;
  font-size: 1.2rem;
  padding: 12px;
  font-weight: bold;
  background: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}
</style>
