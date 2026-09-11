/**
 * StudyBuddy - Adaptive Learning Controller
 * Visualizes difficulty adjustments, depth adaptation, and mastery metrics
 */

import { appState, actions, events } from './state.js';
import { soundFx } from './animations.js';

export class AdaptiveLearningController {
  constructor(toastElement) {
    this.toast = toastElement;
    this.bindEvents();
  }

  bindEvents() {
    events.on('difficultyChanged', ({ from, to }) => {
      this.showAdaptationNotification(from, to);
      soundFx.playDifficultyChange();
    });

    events.on('quizEvaluated', () => {
      this.updateMasteryUI();
    });
  }

  showAdaptationNotification(fromLevel, toLevel) {
    if (!this.toast) return;

    let details = "✓ Balanced concept analogies & formulas";
    if (toLevel === 'Beginner') {
      details = "✓ Intuitive real-world analogies • Plain language • Gentle foundation";
    } else if (toLevel === 'Advanced') {
      details = "✓ High analytical depth • Mathematical formulations • Deep theory";
    } else if (toLevel === 'Exam-Focused') {
      details = "✓ High-yield exam prep • Common pitfalls • Model answer criteria";
    }

    this.toast.innerHTML = `
      <div class="adaptation-toast-icon">⚡</div>
      <div class="adaptation-toast-content">
        <div class="adaptation-toast-title">LEVEL ADAPTATION: ${fromLevel} → ${toLevel}</div>
        <div class="adaptation-toast-desc">${details}</div>
      </div>
    `;

    this.toast.classList.add('show');
    setTimeout(() => {
      this.toast.classList.remove('show');
    }, 3800);
  }

  updateMasteryUI() {
    // Update DOM mastery progress bars
    const strongBar = document.querySelector('#mastery-strong-bar');
    const improvingBar = document.querySelector('#mastery-improving-bar');
    const reviewBar = document.querySelector('#mastery-review-bar');

    if (strongBar) strongBar.style.width = `${Math.min(100, appState.progress)}%`;
    if (improvingBar) improvingBar.style.width = `${Math.min(100, appState.quizAccuracy)}%`;
  }
}
