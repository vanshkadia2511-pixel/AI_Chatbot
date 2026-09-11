/**
 * StudyBuddy - Interactive Quiz Engine
 * Tracks score, provides instant pedagogical feedback and gamification
 */

import { appState, actions, events } from './state.js';
import { soundFx, spawnXPFloat } from './animations.js';

const QUIZ_BANKS = {
  "Mathematics & Statistics": [
    {
      id: "math_1",
      topic: "Linear Regression",
      question: "In simple linear regression (y = mx + b), what does the slope 'm' represent?",
      options: [
        "The predicted value of y when x = 0",
        "The rate of change in y for each one-unit increase in x",
        "The total variance of the dataset",
        "The correlation coefficient squared"
      ],
      correctIndex: 1,
      explanation: "The slope 'm' measures the sensitivity or rate of change in the dependent variable (y) per unit change in the independent variable (x)."
    },
    {
      id: "math_2",
      topic: "Calculus",
      question: "What is the derivative of f(x) = x³ - 4x + 7 with respect to x?",
      options: [
        "3x² - 4",
        "3x² + 7",
        "x² - 4",
        "3x³ - 4x"
      ],
      correctIndex: 0,
      explanation: "Using the power rule d/dx[xⁿ] = n·xⁿ⁻¹, the derivative of x³ is 3x², the derivative of -4x is -4, and constants differentiate to 0."
    },
    {
      id: "math_3",
      topic: "Probability",
      question: "If two events A and B are independent, what is P(A ∩ B)?",
      options: [
        "P(A) + P(B)",
        "P(A) / P(B)",
        "P(A) · P(B)",
        "1 - P(A)"
      ],
      correctIndex: 2,
      explanation: "By definition of statistical independence, the joint probability of two independent events occurring together is the product of their individual probabilities."
    }
  ],
  "Computer Science": [
    {
      id: "cs_1",
      topic: "Algorithms",
      question: "What is the average time complexity of QuickSort?",
      options: [
        "O(n)",
        "O(n log n)",
        "O(n²)",
        "O(log n)"
      ],
      correctIndex: 1,
      explanation: "QuickSort recursively partitions the array with average divide-and-conquer complexity of O(n log n)."
    }
  ]
};

export class QuizEngine {
  constructor(containerElement) {
    this.container = containerElement;
    this.currentQuestionIndex = 0;
    this.activeBank = QUIZ_BANKS["Mathematics & Statistics"];
  }

  startQuiz(subject = appState.subject) {
    this.activeBank = QUIZ_BANKS[subject] || QUIZ_BANKS["Mathematics & Statistics"];
    this.currentQuestionIndex = 0;
    this.renderCurrentQuestion();
  }

  renderCurrentQuestion() {
    if (!this.container) return;

    const q = this.activeBank[this.currentQuestionIndex];
    if (!q) {
      this.renderQuizComplete();
      return;
    }

    const html = `
      <div class="quiz-widget-card" id="active-quiz-widget">
        <div class="quiz-header">
          <span class="quiz-badge">🧩 Quiz Mode</span>
          <span class="quiz-counter">Question ${this.currentQuestionIndex + 1} / ${this.activeBank.length}</span>
        </div>
        <div class="quiz-question-text">${q.question}</div>
        <div class="quiz-options-list">
          ${q.options.map((opt, i) => `
            <button class="quiz-option-btn" data-index="${i}">
              <span class="option-prefix">${String.fromCharCode(65 + i)}</span>
              <span>${opt}</span>
            </button>
          `).join('')}
        </div>
        <div id="quiz-feedback-area"></div>
      </div>
    `;

    this.container.innerHTML = html;

    const buttons = this.container.querySelectorAll('.quiz-option-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const idx = parseInt(btn.getAttribute('data-index'));
        this.evaluateAnswer(idx, q, buttons);
      });
    });
  }

  evaluateAnswer(selectedIndex, question, allButtons) {
    allButtons.forEach(b => b.disabled = true);

    const isCorrect = selectedIndex === question.correctIndex;
    const selectedBtn = allButtons[selectedIndex];
    const correctBtn = allButtons[question.correctIndex];

    if (isCorrect) {
      selectedBtn.classList.add('correct');
      soundFx.playSuccess();
      spawnXPFloat('+15 XP', window.innerWidth - 200, window.innerHeight / 2);
    } else {
      selectedBtn.classList.add('wrong');
      correctBtn.classList.add('correct');
      soundFx.playError();
    }

    actions.recordQuizAnswer(isCorrect);

    const feedbackArea = this.container.querySelector('#quiz-feedback-area');
    feedbackArea.innerHTML = `
      <div class="quiz-feedback-box ${isCorrect ? 'correct' : 'wrong'}">
        <strong>${isCorrect ? '✓ Correct! +15 XP' : '✗ Needs Review'}</strong>
        <p style="margin-top: 4px;">${question.explanation}</p>
        <button class="btn-chat-action" id="btn-next-quiz-q" style="margin-top: 8px; width: 100%; padding: 6px;">
          ${this.currentQuestionIndex < this.activeBank.length - 1 ? 'Next Question →' : 'Complete Quiz 🎉'}
        </button>
      </div>
    `;

    const nextBtn = feedbackArea.querySelector('#btn-next-quiz-q');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        this.currentQuestionIndex++;
        this.renderCurrentQuestion();
      });
    }
  }

  renderQuizComplete() {
    this.container.innerHTML = `
      <div class="quiz-widget-card" style="text-align: center; border-color: var(--color-success);">
        <div style="font-size: 2rem;">🏆</div>
        <div class="quiz-question-text">Quiz Mastery Assessment Complete!</div>
        <p style="font-size: 0.8rem; color: var(--text-secondary);">Score: ${appState.score} / ${appState.totalQuestions} (${appState.quizAccuracy}%)</p>
        <button class="btn-demo-launcher" id="btn-restart-quiz" style="margin: 8px auto 0;">
          Practice Again ↻
        </button>
      </div>
    `;

    const restart = this.container.querySelector('#btn-restart-quiz');
    if (restart) {
      restart.addEventListener('click', () => this.startQuiz());
    }
  }
}
