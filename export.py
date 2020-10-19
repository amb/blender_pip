import re
import os

# run this from the addon root, not from inside bpy_amb

addon_name = None
print("Running export...")

# try:
#     print("Current zip version:", [i for i in os.listdir(".") if i.endswith(".zip")][0])
# except IndexError:
#     print(".zip doesn't exist yet")

with open("__init__.py", "r") as f:
    data = f.read()
    m = re.search('"version": (?P<version>\(.+\))', data)
    version_number = tuple(m.group("version")[1:-1].split(", "))
    m = re.search('"name": "(?P<name>.+)"', data)
    addon_name = "".join(m.group("name"))

    # result = eval(compile(data, '', 'exec'))
    # print(dir(result))

from pathlib import Path

dir_path = Path.cwd().stem
addon_name = addon_name.replace(" ", "_")
version_number = ".".join(version_number)
print("name: {}, version:{}".format(addon_name, version_number))
command = (
    "7z a {}_{}.{} ../{}/"
    ' -xr!"__pycache__"'
    ' -xr!"export"'
    ' -xr!".*"'
    ' -xr!"*.bat"'
    ' -xr!"*.txt"'
    ' -xr!"*.7z"'
    ' -xr!"psutil"'
    ' -xr!"ignored"'
    ' -xr!"export.py"'
    ' -xr!"*.zip"'.format(addon_name, version_number, "zip", dir_path)
)

os.system(command)

print("Finished export.")
