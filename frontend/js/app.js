/**
 * StudyBuddy - Main Application Controller
 * Entry point orchestrating 3D Viewport, UI Controls, Chat, Quiz & Demo Flow
 */

import { appState, actions, events } from './state.js';
import { SceneManager } from './scene.js';
import { ChatController } from './chat.js';
import { QuizEngine } from './quiz.js';
import { AdaptiveLearningController } from './adaptive.js';
import { soundFx } from './animations.js';

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize 3D Scene
  const canvas = document.getElementById('three-canvas');
  let sceneManager = null;
  if (canvas) {
    sceneManager = new SceneManager(canvas);
  }

  // 2. DOM Elements
  const chatStream = document.getElementById('chat-messages-stream');
  const chatInput = document.getElementById('chat-input-field');
  const sendBtn = document.getElementById('btn-send-message');
  const toastEl = document.getElementById('adaptation-toast');

  // 3. Subsystem Controllers
  const chatController = new ChatController(chatStream, chatInput, sendBtn);
  const quizEngine = new QuizEngine(chatStream);
  const adaptiveController = new AdaptiveLearningController(toastEl);

  // 4. UI Control Bindings
  initUIBindings(chatController, quizEngine);

  // 5. Judge 30-Second Demo Script Launcher
  const demoBtn = document.getElementById('btn-judge-demo');
  if (demoBtn) {
    demoBtn.addEventListener('click', () => runJudgeDemo(chatController, quizEngine));
  }
});

function initUIBindings(chatController, quizEngine) {
  // Mode Selector Buttons
  const modeButtons = document.querySelectorAll('.mode-btn');
  modeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.getAttribute('data-mode');
      actions.setMode(mode);
      modeButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      soundFx.playModeSwitch();

      // If switching to Quiz Mode, render quiz in stream
      if (mode === 'Quiz Mode') {
        quizEngine.startQuiz();
      }
    });
  });

  // Difficulty Tier Buttons
  const diffButtons = document.querySelectorAll('.diff-tier-btn');
  diffButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const diff = btn.getAttribute('data-tier');
      actions.setDifficulty(diff);
      diffButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // Subject Selector
  const subjectSelect = document.getElementById('subject-selector');
  if (subjectSelect) {
    subjectSelect.addEventListener('change', (e) => {
      actions.setSubject(e.target.value);
    });
  }

  // Sound Toggle
  const soundBtn = document.getElementById('btn-toggle-sound');
  if (soundBtn) {
    soundBtn.addEventListener('click', () => {
      actions.toggleSound();
      soundBtn.innerHTML = appState.soundEnabled ? '🔊' : '🔇';
    });
  }

  // Mobile Drawer Navigation Toggles
  const navControlsBtn = document.getElementById('mob-nav-controls');
  const nav3dBtn = document.getElementById('mob-nav-3d');
  const navChatBtn = document.getElementById('mob-nav-chat');

  const leftPanel = document.querySelector('.left-panel');
  const rightPanel = document.querySelector('.right-panel');

  if (navControlsBtn && leftPanel && rightPanel) {
    navControlsBtn.addEventListener('click', () => {
      leftPanel.classList.toggle('open');
      rightPanel.classList.remove('open');
    });

    nav3dBtn.addEventListener('click', () => {
      leftPanel.classList.remove('open');
      rightPanel.classList.remove('open');
    });

    navChatBtn.addEventListener('click', () => {
      rightPanel.classList.toggle('open');
      leftPanel.classList.remove('open');
    });
  }

  // Reactive Header Metric Updates
  events.on('xpGained', ({ total }) => {
    const xpVal = document.getElementById('header-xp-val');
    if (xpVal) xpVal.textContent = total;
  });

  events.on('quizEvaluated', ({ streak, progress }) => {
    const streakVal = document.getElementById('header-streak-val');
    const progVal = document.getElementById('header-progress-val');
    if (streakVal) streakVal.textContent = streak;
    if (progVal) progVal.textContent = `${progress}%`;
  });
}

/**
 * Executes the exact 30-second Competition-Winning Demo Flow for Judges
 */
async function runJudgeDemo(chatController, quizEngine) {
  const input = document.getElementById('chat-input-field');

  // Step 1: Set to Study Mode & Beginner
  actions.setMode('Study Mode');
  actions.setDifficulty('Beginner');
  document.querySelectorAll('.diff-tier-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tier') === 'Beginner');
  });

  // Step 2: Ask Beginner Question
  input.value = "Teach me linear regression as a beginner.";
  await chatController.handleSendMessage();

  // Step 3: Wait 2.5s, then trigger visible adaptation to Advanced
  setTimeout(async () => {
    actions.setDifficulty('Advanced');
    document.querySelectorAll('.diff-tier-btn').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-tier') === 'Advanced');
    });

    input.value = "Explain linear regression at an advanced mathematical level.";
    await chatController.handleSendMessage();

    // Step 4: Wait 3s, then start Quiz Mode
    setTimeout(() => {
      actions.setMode('Quiz Mode');
      document.querySelectorAll('.mode-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-mode') === 'Quiz Mode');
      });
      quizEngine.startQuiz();
    }, 3200);

  }, 2800);
}
