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

Test code:
```python
import pygame
import random

pygame.init()
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Flying Hot Dog!")
clock = pygame.time.Clock()

# Positions & Variables
dog_x, dog_y = random.randint(50, 400), random.randint(50, 300)
dog_vx, dog_vy = 5, 4
score = 0
font = pygame.font.SysFont("arial", 20, bold=True)

running = True
while running:
    clock.tick(60)
    
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Click detection on the hot dog
            if abs(mx - dog_x) < 30 and abs(my - dog_y) < 15:
                score += 1
                dog_vx = int(dog_vx * -1.2) if abs(dog_vx) < 15 else dog_vx * -1
                dog_vy = int(dog_vy * -1.2) if abs(dog_vy) < 15 else dog_vy * -1

    # Bounce around
    dog_x += dog_vx
    dog_y += dog_vy
    if dog_x < 30 or dog_x > WIDTH - 30: dog_vx *= -1
    if dog_y < 15 or dog_y > HEIGHT - 15: dog_vy *= -1

    # Draw
    screen.fill((30, 30, 30))
    
    # Draw Hot Dog (Bun + Sausage + Mustard)
    pygame.draw.ellipse(screen, (210, 140, 40), (dog_x - 30, dog_y - 15, 60, 30))  # Bun
    pygame.draw.ellipse(screen, (180, 50, 50), (dog_x - 35, dog_y - 8, 70, 16))    # Sausage
    pygame.draw.circle(screen, (255, 220, 0), (dog_x, dog_y), 4)                  # Mustard

    # Score Display
    txt = font.render(f"Hot Dogs Caught: {score}", True, (255, 255, 255))
    screen.blit(txt, (10, 10))

    pygame.display.flip()

pygame.quit()
```

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
