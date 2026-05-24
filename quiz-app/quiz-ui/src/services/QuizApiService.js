import axios from 'axios';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null) {
    const token = localStorage.getItem('adminToken'); // Retrieve the token from localStorage
    const headers = {
      'Content-Type': 'application/json',
    };

    // Add the token to the headers if it exists
    if (token) {
      headers.authorization = `Bearer ${token}`;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error('API Error:', error.response ? error.response.data : error.message);
        throw error; // Re-throw the error to handle it in the calling function
      });
  },


  // Fetch quiz info
  async getQuizInfo() {
    return this.call('get', 'quiz-info');
  },

  async getTotalQuestions() {
    const response = await this.call('get', 'quiz-info');
    return response.data.size; // Assuming the backend returns { size: X, scores: [...] }
  },

  async getQuestionByPosition(position) {
    return this.call('get', `questions?position=${position}`);
  },
  async getQuestionById(questionId) {
    return this.call('get', `questions/${questionId}`);
  },

  // Delete a question by its ID
  async deleteQuestion(questionId) {
    return this.call('delete', `questions/${questionId}`);
  },
  async deleteAllParticipations() {
    return this.call('delete', 'participations/all');
  },

  // Delete all questions
  async deleteAllQuestions() {
    return this.call('delete', 'questions/all');
  },
  
  // Add a new question
  async addQuestion(questionData) {
    return this.call('post', 'questions', questionData);
  },
  async submitQuiz(payload) {
    return this.call('post', '/participations', payload);
  },
  // Update a question
  async updateQuestion(questionId, questionData) {
    return this.call('put', `questions/${questionId}`, questionData);
  },
 
  // Fetch a question by position
  async getQuestion(position) {
    return this.call('get', `questions?position=${position}`);
  },

  // Submit quiz answers
  async submitAnswers(playerName, answers) {
    return this.call('post', '/participations', { playerName, answers });
  },

  // Login
  async login(password) {
    return this.call('post', '/login', { password });
  },
};