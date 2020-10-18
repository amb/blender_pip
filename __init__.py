bl_info = {
    "name": "Python Module Manager",
    "author": "ambi",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Here",
    "description": "Manage Python modules inside Blender with PIP",
    "warning": "",
    "wiki_url": "",
    "support": "COMMUNITY",
    "tracker_url": "https://github.com/amb/blender_pip/issues",
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


def run_pip_command(*cmds):
    cmds = [c for c in cmds if c is not None]
    print("Running PIP command", cmds, "with", python_bin)
    command = [python_bin, "-m", "pip", *cmds]
    # if bpy.context.scene.pip_user_flag:
    #     command.append("--user")

    subprocess.run(command, check=True, shell=True)


class PMM_OT_PIPInstall(bpy.types.Operator):
    bl_idname = "pmm.pip_install"
    bl_label = "Install packages"
    bl_description = "Install PIP packages"

    def execute(self, context):
        run_pip_command(
            "install",
            bpy.context.scene.pip_module_name,
            "--user" if bpy.context.scene.pip_user_flag else None,
        )
        return {"FINISHED"}


class PMM_OT_PIPRemove(bpy.types.Operator):
    bl_idname = "pmm.pip_remove"
    bl_label = "Remove packages"
    bl_description = "Remove PIP packages"

    def execute(self, context):
        run_pip_command("uninstall", bpy.context.scene.pip_module_name, "-y")
        return {"FINISHED"}


class PMM_OT_PIPList(bpy.types.Operator):
    bl_idname = "pmm.pip_list"
    bl_label = "List packages"
    bl_description = "List installed PIP packages"

    def execute(self, context):
        run_pip_command("list")
        return {"FINISHED"}


class PMM_OT_EnsurePIP(bpy.types.Operator):
    bl_idname = "pmm.ensure_pip"
    bl_label = "Ensure PIP"
    bl_description = "Try to ensure PIP exists"

    def execute(self, context):
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

        row = layout.row()
        row.prop(bpy.context.scene, "pip_module_name", text="Module name(s)")
        row.operator(PMM_OT_PIPInstall.bl_idname, text="Install")
        row.operator(PMM_OT_PIPRemove.bl_idname, text="Remove")


classes = (
    PMM_AddonPreferences,
    PMM_OT_EnsurePIP,
    PMM_OT_PIPList,
    PMM_OT_PIPInstall,
    PMM_OT_PIPRemove,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.pip_user_flag = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.pip_module_name = bpy.props.StringProperty()


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.pip_user_flag
    del bpy.types.Scene.pip_module_name
