import ast
import streamlit as st
from code_checker import CodeChecker  # Imports your AST inspector class!

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Pygame AST Code Inspector", page_icon="🔍", layout="centered"
)

st.title("🔍 Pygame Code Inspector & Health Analyzer")
st.write(
    "Paste your Pygame code below to check for missing drivers, infinite"
    " loops, memory leaks, and get an overall code grade!"
)

# --- USER INPUT AREA ---
default_code = """import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

player_img = pygame.image.load("player.png")
unused_sound = pygame.mixer.Sound("unused.wav")

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(player_img, (100, 100))
    pygame.display.flip()

# Missing pygame.quit()!
"""

code_input = st.text_area(
    "Paste your Python code here:", value=default_code, height=280
)

# --- RUN ANALYSIS ---
if st.button("🚀 Inspect Code", type="primary"):
    try:
        # Parse and run AST Inspector
        tree = ast.parse(code_input)
        checker = CodeChecker()
        checker.visit(tree)

        # Calculate score and unused assets internally
        unused_assets = checker.loaded_assets - checker.used_variables
        score = 100
        if not checker.pygame_init_found:
            score -= 15
        if not checker.pygame_quit_found:
            score -= 15
        if not checker.fps_limiter_found:
            score -= 20
        score -= len(checker.unmonitored_while_loops) * 20
        if checker.hardcoded_resolutions:
            score -= 10
        score -= len(unused_assets) * 5
        score = max(0, score)

        # Determine Grade
        if score >= 90:
            grade, color = "A 🌟", "green"
        elif score >= 75:
            grade, color = "B 👍", "blue"
        elif score >= 60:
            grade, color = "C ⚠️", "orange"
        elif score >= 40:
            grade, color = "D ❌", "red"
        else:
            grade, color = "F 💥", "red"

        # Display Health Score Banner
        st.divider()
        st.metric(label="Overall Code Health Score", value=f"{score} / 100")
        st.subheader(f"Final Grade: :{color}[{grade}]")

        # Breakdown Checklist
        st.divider()
        st.subheader("📋 Inspection Report")

        # Driver checks
        col1, col2 = st.columns(2)
        with col1:
            if checker.pygame_init_found:
                st.success("`pygame.init()` Status: PASS")
            else:
                st.error("`pygame.init()` Status: FAIL (Missing)")

        with col2:
            if checker.pygame_quit_found:
                st.success("`pygame.quit()` Status: PASS")
            else:
                st.error("`pygame.quit()` Status: FAIL (Missing)")

        # Performance & Loops
        if checker.fps_limiter_found:
            st.success("FPS Limiter (`.tick()`): PASS")
        else:
            st.error("FPS Limiter (`.tick()`): FAIL (Missing)")

        if not checker.unmonitored_while_loops:
            st.success("Infinite Loops Check: PASS (All loops monitored)")
        else:
            st.error(
                "Infinite Loops Check: FAIL (Unmonitored loop on line(s):"
                f" {checker.unmonitored_while_loops})"
            )

        # Style & Memory
        if not checker.hardcoded_resolutions:
            st.success("Resolution Practice: PASS (No raw hardcoded tuples)")
        else:
            st.warning(
                "Resolution Practice: WARNING (Hardcoded screen size on line(s):"
                f" {checker.hardcoded_resolutions})"
            )

        if not unused_assets:
            st.success("Memory Efficiency: PASS (No unused assets sitting in RAM)")
        else:
            st.warning(
                f"Memory Efficiency: WARNING (Unused assets in RAM: {unused_assets})"
            )

    except SyntaxError as e:
        st.error(f"❌ Syntax Error on line {e.lineno}: Your code has invalid Python syntax!")
    except Exception as e:
        st.error(f"❌ Error analyzing code: {e}")