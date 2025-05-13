# magic_profanity/enhancement.py
import re


class TextEnhancer:
    def __init__(self):
        """Initialize the text enhancer with improvement patterns."""
        # Patterns for text improvement (regex pattern -> suggested replacement)
        self.improvement_patterns = {
            # Profanity replacements - these can be gentler alternatives
            r'\b(damn|darn)\b': ['darn', 'oh my', 'goodness'],
            r'\b(stupid|idiot|dumb)\b': ['unwise', 'not smart', 'mistaken'],

            # Negative phrases to make more constructive
            r'\b(hate|despise)\b': ['dislike', 'not fond of', 'would prefer not to'],
            r'\b(terrible|awful|horrible)\b': ['not great', 'could be improved', 'less than ideal'],

            # Aggressive tones to make more assertive but respectful
            r'\byou need to\b': ['I would suggest', 'perhaps you could', 'it might help to'],
            r'\byou should\b': ['one option is to', 'you might consider', 'it could be beneficial to'],

            # Absolute statements to make more balanced
            r'\balways\b': ['often', 'frequently', 'in most cases'],
            r'\bnever\b': ['rarely', 'infrequently', 'seldom'],

            # Vague expressions to make more specific
            r'\ba lot\b': ['significantly', 'considerably', 'to a great extent'],
            r'\bvery\b': ['notably', 'particularly', 'exceptionally'],

            # Passive voice patterns (simplified detection)
            r'\bis being\b': ['[active voice recommendation]'],
            r'\bwas done\b': ['[active voice recommendation]']
        }

    def suggest_improvements(self, text):
        """
        Analyze text and suggest improvements.

        Args:
            text (str): The text to analyze

        Returns:
            dict: A dictionary of suggestion categories and specific suggestions
        """
        suggestions = {
            'tone_improvements': [],
            'clarity_improvements': [],
            'politeness_improvements': []
        }

        # Check for improvement patterns
        for pattern, replacements in self.improvement_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                original = match.group(0)
                suggestion = {
                    'original': original,
                    'context': self._get_context(text, match.start(), match.end()),
                    'suggestions': replacements,
                    'position': (match.start(), match.end())
                }

                # Categorize the suggestion
                if any(word in pattern.lower() for word in ['damn', 'stupid', 'idiot', 'dumb', 'hate']):
                    suggestions['politeness_improvements'].append(suggestion)
                elif any(word in pattern.lower() for word in ['always', 'never', 'very', 'a lot']):
                    suggestions['clarity_improvements'].append(suggestion)
                else:
                    suggestions['tone_improvements'].append(suggestion)

        # Add overall text improvement suggestions
        suggestions['overall_recommendations'] = self._get_overall_recommendations(text)

        return suggestions

    def _get_context(self, text, start, end, context_size=20):
        """Get the context surrounding a match."""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)

        return "..." + text[context_start:start] + "[" + text[start:end] + "]" + text[end:context_end] + "..."

    def _get_overall_recommendations(self, text):
        """Generate overall text recommendations."""
        recommendations = []

        # Check text length
        if len(text) > 500:
            recommendations.append("Consider making your message more concise for better readability")

        # Check sentence length
        sentences = re.split(r'[.!?]+', text)
        long_sentences = [s for s in sentences if len(s.split()) > 20]
        if long_sentences:
            recommendations.append("Consider breaking up long sentences to improve clarity")

        # Check for repeated words
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1

        repeated = [word for word, freq in word_freq.items() if
                    freq > 3 and word not in ['this', 'that', 'with', 'from']]
        if repeated:
            recommendations.append(f"Consider using synonyms for frequently used words: {', '.join(repeated)}")

        return recommendations