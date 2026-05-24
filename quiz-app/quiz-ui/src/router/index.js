import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import dashboard from '../views/dashboard.vue';
import updatequestion from '../views/updatequestion.vue';
import addquestion from '../views/Addquestion.vue';
import NewQuizPage from '../views/NewQuizPage.vue';
import Results from '@/views/Results.vue';
import Questions from '@/views/Questions.vue';
import QuestionsManager from '../views/QuestionsManager.vue';
import AdminPage from '../views/AdminPage.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/quiz',
      redirect: '/new-quiz', // Redirect /quiz to /new-quiz
    },
    {
      path: '/results',
      name: 'results',
      component: Results,
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: NewQuizPage,
    },
    {
      path: '/admin/dashboard',
      name: 'dashboard',
      component: dashboard,
      meta: { requiresAuth: true }, // Protect this route
    },
    
    {
      path: '/admin/add-question',
      name: 'addquestion',
      component: addquestion,
      meta: { requiresAuth: true }, // Protect this route
    },
    {
      path: '/admin/update-question/:id', // Dynamic route with question ID
      name: 'UpdateQuestion',
      component: updatequestion,
      meta: { requiresAuth: true }, // Protect this route if needed
    },
    {
      path: '/questions/:id',
      name: 'Questions',
      component: Questions,
    },
    {
      path: '/questions',
      name: 'QuestionsManager',
      component: QuestionsManager,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: AdminPage,
    },
  ],
});
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('adminToken');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'AdminPage' }); // Redirect to login if not authenticated
  } else {
    next(); // Proceed to the route
  }
});

export default router;
