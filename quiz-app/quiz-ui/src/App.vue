<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <div id="app">
    <!-- Include the navigation bar -->
    <NavBar />

    <!-- Render the route content -->
    <main class="container mt-4">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
/* Global app styles */
#app {
  font-family: 'Roboto', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f9f9f9;
  color: #333;
  margin-top: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main.container {
  flex: 1;
}

/* Header styles */
header {
  line-height: 1.5;
}

/* Navigation bar */
nav {
  font-size: 1.1rem;
  background-color: #42b983; /* Updated for a modern look */
  color: white;
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 0 0 12px 12px;
}

nav a {
  text-decoration: none;
  color: white;
  margin: 0 1rem;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #c8f7c5;
}

nav a.router-link-exact-active {
  font-weight: bold;
  text-decoration: underline;
}

nav .logo {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
}

@media (max-width: 768px) {
  nav {
    flex-direction: column;
    text-align: center;
  }
  nav a {
    margin: 0.5rem 0;
  }
}
</style>
