import os

rootDir = os.path.abspath(os.path.dirname(__file__))
var = 'sdf'
print(os.path.join(rootDir, f"static/csc/{var}.html"))
