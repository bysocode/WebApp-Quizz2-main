<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const password = ref('');
const isAuthenticated = ref(false);
const errorMessage = ref('');
const isLoading = ref(false);

const router = useRouter();

// Check if the user is already authenticated
const checkAuth = () => {
  const token = localStorage.getItem('adminToken');
  if (token) {
    isAuthenticated.value = true;
  }
};

// Run checkAuth when the component is mounted
onMounted(() => {
  checkAuth();
});

const login = async () => {
  if (!password.value) {
    errorMessage.value = 'Veuillez entrer un mot de passe.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await quizApiService.login(password.value);
    if (response && response.status === 200 && response.data.token) {
      // Store the token in local storage
      localStorage.setItem('adminToken', response.data.token);
      isAuthenticated.value = true;
      alert('Connexion réussie !');
      goToAdminDashboard();
    } else {
      errorMessage.value = 'Mot de passe incorrect';
      alert('Mot de passe incorrect');
    }
  } catch (error) {
    errorMessage.value = 'Une erreur est survenue. Veuillez réessayer.';
    console.error('Error during login:', error);
    alert('Une erreur est survenue. Veuillez réessayer.');
  } finally {
    isLoading.value = false;
  }
};

const logout = () => {
  // Remove the token from local storage
  localStorage.removeItem('adminToken');
  isAuthenticated.value = false;
  password.value = '';
  errorMessage.value = '';
  alert('Vous êtes déconnecté.');
};

const goToAdminDashboard = () => {
  router.push('/admin/dashboard'); // Navigate to the admin dashboard
};
</script>

<template>
  <div class="admin-login-container card shadow p-4 mx-auto animate-fade-in">
    <h1 class="text-center text-primary mb-4">Administration</h1>

    <!-- Login Form -->
    <div v-if="!isAuthenticated" class="mt-4">
      <p class="text-center">Veuillez entrer le mot de passe pour accéder :</p>
      <input
        type="password"
        v-model="password"
        placeholder="Mot de passe"
        class="form-control input-glow mb-3"
      />
      <button @click="login" :disabled="isLoading" class="btn btn-primary w-100 btn-hover">
        <span v-if="isLoading">Connexion en cours...</span>
        <span v-else>Se connecter</span>
      </button>
      <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
    </div>

    <!-- Admin Section -->
    <div v-else class="mt-4 text-center">
      <p class="text-muted">Bienvenue dans la section administrateur !</p>
      <button @click="goToAdminDashboard" class="btn btn-success w-100 mb-3 btn-hover">
        Accéder au tableau de bord
      </button>
      <button @click="logout" class="btn btn-danger w-100 btn-hover">
        Déconnexion
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Container Styling */
.admin-login-container {
  max-width: 400px;
  margin-top: 100px;
  background: linear-gradient(to bottom right, #ffffff, #f8f9f9);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  animation: fadeIn 1s ease-in-out;
}

/* Header Styling */
h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #007bff;
}

/* Text Styling */
p {
  color: #6c757d;
  font-size: 1rem;
}

/* Input Styling */
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

button.btn-primary {
  background-color: #007bff;
  border: none;
}

button.btn-primary:hover {
  background-color: #0056b3;
}

button.btn-success {
  background-color: #28a745;
  border: none;
}

button.btn-success:hover {
  background-color: #218838;
}

button.btn-danger {
  background-color: #dc3545;
  border: none;
}

button.btn-danger:hover {
  background-color: #c82333;
}

/* Hover Effect for Buttons */
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

/* Error Message */
.text-danger {
  color: #dc3545;
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
