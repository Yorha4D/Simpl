# Example of a group that edits a single property
# using the predefined gizmo arrow.
#
# Usage: Select a light in the 3D view and drag the arrow at it's rear
# to change it's energy value.
#
import bpy
from bpy.types import (
    GizmoGroup,
)


class MyLightWidgetGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_light_test"
    bl_label = "Test Light Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'MESH')

    def setup(self, context):
        # Arrow gizmo has one 'offset' property we can assign to the light energy.
        ob = context.object
        gz = self.gizmos.new("GIZMO_GT_arrow_3d")
        gz.target_set_prop("offset", ob, "up_limits")

        gz.matrix_basis = ob.matrix_world.normalized()
        gz.draw_style = 'BOX'

        gz.color = 1.0, 0.5, 0.0
        gz.alpha = 0.5

        gz.color_highlight = 1.0, 0.5, 1.0
        gz.alpha_highlight = 0.5

        self.energy_gizmo = gz

    def refresh(self, context):
        ob = context.object
        gz = self.energy_gizmo
        gz.matrix_basis = ob.matrix_world.normalized()


def active_mod():
    context = bpy.context
    obj = context.object
    mod = obj.modifiers.active if obj else None
    if mod and mod.type == "SIMPLE_DEFORM":
        return mod


def get_prop(self):
    mod = active_mod()
    if mod:
        return mod.limits[1]

    return -1


def set_prop(self, value):
    mod = active_mod()
    if mod:
        mod.limits[1] = value


bpy.types.Object.up_limits = bpy.props.FloatProperty(get=get_prop, set=set_prop)
bpy.utils.register_class(MyLightWidgetGroup)
