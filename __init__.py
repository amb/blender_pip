bl_info = {
    "name": "Python Module Manager",
    "author": "ambi",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "Development",
}

__version__ = ".".join(map(str, bl_info["version"]))

# add user site to sys.path
# binaries go to {site.USER_BASE}/bin
# venv notice:
#   https://stackoverflow.com/questions/33412974/
#   how-to-uninstall-a-package-installed-with-pip-install-user/56948334#56948334
import site
import sys
import subprocess

app_path = site.USER_SITE
if app_path not in sys.path:
    sys.path.append(app_path)

import bpy
import numpy as np
import mathutils as mu

python_bin = bpy.app.binary_path_python


class PMM_OT_PIPList(bpy.types.Operator):
    bl_idname = "pmm.pip_list"
    bl_label = "List packages"
    bl_description = "List installed PIP packages"

    def execute(self, context):
        print("[PIP list] Using", python_bin)
        command = [python_bin, "-m", "pip", "list"]
        if bpy.context.scene.pip_user_flag:
            command.append("--user")

        subprocess.run(command, check=True, shell=True)

        return {"FINISHED"}


class PMM_OT_EnsurePIP(bpy.types.Operator):
    bl_idname = "pmm.ensure_pip"
    bl_label = "Ensure PIP"
    bl_description = "Try to ensure PIP exists"

    def execute(self, context):

        import subprocess
        import os
        import platform
        import sys

        # if platform.system() == "Windows":
        #     print("Platform: Windows")
        # elif platform.system() == "Darwin":
        #     print("Platform: Mac")
        # elif platform.system() == "Linux":
        #     print("Platform: Linux")
        # else:
        #     print("!!! Unknown system !!!")

        # print(">>> Site packages:")
        # for path in sys.path:
        #     if os.path.basename(path) in ("dist-packages", "site-packages"):
        #         print(path)

        # import site
        # print(site.getsitepackages())
        # from distutils.sysconfig import get_python_lib
        # print(get_python_lib())

        # import ensurepip
        # ensurepip.bootstrap()
        # print(ensurepip._PIP_VERSION)
        # os.environ.pop("PIP_REQ_TRACKER", None)

        print("[Ensure PIP] Using", python_bin)
        command = [python_bin, "-m", "ensurepip"]
        if bpy.context.scene.pip_user_flag:
            command.append("--user")

        subprocess.run(command, check=True, shell=True)

        return {"FINISHED"}


class PMM_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(bpy.context.scene, "pip_user_flag", text="As local user")
        row.operator(PMM_OT_EnsurePIP.bl_idname, text="Ensure PIP")
        row.operator(PMM_OT_PIPList.bl_idname, text="List")


classes = (PMM_AddonPreferences, PMM_OT_EnsurePIP, PMM_OT_PIPList)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.pip_user_flag = bpy.props.BoolProperty(default=True)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.pip_user_flag
