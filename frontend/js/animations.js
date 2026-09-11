/**
 * StudyBuddy - Audio Feedback & UI Micro-Animation Engine
 * Pure Web Audio API Synthesizer (Zero External Assets)
 */

import { appState } from './state.js';

class AudioSynthesizer {
  constructor() {
    this.ctx = null;
  }

  init() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
  }

  playTone(freq, type = 'sine', duration = 0.15, gainVal = 0.08) {
    if (!appState.soundEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  playClick() {
    this.playTone(600, 'sine', 0.06, 0.04);
  }

  playModeSwitch() {
    this.playTone(440, 'triangle', 0.1, 0.06);
    setTimeout(() => this.playTone(660, 'sine', 0.15, 0.06), 60);
  }

  playDifficultyChange() {
    this.playTone(523.25, 'sine', 0.12, 0.06); // C5
    setTimeout(() => this.playTone(659.25, 'sine', 0.15, 0.06), 80); // E5
  }

  playSuccess() {
    this.playTone(523.25, 'triangle', 0.15, 0.08); // C5
    setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.08), 90); // E5
    setTimeout(() => this.playTone(783.99, 'sine', 0.25, 0.1), 180); // G5
  }

  playError() {
    this.playTone(220, 'sawtooth', 0.2, 0.06);
    setTimeout(() => this.playTone(180, 'sawtooth', 0.25, 0.06), 100);
  }

  playThinking() {
    this.playTone(320, 'sine', 0.08, 0.03);
  }
}

export const soundFx = new AudioSynthesizer();

/**
 * Spawns a floating +XP / notification element in the DOM
 */
export function spawnXPFloat(text, x, y) {
  const el = document.createElement('div');
  el.className = 'xp-float-toast';
  el.textContent = text;
  el.style.left = `${x || window.innerWidth / 2}px`;
  el.style.top = `${y || window.innerHeight / 2}px`;

  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1300);
}
