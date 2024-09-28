import ast
import os
import hashlib
from collections import defaultdict

class DuplicatedCodeDetector(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.code_blocks = defaultdict(list)

    def _hash_code(self, code):
        """Create a hash for the given code block."""
        return hashlib.md5(code.encode('utf-8')).hexdigest()
    
    def extract_code(self, code):
        return code.splitlines()
    
    def generate_code_hash(self, code_block):
        code_lines = code_block[1:]
        code = '\n'.join(code_lines)
        return self._hash_code(code)

    def visit_FunctionDef(self, node):
        code_block = []
        # Convert the function body to a string
        code = ast.get_source_segment(self.source_code, node)
        code_block = self.extract_code(code)
        code_hash = self.generate_code_hash(code_block)
        self.code_blocks[code_hash].append((node.name, node.lineno, code))          
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Optionally, you can also visit class definitions
        self.generic_visit(node)

# def detect_duplicates(file_path):
#     if os.path.isfile(file_path) and file_path.endswith('.py'):
#         with open(file_path, 'r') as f:
#             source_code = f.read()
#             try:
#                 tree = ast.parse(source_code, filename=file_path)
#                 detector = DuplicatedCodeDetector(source_code)
#                 detector.visit(tree)
#             except SyntaxError as e:
#                 print(f"Syntax error in {file_path}: {e}")
#                 return {}

#     return detector.code_blocks

def detect_duplicates(source_code, filename):
    try:
        # Parse the source code into an AST
        tree = ast.parse(source_code, filename=filename)
        detector = DuplicatedCodeDetector(source_code)
        detector.visit(tree)  # Traverse the AST
    except SyntaxError as e:
        print(f"Syntax error in {filename}: {e}")
        return {}

    return detector.code_blocks


def visualize_duplicates(duplicates):
    found = False
    for code_hash, items in duplicates.items():
        if len(items) > 1:  # Only interested in actual duplicates
            found = True
            print(f"Duplicate code block (hash: {code_hash}):")
            for name, lineno, code in items:
                print(f"  - Function: {name} at line {lineno}")
                print(f"    Code:\n{code}\n")

    if not found:
        print("No duplicate code found.")