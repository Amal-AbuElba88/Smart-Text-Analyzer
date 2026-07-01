# Smart Text Analyzer 🚀

A powerful and modular Python command-line application designed to analyze textual data and extract deep insights. This project demonstrates the practical application of core **Data Structures** combined with **Natural Language Processing (NLP)** techniques to create an interactive and efficient text analysis tool.

---

## 📌 Features
* **Smart Autocompletion:** Prefix-based word suggestions as you type.
* **Next-Word Prediction:** Predicts the subsequent word using a Bigram model.
* **Sentence-Level Sentiment Analysis:** Sentiment tracking with context-aware negation handling (e.g., "not good").
* **Keyword Extraction & Word Cloud Prep:** Extracts key terms and calculates frequencies for word clouds.
* **Text Editing with Undo:** Supports word search, replacement, and a full rollback (Undo) system.
* **Text Statistics:** Real-time word and character counts.

---

## 🛠️ Data Structures Breakdown
Choosing the right data structure was key to maintaining optimal performance:
1. **Trie (Prefix Tree):** Used for **Autocompletion** to ensure fast prefix lookups in $O(n)$ time complexity, where $n$ is the prefix length.
2. **Dictionary (Hash Map):** Used for the **Bigram Model (Next Word Prediction)** and frequency counting, achieving $O(1)$ average time complexity.
3. **Sets:** Used for **Sentiment Lexicons** to allow constant-time membership testing for positive/negative words.
4. **Stack (LIFO):** Used for the **Undo Replace** feature to track and revert text history.

---

## 💡 Implementation Challenges & Solutions
* **Challenge:** Managing increasing project complexity with global variables.
  * **Solution:** Refactored the code using Object-Oriented Programming (OOP) by encapsulating state into a `SmartTextAnalyzer` class.
* **Challenge:** Text replacement mistakes could not be reverted.
  * **Solution:** Integrated a Stack structure to push previous text states before any replacement, enabling an efficient 'Undo' functionality.
* **Challenge:** Handling negation in sentiment analysis (e.g., "not happy" scored as positive due to "happy").
  * **Solution:** Implemented context-aware rules to look ahead and invert the sentiment score if preceded by a negation word like 'not'.
* **Challenge:** Maintaining Trie accuracy after text edits or updates.
  * **Solution:** Implemented automatic Trie reconstruction hooks inside `replace_word()` and `undo_last_change()`.

---

## 🧪 Testing & Edge Cases Handled
The application has been thoroughly tested against various scenarios:
* Robust error handling for invalid file paths and menu inputs using `try-except` blocks.
* Complex sentiment analysis phrases (e.g., *"I am not happy"* and *"This is not bad"*).
* Edge cases in autocompletion when entering prefixes that do not exist in the text.
* Reverting sequential replacements using the Undo stack.

---

## 📄 Project Context & Documentation
* **Institution:** University College of Applied Sciences (UCAS)
* **Course:** Data Structures Course Project
* **Instructor:** Eng. Abd-Elkarem Abu Samra
* **Developer:** Amal Ahmed Abu Elba
* **Project Report:** You can view the comprehensive project report directly in this repository: [`DS-project.pdf`](./DS-project.pdf)
