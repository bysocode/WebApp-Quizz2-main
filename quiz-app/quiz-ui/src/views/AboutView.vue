sours<template>
  <div class="about-container">
    <div class="card shadow-lg p-5 text-center">
      <h1 class="mb-4">About This Application</h1>
      <p class="mb-4">
        This is a quiz application designed to test your knowledge and improve your skills in various subjects. Compete with others, view the leaderboard, and track your progress!
      </p>
      <p>
        Built with ❤️ using modern technologies like <strong>Vue.js</strong>, <strong>Bootstrap</strong>, and <strong>Node.js</strong>.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Container Styles */
.about-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
  padding: 2rem;
}

/* Card Styling */
.card {
  max-width: 800px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  text-align: center;
}

/* Typography */
h1 {
  font-size: 2.5rem;
  color: #0d6efd;
  font-weight: bold;
}

p {
  font-size: 1.2rem;
  color: #6c757d;
  line-height: 1.6;
}
</style>
