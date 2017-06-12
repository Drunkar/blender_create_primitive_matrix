import re
import bpy
from bpy.props import StringProperty

bl_info = {
    "name": "create primitive matrix",
    "author": "Drunkar",
    "version": (0, 1),
    "blender": (2, 7, 8),
    "location": "3D View, Ctrl + Alt + M",
    "description": "Create and put primitives in matrix.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


addon_keymaps = []


class SeectionSplitter(bpy.types.Operator):

    bl_idname = "object.create_primitive_matrix"
    bl_label = "create primitive matrix"
    bl_description = "Create and put primitives in matrix."
    bl_options = {"REGISTER", "UNDO"}

    # main
    def execute(self, context):
        x = context.scene.primitive_matrix_location[0]
        y = context.scene.primitive_matrix_location[1]
        dx = context.scene.primitive_matrix_distances[0]
        dy = context.scene.primitive_matrix_distances[1]
        for i in range(context.scene.primitive_matrix_num_objects[0]):
            for j in range(context.scene.primitive_matrix_num_objects[1]):
                if context.scene.primitive_matrix_primitive_type == "cube":
                    bpy.ops.mesh.primitive_cube_add(
                        location=(x + i * dx, y + j * dy, 0.0))
                elif context.scene.primitive_matrix_primitive_type == "ico_sphere":
                    bpy.ops.mesh.primitive_ico_sphere_add(
                        subdivisions=2, size=0.2, location=(x + i * dx, y + j * dy, 0.0))
        return {"FINISHED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.prop(context.scene, "primitive_matrix_primitive_type")
        col.prop(context.scene, "primitive_matrix_location")
        col.prop(context.scene, "primitive_matrix_num_objects")
        col.prop(context.scene, "primitive_matrix_distances")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.operator(SeectionSplitter.bl_idname)


def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # register shortcut in 3d view
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        # key
        kmi = km.keymap_items.new(
            idname=SeectionSplitter.bl_idname,
            type="M",
            value="PRESS",
            shift=False,
            ctrl=True,
            alt=True)
        # register to shortcut key list
        addon_keymaps.append((km, kmi))


def unregister_shortcut():
    for km, kmi in addon_keymaps:
        # unregister shortcut key
        km.keymap_items.remove(kmi)
    # clear shortcut key list
    addon_keymaps.clear()


def register():
    unregister_shortcut()
    bpy.utils.register_module(__name__)
    bpy.types.Scene.primitive_matrix_primitive_type\
        = bpy.props.EnumProperty(name="objType",
                                 description="Object Type",
                                 default="ico_sphere",
                                 items=[
                                     ("cube", "Cube", ""),
                                     ("ico_sphere", "Ico Sphere", "")
                                 ])
    bpy.types.Scene.primitive_matrix_location\
        = bpy.props.FloatVectorProperty(name="Location", size=3,
                                        subtype="XYZ", default=(0.0, 0.0, 0.0),
                                        description="Start point.")
    bpy.types.Scene.primitive_matrix_num_objects\
        = bpy.props.IntVectorProperty(name="num_objects", size=2, subtype="XYZ",
                                      default=(2, 3), description="Row and column")
    bpy.types.Scene.primitive_matrix_distances\
        = bpy.props.FloatVectorProperty(name="distance", size=2, subtype="XYZ",
                                        default=(2.0, 2.0), description="Distance between objects")
    register_shortcut()


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.primitive_matrix_primitive_type
    del bpy.types.Scene.primitive_matrix_location
    del bpy.types.Scene.primitive_matrix_num_objects
    del bpy.types.Scene.primitive_matrix_distances


if __name__ == "__main__":
    register()
