import ast
import os
import hashlib
from collections import defaultdict
from duplicates import *

class CodeSmellDetector(ast.NodeVisitor):
    def __init__(self):
        self.long_methods = []
        self.god_classes = []
        self.duplicated_code = defaultdict(list)
        self.large_param_methods = []

        # Set thresholds
        self.method_length_threshold = 10
        self.class_method_count_threshold = 10
        self.class_attribute_count_threshold = 10
        self.class_length_threshold = 20
        self.param_count_threshold = 5

    def visit_FunctionDef(self, node):
        # Check for Long Method
        if len(node.body) > self.method_length_threshold:
            self.long_methods.append(node.name)

        # Check for Large Parameter List
        if len(node.args.args) > self.param_count_threshold:
            self.large_param_methods.append(node.name)

        self.generic_visit(node)

    def check_method_count(self, method_count):
        return method_count > self.class_method_count_threshold
    
    def check_attribute_count(self, attribute_count):
        return attribute_count > self.class_attribute_count_threshold
    
    def check_class_length(self, class_length):
        return class_length > self.class_length_threshold

    def visit_ClassDef(self, node):
        # Check for God Class
        method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
        attribute_count = len([n for n in node.body if isinstance(n, ast.Assign)])

        if self.check_method_count(method_count) or self.check_attribute_count(attribute_count) or self.check_class_length(len(node.body)):
            self.god_classes.append(node.name)

        self.generic_visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)



# def detect_code_smells(file):
#     detector = CodeSmellDetector()

#     if file.filename.endswith('.py'):
#         with open(file_path, 'r') as f:
#             try:
#                 tree = ast.parse(f.read(), filename=file_path)
#                 # print(ast.dump(tree))
#                 detector.visit(tree)
#             except SyntaxError as e:
#                 print(f"Syntax error in {file_path}: {e}")

#     return {
#         'Long Methods': detector.long_methods,
#         'God Classes': detector.god_classes,
#         'Large Parameter Methods': detector.large_param_methods,
#         'Duplicated Code': detector.duplicated_code,  
#     }

def detect_code_smells(source_code, filename):
    detector = CodeSmellDetector()

    try:
        tree = ast.parse(source_code, filename=filename)  # Parse the source code
        detector.visit(tree)  # Traverse the AST
    except SyntaxError as e:
        print(f"Syntax error in {filename}: {e}")
        return {'error': f"Syntax error in {filename}: {e}"}
    
    return {
        'Long Methods': detector.long_methods,
        'God Classes': detector.god_classes,
        'Large Parameter Methods': detector.large_param_methods,
    }

def visualize_results(smells):
    for smell, items in smells.items():
        if items:  # Check if there are any detected items
            print(f"{smell}:")
            for item in items:
                if isinstance(item, tuple) and len(item) == 2:
                    name, lineno = item
                    print(f"  - {name} at line {lineno}")
                else:
                    print(f"  - {item}")


# Example usage
if __name__ == "__main__":
    file_to_check = '.\smelly.py'
    smells = detect_code_smells(file_to_check)
    visualize_results(smells)
    visualize_duplicates(detect_duplicates(file_to_check))

    
