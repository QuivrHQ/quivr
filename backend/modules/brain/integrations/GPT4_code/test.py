import sys

# Assuming the 'modules' directory is at the root level of your project
root_path = "/Users/chloed./Documents/quivr/quivr/backend"
sys.path.insert(0, root_path)


from modules.tools.code_generator import CodeGeneratorTool

code_generator = CodeGeneratorTool()
print(code_generator._run("Using matplotlib, how do i do a scatter plot ?"))
