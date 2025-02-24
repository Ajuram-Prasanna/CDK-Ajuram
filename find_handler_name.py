import ast
import os

def find_functions_in_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        
    tree = ast.parse(file_content)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    return functions



for folder in os.listdir('lambdas'):
    folder_path = os.path.join('lambdas', folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith('.py'):
                source_file_path = os.path.join(folder_path, file)
                functions = find_functions_in_file(source_file_path)
                print(f"Functions found in {source_file_path}: {functions}")
