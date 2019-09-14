import re
import bpy
from bpy.props import StringProperty

bl_info = {
    "name": "create primitive matrix",
    "author": "Drunkar",
    "version": (0, 4),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Primitive in matrix, Ctrl + Alt + M",
    "description": "Create and put primitives in matrix.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


addon_keymaps = []


class CreatePrimitiveMatrix(bpy.types.Operator):

    bl_idname = "object.create_primitive_matrix"
    bl_label = "create primitive in matrix"
    bl_description = "Create and put primitives in matrix."
    bl_options = {"REGISTER", "UNDO"}

    # main
    def execute(self, context):
        x = context.scene.primitive_matrix_location[0]
        y = context.scene.primitive_matrix_location[1]
        dx = context.scene.primitive_matrix_distances[0]
        dy = context.scene.primitive_matrix_distances[1]
        count = 1
        for i in range(context.scene.primitive_matrix_num_objects[0]):
            for j in range(context.scene.primitive_matrix_num_objects[1]):
                if context.scene.primitive_matrix_primitive_type == "cube":
                    bpy.ops.mesh.primitive_cube_add(
                        location=(x + i * dx, y + j * dy, 0.0))
                elif context.scene.primitive_matrix_primitive_type == "ico_sphere":
                    bpy.ops.mesh.primitive_ico_sphere_add(
                        subdivisions=2, radius=0.6, location=(x + i * dx, y + j * dy, 0.0))
                # set name
                bpy.context.object.name = context.scene.primitive_matrix_name_prefix + \
                    ("{0:0" + str(context.scene.primitive_matrix_name_zero_padding) + \
                    "d}").format(count)
                count += 1
        return {"FINISHED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.prop(context.scene, "primitive_matrix_primitive_type")
        col.prop(context.scene, "primitive_matrix_location")
        col.prop(context.scene, "primitive_matrix_num_objects")
        col.prop(context.scene, "primitive_matrix_distances")
        col.prop(context.scene, "primitive_matrix_name_prefix")
        col.prop(context.scene, "primitive_matrix_name_zero_padding")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.operator(CreatePrimitiveMatrix.bl_idname, text="Primitive in Matrix")


def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # register shortcut in 3d view
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        # key
        kmi = km.keymap_items.new(
            idname=CreatePrimitiveMatrix.bl_idname,
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


classes = (
    CreatePrimitiveMatrix,
)


def register():
    unregister_shortcut()
    for cls in classes:
        bpy.utils.register_class(cls)
    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_mesh_add.append(menu_func)
    else:
        bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
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
    bpy.types.Scene.primitive_matrix_name_prefix\
        = bpy.props.StringProperty(
            name="name_prefix",
            description="name before number",
            default="OBJ_")
    bpy.types.Scene.primitive_matrix_name_zero_padding\
        = bpy.props.IntProperty(
            name="name_zero_padding_num",
            description="number of zero padding of the object name",
            min=0,
            default=3)
    register_shortcut()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_mesh_add.remove(menu_func)
    else:
        bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Scene.primitive_matrix_primitive_type
    del bpy.types.Scene.primitive_matrix_location
    del bpy.types.Scene.primitive_matrix_num_objects
    del bpy.types.Scene.primitive_matrix_distances
    del bpy.types.Scene.primitive_matrix_name_prefix
    del bpy.types.Scene.primitive_matrix_name_zero_padding


if __name__ == "__main__":
    register()
