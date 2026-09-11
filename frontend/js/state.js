/**
 * StudyBuddy - Central Application State & Reactive Event Hub
 * SDG 4 — Quality Education AI Tutor Interface
 */

class EventEmitter {
  constructor() {
    this.events = {};
  }

  on(event, listener) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
    return () => this.off(event, listener);
  }

  off(event, listener) {
    if (!this.events[event]) return;
    this.events[event] = this.events[event].filter(l => l !== listener);
  }

  emit(event, data) {
    if (!this.events[event]) return;
    this.events[event].forEach(listener => {
      try {
        listener(data);
      } catch (err) {
        console.error(`Error in event listener for "${event}":`, err);
      }
    });
  }
}

export const events = new EventEmitter();

export const appState = {
  // Curriculum Context
  subject: "Mathematics & Statistics",
  difficulty: "Intermediate", // Beginner, Intermediate, Advanced, Exam-Focused
  mode: "Study Mode", // Study Mode, Explain Mode, Quiz Mode, Exam Mode
  topic: "Linear Regression",

  // Gamification & Progress
  xp: 450,
  streak: 5,
  progress: 78, // 0 - 100%
  score: 8,
  totalQuestions: 10,
  quizAccuracy: 80,

  // Learning Profile Mastery
  mastery: {
    "Math Foundations": 90,
    "Linear Regression": 78,
    "Probability": 65,
    "Statistics": 42
  },

  // Conversation & AI Status
  messages: [],
  isThinking: false,
  connectionStatus: "connected", // connected, connecting, offline, error

  // Exam & Quiz Engine State
  activeQuiz: null,
  examTimeRemaining: 1200, // 20 minutes in seconds
  examActive: false,

  // Settings
  soundEnabled: true,
  qualityTier: "HIGH" // HIGH, MEDIUM, LOW
};

// State Mutator Actions
export const actions = {
  setSubject(subject) {
    appState.subject = subject;
    events.emit("subjectChanged", subject);
  },

  setDifficulty(difficulty) {
    const oldDiff = appState.difficulty;
    appState.difficulty = difficulty;
    events.emit("difficultyChanged", { from: oldDiff, to: difficulty });
  },

  setMode(mode) {
    const oldMode = appState.mode;
    appState.mode = mode;
    events.emit("modeChanged", { from: oldMode, to: mode });
  },

  setTopic(topic) {
    appState.topic = topic;
    events.emit("topicSelected", topic);
  },

  setThinking(isThinking) {
    appState.isThinking = isThinking;
    events.emit("thinkingChanged", isThinking);
  },

  addMessage(message) {
    appState.messages.push(message);
    events.emit("messageAdded", message);
  },

  addXP(points) {
    appState.xp += points;
    events.emit("xpGained", { points, total: appState.xp });
  },

  recordQuizAnswer(isCorrect) {
    if (isCorrect) {
      appState.score += 1;
      appState.streak += 1;
      appState.xp += 15;
      appState.progress = Math.min(100, appState.progress + 4);
    } else {
      appState.streak = 0;
      appState.progress = Math.max(0, appState.progress - 2);
    }
    appState.totalQuestions += 1;
    appState.quizAccuracy = Math.round((appState.score / Math.max(1, appState.totalQuestions)) * 100);

    events.emit("quizEvaluated", {
      isCorrect,
      score: appState.score,
      total: appState.totalQuestions,
      streak: appState.streak,
      progress: appState.progress
    });
  },

  updateProgress(newProgress) {
    appState.progress = Math.max(0, Math.min(100, newProgress));
    events.emit("progressChanged", appState.progress);
  },

  setQuality(tier) {
    appState.qualityTier = tier;
    events.emit("qualityChanged", tier);
  },

  toggleSound() {
    appState.soundEnabled = !appState.soundEnabled;
    events.emit("soundToggled", appState.soundEnabled);
  }
};
