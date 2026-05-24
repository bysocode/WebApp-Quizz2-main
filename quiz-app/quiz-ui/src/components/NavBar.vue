<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container-fluid">
      <!-- Brand logo with router-link -->
      <router-link to="/" class="navbar-brand fw-bold">
        <span class="brand-logo">🎓 Quiz App</span>
      </router-link>

      <!-- Navbar toggler for mobile devices -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Collapsible navbar links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link" active-class="active">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/quiz" class="nav-link" active-class="active">Take Quiz</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin" class="nav-link" active-class="active">Admin</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
/* No additional logic required; this is a presentation component. */
</script>

<style scoped>
/* Navbar custom styles */
.navbar {
  padding: 1rem 1.5rem;
  border-radius: 0 0 12px 12px; /* Rounded bottom corners for a modern look */
  position: sticky;
  top: 0;
  z-index: 1000; /* Ensure the navbar stays on top */
  transition: all 0.3s ease;
}

/* Navbar hover effect */
.navbar:hover {
  background-color: #0056b3; /* Darker shade on hover */
}

/* Brand logo styling */
.brand-logo {
  font-size: 1.8rem;
  letter-spacing: 1.2px;
  color: #ffc107; /* Golden color for the logo */
  text-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
}

.navbar-brand {
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.1); /* Slight zoom effect */
}

/* Nav link styles */
.nav-link {
  color: #f8f9fa;
  font-weight: 500;
  transition: color 0.3s ease, background-color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.nav-link:hover {
  color: #ffc107; /* Golden color on hover */
  background-color: rgba(255, 255, 255, 0.2); /* Subtle background effect */
}

.nav-link.active {
  color: #ffc107; /* Highlight active link */
  font-weight: bold;
  text-decoration: underline;
  background-color: rgba(255, 255, 255, 0.15); /* Subtle highlight background */
}

/* Responsive design */
@media (max-width: 768px) {
  .navbar {
    text-align: center;
    padding: 0.8rem 1rem;
  }
  .navbar-nav {
    margin-top: 1rem;
  }
  .nav-link {
    margin: 0.5rem 0;
  }
}
</style>
