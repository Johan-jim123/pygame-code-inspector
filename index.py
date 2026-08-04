import ast
from flask import Flask, request, jsonify

app = Flask(__name__)


class CodeChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.score = 100
        self.has_init = False
        self.has_quit = False
        self.has_fps_limit = False

    def visit_Call(self, node):
        # Check for pygame.init()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'init' and getattr(node.func.value, 'id', '') == 'pygame':
                self.has_init = True
            if node.func.attr == 'quit' and getattr(node.func.value, 'id', '') == 'pygame':
                self.has_quit = True
            if node.func.attr == 'tick':
                self.has_fps_limit = True
        self.generic_visit(node)

    def analyze(self, code_str):
        try:
            tree = ast.parse(code_str)
            self.visit(tree)

            if not self.has_init:
                self.issues.append("Missing 'pygame.init()' call.")
                self.score -= 15
            if not self.has_quit:
                self.issues.append("Missing 'pygame.quit()' call.")
                self.score -= 15
            if not self.has_fps_limit:
                self.issues.append("Missing frame rate control ('clock.tick()').")
                self.score -= 10

            self.score = max(0, self.score)

            # Grade assignment
            if self.score >= 90:
                grade = "A 🌟"
            elif self.score >= 75:
                grade = "B 👍"
            elif self.score >= 60:
                grade = "C ⚠️"
            elif self.score >= 40:
                grade = "D ❌"
            else:
                grade = "F 💀"

            return {
                "score": self.score,
                "grade": grade,
                "issues": self.issues if self.issues else ["No major issues found! 🎉"]
            }
        except SyntaxError as e:
            return {"error": f"Syntax Error in code: {str(e)}"}


@app.route('/api/inspect', methods=['POST'])
def inspect():
    data = request.get_json()
    code = data.get('code', '')
    checker = CodeChecker()
    result = checker.analyze(code)
    return jsonify(result)