Contributing to magic_profanity

First of all, thank you for considering contributing to magic_profanity! This project aims to provide a fast, flexible, and accurate profanity filtering solution for Python applications.

By participating in this project, you help make the internet a cleaner place.

Code of Conduct

By contributing to this project, you agree to maintain a respectful and inclusive environment. Please be professional and constructive in your communication.

How Can I Contribute?

Reporting Bugs

If you find a bug, please open an issue and include:

A clear and descriptive title.

Steps to reproduce the problem.

Your Python version and magic_profanity version.

Any relevant logs or screenshots.

Suggesting Enhancements

Have an idea for a new feature or a way to improve detection accuracy?

Check existing issues to see if it has been discussed.

Explain the use case and why the enhancement would be beneficial.

If it involves a new detection algorithm, please provide a brief overview of the logic.

Adding New Words or Patterns

Detection of profanity often requires updating word lists or regex patterns.

Ensure that any new words added are categorized correctly.

Avoid adding words that are overly context-dependent unless the library supports specific context-based filtering.

Check for existing "leetspeak" variations to avoid duplicates.

Development Setup

To contribute code, you should set up a local development environment:

Fork the repository and clone it:

git clone [https://github.com/YOUR_USERNAME/magic_profanity.git](https://github.com/YOUR_USERNAME/magic_profanity.git)
cd magic_profanity


Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install development dependencies:

pip install -r requirements.txt
pip install pytest  # If not already in requirements


Create a new branch:

git checkout -b feature/your-feature-name


Pull Request Process

Code Style: Please follow PEP 8 standards.

Tests: Ensure that any new features or bug fixes include corresponding test cases.

Run Tests: Make sure all existing tests pass before submitting:

pytest


Documentation: Update the README.md or any relevant docstrings if your changes affect the API.

Submit: Open a Pull Request against the main branch of the original repository. Provide a clear description of what the PR accomplishes.

Contact

If you have any questions or need further clarification, feel free to reach out via GitHub Issues or contact the maintainer at kabhishek18.com.

Thank you for your contribution!
