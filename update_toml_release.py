import toml
import sys

data = toml.load("pyproject.toml") 

# Modify field
version = sys.argv[1]
version = version.replace("v", "")
data['project']['version']=version

# To use the dump function, you need to open the file in 'write' mode
# It did not work if I just specify file location like in load
f = open("pyproject.toml",'w')
toml.dump(data, f)
f.close()
print(f"Dataplane python project updated to {version}")