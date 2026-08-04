# 🔍 Pygame AST Code Inspector & Health Analyzer

An automated static analysis tool and web application designed to help Pygame developers detect architectural anti-patterns, performance bottlenecks, and memory leaks without executing untrusted code.

---

## 🌟 Overview

When building Pygame projects, silent bugs—such as missing frame rate caps, unmonitored infinite loops, unhandled display teardowns, and dangling audio assets—frequently cause high CPU usage or system crashes. 

**Pygame AST Code Inspector** leverages Python's built-in Abstract Syntax Tree (`ast`) module to inspect game scripts in real time, serving as an automated quality-of-life code health analyzer.

---

## ✨ Features

* **Lifecycle Verification:** Verifies proper initialization (`pygame.init()`) and clean teardown (`pygame.quit()`).
* **Performance Controls:** Scans for frame-rate limiting calls (`clock.tick()`).
* **Loop Safety Checks:** Detects unmonitored `while` loops lacking event polling (`pygame.event.get()`) or exit flags.
* **Memory Optimization:** Tracks asset loading statements (`pygame.image.load`, `pygame.mixer.Sound`) to highlight unused memory allocations.
* **Hardcoded Resolution Warnings:** Flags raw resolution tuples passed directly into `pygame.display.set_mode()`.
* **Automated Scoring:** Generates an instant Code Health Score (0–100) along with a letter grade (A–F).

---

## 🛠️ Project Architecture
