export default {
  clear() {
    // Supprimer toutes les données de participation dans le localStorage
    window.localStorage.removeItem('playerName');
    window.localStorage.removeItem('participationScore');
  },
  savePlayerName(playerName) {
    // Sauvegarder le nom du joueur
    window.localStorage.setItem('playerName', playerName);
  },
  getPlayerName() {
    // Récupérer le nom du joueur
    return window.localStorage.getItem('playerName');
  },
  saveParticipationScore(participationScore) {
    // Sauvegarder le score de participation
    window.localStorage.setItem(
      'participationScore',
      JSON.stringify(participationScore)
    );
  },
  getParticipationScore() {
    // Récupérer le score de participation
    const score = window.localStorage.getItem('participationScore');
    return score ? JSON.parse(score) : null;
  },
};
