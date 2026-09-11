/**
 * StudyBuddy - Chat Stream & AI Tutor Interaction Controller
 */

import { appState, actions, events } from './state.js';
import { sendChatMessage } from './api.js';
import { soundFx } from './animations.js';

export class ChatController {
  constructor(streamContainer, inputField, sendBtn) {
    this.stream = streamContainer;
    this.input = inputField;
    this.sendBtn = sendBtn;

    this.bindEvents();
  }

  bindEvents() {
    this.sendBtn.addEventListener('click', () => this.handleSendMessage());

    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.handleSendMessage();
      }
    });

    // Preset prompts from empty state
    document.addEventListener('click', (e) => {
      const promptBtn = e.target.closest('.prompt-suggestion-card, .topic-pill');
      if (promptBtn) {
        const text = promptBtn.getAttribute('data-prompt') || promptBtn.textContent.trim();
        this.input.value = text;
        this.handleSendMessage();
      }
    });
  }

  async handleSendMessage() {
    const text = this.input.value.trim();
    if (!text || appState.isThinking) return;

    this.input.value = '';
    soundFx.playClick();

    // 1. Remove Empty State if present
    const emptyState = this.stream.querySelector('.empty-state-container');
    if (emptyState) emptyState.remove();

    // 2. Append User Message
    this.appendUserMessage(text);

    // 3. Append Thinking Indicator
    const thinkingEl = this.appendThinkingIndicator();

    // 4. Send API Request
    try {
      const reply = await sendChatMessage(text);
      if (thinkingEl) thinkingEl.remove();
      this.appendAIMessage(reply);
      soundFx.playSuccess();
    } catch (err) {
      if (thinkingEl) thinkingEl.remove();
      this.appendAIMessage(`### Something went wrong\nStudyBuddy couldn't reach the learning engine. Please try again.`);
      soundFx.playError();
    }
  }

  appendUserMessage(text) {
    const el = document.createElement('div');
    el.className = 'message-bubble user-message';
    el.innerHTML = `
      <div class="message-meta-header">
        <span class="message-meta-tag">${appState.subject}</span>
        <span class="message-meta-tag">${appState.difficulty}</span>
        <span class="message-meta-tag">${appState.mode}</span>
      </div>
      <div class="message-content-box">${this.escapeHTML(text)}</div>
    `;
    this.stream.appendChild(el);
    this.scrollToBottom();
  }

  appendThinkingIndicator() {
    const el = document.createElement('div');
    el.className = 'ai-thinking-indicator';
    el.id = 'active-thinking-indicator';
    el.innerHTML = `
      <span>StudyBuddy is thinking</span>
      <div class="typing-dots">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    `;
    this.stream.appendChild(el);
    this.scrollToBottom();
    return el;
  }

  appendAIMessage(markdownText) {
    const el = document.createElement('div');
    el.className = 'message-bubble ai-message';
    el.innerHTML = `
      <div class="message-meta-header">
        <span>🤖 StudyBuddy Tutor</span>
      </div>
      <div class="message-content-box">${this.formatEducationalMarkdown(markdownText)}</div>
    `;
    this.stream.appendChild(el);
    this.scrollToBottom();
  }

  formatEducationalMarkdown(md) {
    let html = md;

    // Convert Headers
    html = html.replace(/### (.*?)\n/g, '<h3>$1</h3>');
    html = html.replace(/#### (.*?)\n/g, '<h4>$1</h4>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Code blocks & inline code
    html = html.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Bullet points
    html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>');

    // Line breaks
    html = html.replace(/\n\n/g, '<p></p>');

    return html;
  }

  escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  scrollToBottom() {
    this.stream.scrollTop = this.stream.scrollHeight;
  }
}
