# Pygame  Code Inspector 
An automated static analysis tool and web application designed to help Pygame developers detect architectural anti-patterns, performance bottlenecks, and memory leaks without executing untrusted code.

<img width="1147" height="909" alt="Screenshot 2026-07-26 215136" src="https://github.com/user-attachments/assets/2abb3c39-0c29-49f8-90a7-7fb7f072c440" />

## Overview
Coding is hard, especially when you don't know what you are doing wrong. My project helps you identify the main problems such as frame rate caps, unmonitored infinite loops, displays, etc., and makes sure that your code runs smoothly without frying your computer.

Pygame AST Code Inspector leverages Python's built-in Abstract Syntax Tree (`ast`) module to inspect game scripts in real time, serving as an automated quality-of-life code health analyzer.

---

## Key Quality of Life (QoL) Improvements

1. One-Click Test Presets:
Preset buttons in the interface let you click Load Clean Sample or Load Buggy Sample to run test code immediately without needing to manually copy-paste snippets.

2. Hardware Strain and CPU Safeguard Warnings:
The analyzer catches unmonitored infinite loops and missing frame rate limits (`clock.tick()`), explicitly warning developers if a script risks 100% CPU usage or desktop window freezes.

3. Actionable Fix Guidance:
Lists exact architectural issues (such as missing `pygame.init()`, unhandled `QUIT` events, or unclosed windows) along with specific code fixes needed to fix the script.

Try it!: 
https://pygamecoden-inspector.vercel.app/

## Features

* **Safe Sandbox Launch:** Runs the submitted Pygame code automatically in a safe test window.
* **Crash & Error Detection:** Checks if the game opens properly without crashing or throwing errors.
* **Screen & Render Verification:** Verifies that the graphics actually draw and update on the screen.
* **Clean Exit Handling:** Tests if the game closes cleanly when you click the "X" button.
* **Instant Pass/Fail Verdict:** Displays a clear Pass or Fail report showing what worked or what broke.

## Running it locally
Got Python installed? Here’s how to get it running on your machine:

Step 1: Clone the repo and jump into the folder:
```bash
git clone [https://github.com/Johan-jim123/pygame-code-inspector.git](https://github.com/Johan-jim123/pygame-code-inspector.git)
cd pygame-code-inspector
```

Step 2: Set up a virtual environment (so your global Python stays clean):
* **Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
* **Mac or Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Step 3: Install Pygame and dependencies:
```bash
pip install -r requirements.txt
```

Step 4: Run the checker:
```bash
python main.py test_script.py
```

## How it works:
* Loads the code
* Runs it in an isolated sandbox so your main terminal won't take any damage
* Tracks whether our window opens, Pygame initialises, frames are rendering, Pygame quits cleanly, etc.
* Outputs result
