import argparse
import ast
import sys


class CodeChecker(ast.NodeVisitor):

    def __init__(self):
        self.try_except_count = 0
        self.unmonitored_while_loops = []
        self.fps_limiter_found = False
        self.pygame_init_found = False
        self.pygame_quit_found = False
        self.hardcoded_resolutions = []
        self.loaded_assets = set()
        self.used_variables = set()

    def visit_Try(self, node):
        self.try_except_count += 1
        self.generic_visit(node)

    def visit_While(self, node):
        has_event_handling = any(
            isinstance(child, ast.Attribute) and child.attr in ("get", "pump")
            for child in ast.walk(node)
        )
        has_break = any(
            isinstance(child, ast.Break) for child in ast.walk(node)
        )

        if not has_event_handling and not has_break:
            self.unmonitored_while_loops.append(node.lineno)

        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "tick":
                self.fps_limiter_found = True

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "pygame"
            ):
                if node.func.attr == "init":
                    self.pygame_init_found = True
                elif node.func.attr == "quit":
                    self.pygame_quit_found = True

            if (
                isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "display"
            ):
                if node.func.attr == "set_mode":
                    if node.args and isinstance(
                        node.args[0], (ast.Tuple, ast.List)
                    ):
                        has_numbers = any(
                            isinstance(elt, ast.Constant)
                            and isinstance(elt.value, (int, float))
                            for elt in node.args[0].elts
                        )
                        if has_numbers:
                            if node.lineno not in self.hardcoded_resolutions:
                                self.hardcoded_resolutions.append(node.lineno)

        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr in ("load", "Sound"):
                    target = node.targets[0]
                    if isinstance(target, ast.Name):
                        self.loaded_assets.add(target.id)

        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_variables.add(node.id)
        self.generic_visit(node)

    def generate_report(self, file_path):
        unused_assets = self.loaded_assets - self.used_variables

        score = 100

        if not self.pygame_init_found:
            score -= 15
        if not self.pygame_quit_found:
            score -= 15
        if not self.fps_limiter_found:
            score -= 20

        score -= len(self.unmonitored_while_loops) * 20

        if self.hardcoded_resolutions:
            score -= 10

        score -= len(unused_assets) * 5
        score = max(0, score)

        if score >= 90:
            grade = "A 🌟"
        elif score >= 75:
            grade = "B 👍"
        elif score >= 60:
            grade = "C ⚠️"
        elif score >= 40:
            grade = "D ❌"
        else:
            grade = "F 💥"

        print("\n" + "=" * 52)
        print(f"       🔍 CODE INSPECTOR REPORT: {file_path}")
        print("=" * 52)
        print("-" * 52)
        print(f"OVERALL CODE HEALTH SCORE:  {score}/100 (Grade: {grade})")
        print("-" * 52 + "\n")

        init_status = "[PASS]" if self.pygame_init_found else "[FAIL] Missing"
        quit_status = "[PASS]" if self.pygame_quit_found else "[FAIL] Missing"
        print(f"pygame.init() Status:       {init_status}")
        print(f"pygame.quit() Status:       {quit_status}")

        tick_status = (
            "[PASS]" if self.fps_limiter_found else "[FAIL] Missing (.tick)"
        )
        print(f"FPS Limiter (.tick):        {tick_status}")

        if not self.unmonitored_while_loops:
            print("Infinite Loops Check:       [PASS] All loops monitored")
        else:
            print(
                f"Infinite Loops Check:       [FAIL] Unmonitored on line(s)"
                f" {self.unmonitored_while_loops}"
            )

        if not self.hardcoded_resolutions:
            print("Resolution Practice:        [PASS] No raw hardcoded tuples")
        else:
            print(
                f"Resolution Practice:        [WARNING] Hardcoded on line(s)"
                f" {self.hardcoded_resolutions}"
            )

        if not unused_assets:
            print("Memory Efficiency:          [PASS] No unused assets in RAM")
        else:
            print(f"Memory Efficiency:          [WARNING] Unused: {unused_assets}")

        print(
            f"Try/Except Error Blocks:    {self.try_except_count} block(s)"
            " found"
        )
        print("=" * 52 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Static AST Code Inspector for Pygame Projects"
    )
    # Target file argument (defaults to 'Test.py' if you just press run)
    parser.add_argument(
        "file_path",
        nargs="?",
        default="Test.py",
        help="Path to the Python file you want to inspect (e.g. boss_fight.py)",
    )

    args = parser.parse_args()

    try:
        with open(args.file_path, "r", encoding="utf-8") as file:
            code = file.read()

        tree = ast.parse(code)
        checker = CodeChecker()
        checker.visit(tree)
        checker.generate_report(args.file_path)

    except FileNotFoundError:
        print(
            f"❌ Error: Could not find the file '{args.file_path}'. Check the"
            " path!"
        )
    except SyntaxError as e:
        print(
            f"❌ Error: '{args.file_path}' has a Python syntax error on line"
            f" {e.lineno}!"
        )


if __name__ == "__main__":
    main()
