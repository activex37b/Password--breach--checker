# 🔐 Password Breach Checker

**Password Breach Checker** is a Python-based security tool that helps users ensure their passwords are safe and strong. It checks whether a password has been compromised in known data breaches using the **Have I Been Pwned (HIBP)** API, and also evaluates the **strength** of new passwords using complexity and entropy metrics.

---

## 🚀 Features

- ✅ Checks if a password appears in public data breaches (HIBP API)
- 🔒 Local hashing (k-anonymity model – passwords are never sent in full)
- 🔍 Analyzes password strength based on:
  - Length
  - Use of uppercase/lowercase letters
  - Numbers and special characters
  - Entropy estimation
- 🧠 Provides feedback: `Weak`, `Moderate`, or `Strong` password

---

## 🛠️ How It Works

```bash
$ python3 password Breach Checker.py

