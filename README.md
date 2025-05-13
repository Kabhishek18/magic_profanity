
# 🧙‍♂️ Magic Profanity

`magic_profanity` is a Python library for detecting and censoring profanity in text using customizable word lists and character mappings. It supports **English** and **Hinglish**, with enhanced features including:

- Sentiment Analysis
- Text Enhancement Suggestions

---

## 📦 Installation

```bash
pip install magic_profanity
```

### Requirements

- Python 3+
- `nltk` (for sentiment analysis)

---

## 🚀 Usage

### 🔁 Importing the Library

```python
from magic_profanity import ProfanityFilter
```

---

### 🛠️ Initializing the Profanity Filter

Basic initialization:

```python
profanity_filter = ProfanityFilter()
```

With sentiment analysis:

```python
profanity_filter = ProfanityFilter(enable_sentiment=True)
```

With all features enabled:

```python
profanity_filter = ProfanityFilter(
    enable_sentiment=True,
    sentiment_options={
        'custom_threshold': {'positive': 0.1, 'negative': -0.1},
        'preprocess_text': True
    },
    enable_enhancement=True
)
```

---

### 📥 Loading Custom Words

**From a list:**

```python
profanity_filter.load_words(["badword1", "badword2"])
```

**From a file:**

```python
profanity_filter.load_words_from_file("path/to/custom_wordlist.txt")
```

---

### 🔍 Checking for Profanity

```python
text = "This sentence contains a badword1 and a BadWord2."
if profanity_filter.has_profanity(text):
    print("Profanity detected!")
else:
    print("No profanity found.")
```

---

### ❌ Censoring Text

```python
censored_text = profanity_filter.censor_text(text)
print(censored_text)
```

---

### ➕ Adding Custom Words

```python
profanity_filter.add_custom_words(["newbadword1", "newbadword2"])
```

---

### 🔤 Custom Character Mappings

```python
profanity_filter.char_map = {
    "a": ("a", "@", "*", "4"),
    "i": ("i", "*", "l", "1"),
    "o": ("o", "*", "0", "@"),
    # Add more mappings as needed
}
```

---

## 💬 Using Sentiment Analysis

### Basic Sentiment Analysis

```python
text = "This product is amazing! I'm really happy with it."
analysis = profanity_filter.analyze_text(text)

print(f"Censored text: {analysis['censored_text']}")
print(f"Contains profanity: {analysis['contains_profanity']}")
print(f"Sentiment: {analysis['sentiment']['classification']}")
print(f"Sentiment scores: {analysis['sentiment']['scores']}")
```

---

### 🔎 Detailed Sentiment Analysis

```python
text = "This product is absolutely amazing! I couldn't be happier with it."
analysis = profanity_filter.analyze_text(text, detailed=True)

print(f"Sentiment: {analysis['sentiment']['classification']}")
print(f"Confidence: {analysis['sentiment']['confidence']}")
print(f"Emotion indicators: {analysis['sentiment']['emotion_indicators']}")
```

---

## ✨ Getting Text Enhancement Suggestions

```python
text = "This damn product is terrible. I hate how it always breaks!"
analysis = profanity_filter.analyze_text(text)

# Print enhancement suggestions
suggestions = analysis['enhancement_suggestions']
for category, items in suggestions.items():
    if category != 'overall_recommendations' and items:
        print(f"\n{category.replace('_', ' ').title()}:")
        for suggestion in items:
            print(f"- Replace '{suggestion['original']}' with: {', '.join(suggestion['suggestions'])}")
    elif category == 'overall_recommendations' and items:
        print("\nOverall recommendations:")
        for recommendation in items:
            print(f"- {recommendation}")
```

---

## 🧪 Complete Example

```python
# Initialize with all features enabled
# Initialize with all features enabled
profanity_filter = ProfanityFilter(
    enable_sentiment=True,
    sentiment_options={
        'custom_threshold': {'positive': 0.1, 'negative': -0.1},
        'preprocess_text': True
    },
    enable_enhancement=True
)

# Analyze text
text = "This damn product is terrible. I hate how it always breaks!"
analysis = profanity_filter.analyze_text(text, detailed=True)

# Use the analysis results
print(f"Censored: {analysis['censored_text']}")
print(f"Sentiment: {analysis['sentiment']['classification']} ({analysis['sentiment']['confidence']})")

if analysis['enhancement_suggestions']['politeness_improvements']:
    print("\nSuggested improvements:")
    for suggestion in analysis['enhancement_suggestions']['politeness_improvements']:
        print(f"- Replace '{suggestion['original']}' with: {', '.join(suggestion['suggestions'])}")

```

---

## 🤝 Contributing

Contributions are welcome!  
Please open an issue or pull request on [GitHub](https://github.com/Kabhishek18/magic_profanity/) with your suggestions, bug reports, or enhancements.

---

## 📄 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.
