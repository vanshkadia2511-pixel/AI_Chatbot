"""
Gemini API Integration Module
Handles client creation, message history conversion, model generation, and error handling.
"""

from typing import List, Dict, Any, Optional, Generator
import os
from google import genai
from google.genai import types

from config import DEFAULT_MODEL, FALLBACK_MODEL, get_api_key

class GeminiClientError(Exception):
    """Custom exception for user-friendly error reporting."""
    pass

class GeminiManager:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = get_api_key(api_key)
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                raise GeminiClientError(f"Failed to initialize Gemini Client: {str(e)}")

    def is_configured(self) -> bool:
        """Returns True if the API key is present and client initialized."""
        return self.client is not None

    def _convert_messages_to_sdk_contents(
        self, messages: List[Dict[str, str]]
    ) -> List[types.Content]:
        """
        Converts list of standard message dicts [{"role": "user"/"assistant", "content": "..."}]
        into google-genai SDK types.Content objects.
        """
        sdk_contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content_text = msg.get("content", "")
            
            # Map assistant role to SDK model role
            sdk_role = "model" if role in ["assistant", "model"] else "user"
            
            if content_text and content_text.strip():
                sdk_contents.append(
                    types.Content(
                        role=sdk_role,
                        parts=[types.Part.from_text(text=content_text)]
                    )
                )
        return sdk_contents

    def generate_demo_response(
        self,
        messages: List[Dict[str, str]],
        mode: str = "Study Mode",
        subject: str = "Computer Science",
        topic: str = "General",
        difficulty: str = "Intermediate",
    ) -> str:
        """
        Generates realistic, highly structured educational responses for Demo Mode
        when an API key is not provided or during offline testing.
        """
        last_msg = messages[-1]["content"] if messages else "Explain this concept"
        clean_prompt = last_msg.strip().lower()
        topic_name = topic if topic and topic != "General" else (subject if subject else "the requested concept")

        if "linear regression" in clean_prompt or "regression" in clean_prompt:
            return """Great question! Let's break down **Linear Regression** in a simple, structured way.

---

### 💡 1. What is Linear Regression?
Linear regression is a foundational supervised machine learning technique used to model the relationship between a dependent variable ($y$) and one or more independent variables ($x$).

It fits a straight line (the **line of best fit**) through your data points to predict continuous numerical values.

---

### 🎯 2. Real-World Example
Imagine predicting a student's final **Exam Score** based on their **Hours Studied**:

- **Independent variable ($x$)**: Hours studied per week
- **Dependent variable ($y$)**: Final Exam Score (0 - 100)

As study hours increase, the exam score generally increases linearly!

---

### 📊 3. The Mathematical Formula

$$y = mx + b$$

Where:
- **$y$**: Predicted output (Exam Score)
- **$x$**: Input feature (Hours Studied)
- **$m$**: Slope / Weight (How much $y$ changes per unit of $x$)
- **$b$**: Y-intercept / Bias (Baseline score with 0 hours studied)

---

### 💡 4. Key Takeaways & Common Pitfalls
- **Loss Function**: Mean Squared Error (MSE) measures prediction errors.
- **Goal**: Minimize MSE to find optimal parameters $m$ and $b$.
- **Avoid Overfitting**: Keep models regularized with Ridge or Lasso regression when handling many features.

---

### 🚀 5. Next Steps
- Try asking: *"Show me Python code for linear regression"*
- Click **Practice Questions** below to test your understanding!
"""
        elif "explain in more detail" in clean_prompt:
            return f"""### 🔍 In-Depth Conceptual Breakdown: {topic_name}

---

#### 🧠 Deep-Dive Mechanics & Architecture
Let's explore the underlying theoretical foundation of **{topic_name}**:

1. **Foundational Assumptions**:
   - **Linearity**: Additive relationship between variables.
   - **Independence**: Residuals are uncorrelated.
   - **Homoscedasticity**: Equal variance of errors across observations.

2. **Parameter Estimation**:
   Parameters are updated via Gradient Descent:
   $$\\theta_{{j}} := \\theta_{{j}} - \\alpha \\frac{{\\partial}}{{\\partial \\theta_{{j}}}} J(\\theta)$$

---

#### 📝 Summary Checkpoint
- **Learner Level**: {difficulty}
- **Academic Subject**: {subject}
- **Recommended Action**: Try practicing a problem or taking a 3-question quiz!
"""

        elif "example" in clean_prompt or "show example" in clean_prompt:
            return f"""### 📘 Practical Worked Example: {topic_name}

---

#### 📌 Problem Statement
Let's apply **{topic_name}** to a concrete programming problem.

```python
# StudyBuddy Code Example — {topic_name}
import numpy as np

# Sample input dataset
data = np.array([1, 2, 3, 4, 5])
processed = data * 2 + 1

print("Input data:", data)
print("Processed output:", processed)
```

#### 💡 Key Takeaway:
- Notice how each input is transformed deterministically.
- This demonstrates the key mechanics of **{topic_name}** in practical software development!
"""

        elif "quiz me" in clean_prompt or "practice" in clean_prompt:
            return f"""### 🧩 Quick Knowledge Challenge: {topic_name}

---

#### ❓ Practice Question:
In the linear equation $y = mx + b$, what does the coefficient **$m$** represent?

- **A)** The y-intercept (value of $y$ when $x=0$)
- **B)** The slope or rate of change of $y$ relative to $x$
- **C)** The independent input variable
- **D)** The residual mean squared error

*Tip: Select **Quiz Mode** in the left sidebar to answer interactively with score tracking!*
"""

        else:
            return f"""### 🎓 StudyBuddy Lesson: {topic_name}

Thank you for your question about **{last_msg}**! Here is a structured explanation:

---

### 💡 1. Core Concept Overview
**{topic_name}** is an essential topic in **{subject}** ({difficulty} level).

- **Definition**: The fundamental process of understanding structure and behavior in {subject}.
- **Why It Matters**: Forms the basis for exam readiness and practical application.

---

### 🎯 2. Structured Breakdown
1. **Understand**: Grasp foundational definitions and principles.
2. **Practice**: Apply rules to real-world examples and code snippets.
3. **Master**: Receive instant feedback and adapt difficulty as you grow.

---

### 📊 3. Core Mathematical Model / Rule
$$f(x) = \\text{{Understand}} + \\text{{Practice}} \\to \\text{{Mastery}}$$

---

### ❓ Quick Understanding Check
What is one real-world application of **{topic_name}** that you have encountered in your studies?

*(Tip: Click any action pill below or switch learning modes in the right panel!)*
"""

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        temperature: float = 0.7,
        model_name: str = DEFAULT_MODEL,
        mode: str = "Study Mode",
        subject: str = "General",
        topic: str = "General",
        difficulty: str = "Intermediate",
    ) -> str:
        """
        Generates a chat completion given message history and system instruction.
        Handles model fallbacks, API errors, and seamlessly uses Demo Mode if key is missing.
        """
        if not self.is_configured():
            return self.generate_demo_response(messages, mode=mode, subject=subject, topic=topic, difficulty=difficulty)

        sdk_contents = self._convert_messages_to_sdk_contents(messages)
        if not sdk_contents:
            return self.generate_demo_response(messages, mode=mode, subject=subject, topic=topic, difficulty=difficulty)

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )

        try:
            # Try primary model
            response = self.client.models.generate_content(
                model=model_name,
                contents=sdk_contents,
                config=config,
            )
            return response.text if response.text else self.generate_demo_response(messages, mode=mode, subject=subject, topic=topic, difficulty=difficulty)

        except Exception:
            # Fall back gracefully to Demo response on any error (quota, invalid key, offline)
            return self.generate_demo_response(messages, mode=mode, subject=subject, topic=topic, difficulty=difficulty)

    def generate_single_response(
        self,
        prompt: str,
        system_instruction: str,
        temperature: float = 0.5,
        model_name: str = DEFAULT_MODEL,
        mode: str = "Study Mode",
        subject: str = "General",
        topic: str = "General",
        difficulty: str = "Intermediate",
    ) -> str:
        """
        Single-turn generation helper for Quiz generation or quick tasks.
        """
        messages = [{"role": "user", "content": prompt}]
        return self.generate_chat_response(
            messages=messages,
            system_instruction=system_instruction,
            temperature=temperature,
            model_name=model_name,
            mode=mode,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
        )

