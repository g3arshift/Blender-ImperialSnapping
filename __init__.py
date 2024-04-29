# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from ctypes import alignment
import bpy
from bpy.props import *
from bpy.types import *
from bpy.ops import *

bl_info = {
    "name": "ImperialSnappingAddon",
    "author": "Gear Shift, Tristan L",
    "version": (2, 0),
    "blender": (4, 1, 1),
    "location": "View3D > N",
    "description": "Imperial Snapping and Scaling",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/g3arshift/Blender-ImperialSnapping/issues",
    "support": "COMMUNITY",
    "category": "3D View",
}

INCH_HALF = 0.500
INCH_QUARTER = 0.250
INCH_EIGHTH = 0.125
INCH_TENTH = 0.100
INCH_SIXTEENTH = 0.0625
INCH_THIRTYSECOND = 0.03125
INCH_SIXTYFOURTH = 0.015625
INCH_HUNDREDTH = 0.010

# Define Set Grid Scale
def set_grid_scale(self, context):       
    for workspace in bpy.data.workspaces:
        for area in workspace.screens[0].areas:
            if area.type == 'VIEW_3D':
                if area.spaces is not None:
                    space = area.spaces.active
                    region = space.region_3d
                    scene = context.scene
                    prop_tool = scene.prop_tool
                    
                    # Define Set Scale
                    def set_scale(val):
                        for area in workspace.screens[0].areas:
                            if area.type == 'VIEW_3D':
                                area.spaces.active.overlay.grid_scale = val

                    unit_scalars = [1609.344, 201.168, 20.1168, 0.9144, 0.3048, 0.0254, 0.0000254]
                    # Imperial Grid Count per Grid Unit
                    dist_base = 12.0
                    # Window Matrix First Element
                    winmat = region.window_matrix[0][0]
                    # 3D View Region sizex and sizey in C
                    region_width = 0
                    region_height = 0
                    # Get 3D View Region Width and Height
                    for a in workspace.screens[0].areas:
                        if a.type == 'VIEW_3D':
                            for r in a.regions:
                                if r.type == 'WINDOW':
                                    region_width = r.width
                                    region_height = r.height
                    # Grid Scale as determined by Blender user input
                    gs = space.overlay.grid_scale
                    # Override Grid Scale so we can keep our ratios consistent
                    gs = 1.000
                    # Divide the Grid Scale by the Scale length incase that is different
                    gs /= scene.unit_settings.scale_length
                    # Populate Grid Steps with the Smallest to Largest Units based on unit_scalars and the grid_scale, largest is multiplied by 10.0 in the background
                    grid_steps = [unit_scalars[6] * gs, unit_scalars[5] * gs, unit_scalars[4] * gs, unit_scalars[3] * gs, unit_scalars[2] * gs, unit_scalars[1] * gs, unit_scalars[0] * gs, unit_scalars[0] * gs * 10.0]
                    # Different than the view_distance, calculated this way in view3d_draw.c
                    region_dist = (dist_base / (region_width * winmat))
                    thou_to_inch_diff = (grid_steps[1] - grid_steps[0])

                    # Determine Grid Scale
                    if not context.scene.prop_tool.imperial_snapping_enabled:
                        gs = 1.000
                        _current_snap_unit = 'None'
                    elif region_dist <= grid_steps[0]:
                        # Thou
                        gs = 1.000
                        _current_snap_unit = 'Thou'
                    elif prop_tool.unit_bool_hundredth_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_hundredth_inch):
                        # Hundredth Inches
                        gs = INCH_HUNDREDTH
                        _current_snap_unit = 'Hundredth'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_hundredth_inch_text_display_offset
                    elif prop_tool.unit_bool_sixtyfourth_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_sixtyfourth_inch):
                        # Sixtyfourth Inches
                        gs = INCH_SIXTYFOURTH
                        _current_snap_unit = 'Sixty-fourth'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_sixtyfourth_inch_text_display_offset
                    elif prop_tool.unit_bool_thirtysecond_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_thirtysecond_inch):
                        # Thirtysecond Inches
                        gs = INCH_THIRTYSECOND
                        _current_snap_unit = 'Thirty-Second'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_thirtysecond_inch_text_display_offset
                    elif prop_tool.unit_bool_sixteenth_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_sixteenth_inch):
                        # Sixteenth Inches
                        gs = INCH_SIXTEENTH
                        _current_snap_unit = 'Sixteenth'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_sixteenth_inch_text_display_offset
                    elif prop_tool.unit_bool_tenth_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_tenth_inch):
                        # Tenth Inches
                        gs = INCH_TENTH
                        _current_snap_unit = 'Tenth'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_tenth_inch_text_display_offset
                    elif prop_tool.unit_bool_eighth_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_eighth_inch):
                        # Eigth Inches
                        gs = INCH_EIGHTH
                        _current_snap_unit = 'Eighth'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_eighth_inch_text_display_offset
                    elif prop_tool.unit_bool_quarter_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_quarter_inch):
                        # Quarter Inches
                        gs = INCH_QUARTER
                        _current_snap_unit = 'Quarter'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_quarter_inch_text_display_offset
                    elif prop_tool.unit_bool_half_inch and (
                            region_dist <= thou_to_inch_diff / prop_tool.unit_int_half_inch):
                        # Half Inches
                        gs = INCH_HALF
                        _current_snap_unit = 'Half'
                        prop_tool.unit_int_current_text_display_offset = prop_tool.unit_int_half_inch_text_display_offset
                    elif region_dist <= grid_steps[1]:
                        # Inches
                        gs = 1.000
                        _current_snap_unit = 'Inches'
                    elif region_dist <= grid_steps[2]:
                        # Feet
                        gs = 1.000
                        _current_snap_unit = 'Feet'
                    elif region_dist <= grid_steps[3]:
                        # Yards
                        gs = 1.000
                        _current_snap_unit = 'Yards'
                    elif region_dist <= grid_steps[4]:
                        # Chains
                        gs = 1.000
                        _current_snap_unit = 'Chains'
                    elif region_dist <= grid_steps[5]:
                        # Furlongs
                        gs = 1.000
                        _current_snap_unit = 'Furlongs'
                    elif region_dist <= grid_steps[6]:
                        # Miles
                        gs = 1.000
                        _current_snap_unit = 'Miles'
                        
                    if bpy.context.window.workspace == workspace:
                        prop_tool.unit_string_current_snap = _current_snap_unit
                    set_scale(gs)


def update_func(self, context):
    set_grid_scale(self, context)
    
def toggle_functionality(self, context):
    prop_tool = context.scene.prop_tool
    if context.scene.prop_tool.imperial_snapping_enabled:
        prop_tool.previous_unit_system = context.scene.unit_settings.system
        context.scene.unit_settings.system = 'IMPERIAL'
        bpy.ops.view3d.modal_operator('INVOKE_DEFAULT')
    else:
        context.scene.unit_settings.system = prop_tool.previous_unit_system
        
        
    update_func(self, context)

class ScaleUnitProperties(bpy.types.PropertyGroup):
    unit_int_half_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=10, update=update_func)
    unit_int_quarter_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=12, update=update_func)
    unit_int_eighth_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=14, update=update_func)
    unit_int_tenth_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=16, update=update_func)
    unit_int_sixteenth_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=18, update=update_func)
    unit_int_thirtysecond_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=20, update=update_func)
    unit_int_sixtyfourth_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=32, update=update_func)
    unit_int_hundredth_inch: bpy.props.IntProperty(name="Visible at ", soft_min=1, soft_max=100, default=40, update=update_func)

    unit_bool_half_inch: bpy.props.BoolProperty(name="Half Inches", default=True, update=update_func)
    unit_bool_quarter_inch: bpy.props.BoolProperty(name="Quarter Inches", default=True, update=update_func)
    unit_bool_eighth_inch: bpy.props.BoolProperty(name="Eighth Inches", default=True, update=update_func)
    unit_bool_tenth_inch: bpy.props.BoolProperty(name="Tenth Inches", default=False, update=update_func)
    unit_bool_sixteenth_inch: bpy.props.BoolProperty(name="Sixteenth Inches", default=True, update=update_func)
    unit_bool_thirtysecond_inch: bpy.props.BoolProperty(name="Thirty-second Inches", default=False, update=update_func)
    unit_bool_sixtyfourth_inch: bpy.props.BoolProperty(name="Sixty-fourth Inches", default=False, update=update_func)
    unit_bool_hundredth_inch: bpy.props.BoolProperty(name="Hundredth Inches", default=False, update=update_func)

    unit_string_current_snap: bpy.props.StringProperty(name="Current Snap Step")
    unit_int_current_text_display_offset: bpy.props.IntProperty(name="Current Offset", default=0)
    
    unit_int_half_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=130)
    unit_int_quarter_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=137)
    unit_int_eighth_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=144)
    unit_int_tenth_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=130)
    unit_int_sixteenth_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=151)
    unit_int_thirtysecond_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=158)
    unit_int_sixtyfourth_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=158)
    unit_int_hundredth_inch_text_display_offset: bpy.props.IntProperty(name="Offset", default=137)
    
    imperial_snapping_enabled: bpy.props.BoolProperty(name="Enabled", default=False, update=toggle_functionality)
    
    previous_unit_system: bpy.props.StringProperty(name="Previous Unit System", default=bpy.context.scene.unit_settings.system)


class ImperialSnappingPanel(bpy.types.Panel):
    """Creates a Panel in the N window"""
    bl_idname = "OBJECT_PT_grid_scale_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Grid Scale Options"
    bl_category = "Grid Scale Options"

    def draw(self, context):
        layout = self.layout
        space = context.area.spaces.active
        region = space.region_3d
        scene = context.scene
        prop_tool = scene.prop_tool

        col = layout.column()
        col.prop(prop_tool, "unit_string_current_snap", emboss=True, text="Snap on")
        col.enabled = False
        
        # Enable snapping
        col = layout.column(heading="Enable Imperial Snapping")
        col.prop(prop_tool, "imperial_snapping_enabled")

        col = layout.column(heading="Fractions Snapping:")
        
        # Check Half Inch
        col.prop(prop_tool, "unit_bool_half_inch")
        if prop_tool.unit_bool_half_inch:
            col.prop(prop_tool, "unit_int_half_inch")
            col.separator()
            
        # Check Quarter Inch
        col.prop(prop_tool, "unit_bool_quarter_inch")
        if prop_tool.unit_bool_quarter_inch:
            col.prop(prop_tool, "unit_int_quarter_inch")
            col.separator()
            
        # Check Eighth Inch
        col.prop(prop_tool, "unit_bool_eighth_inch")
        if prop_tool.unit_bool_eighth_inch:
            col.prop(prop_tool, "unit_int_eighth_inch")
            col.separator()
            
        # Check Tenth Inch
        col.prop(prop_tool, "unit_bool_tenth_inch")
        if prop_tool.unit_bool_tenth_inch:
            col.prop(prop_tool, "unit_int_tenth_inch")
            col.separator()
            
        # Check Sixteenth Inch
        col.prop(prop_tool, "unit_bool_sixteenth_inch")
        if prop_tool.unit_bool_sixteenth_inch:
            col.prop(prop_tool, "unit_int_sixteenth_inch")
            col.separator()
        else:
            col.separator()
        col.label(text="Experimental Options:")
        
        # Check Thirtysecond Inch
        col.prop(prop_tool, "unit_bool_thirtysecond_inch")
        if prop_tool.unit_bool_thirtysecond_inch:
            col.prop(prop_tool, "unit_int_thirtysecond_inch")
            col.separator()
            
        # Check Sixtyfourth Inch
        col.prop(prop_tool, "unit_bool_sixtyfourth_inch")
        if prop_tool.unit_bool_sixtyfourth_inch:
            col.prop(prop_tool, "unit_int_sixtyfourth_inch")
            col.separator()
            
        # Check Hundredth Inch
        col.prop(prop_tool, "unit_bool_hundredth_inch")
        if prop_tool.unit_bool_hundredth_inch:
            col.prop(prop_tool, "unit_int_hundredth_inch")
            col.separator()

class ModalOperator(bpy.types.Operator):
    bl_idname = "view3d.modal_operator"
    bl_label = "Imperial Snapping Addon"

    def modal(self, context, event):

        if not context.scene.prop_tool.imperial_snapping_enabled:
            return{'FINISHED'}
        elif event.type == 'WHEELUPMOUSE' or event.type == 'WHEELDOWNMOUSE':
            set_grid_scale(self, context)
            return {'PASS_THROUGH'}
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

_classes = [ScaleUnitProperties, ImperialSnappingPanel, ModalOperator]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.prop_tool = bpy.props.PointerProperty(type=ScaleUnitProperties)


def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.prop_tool


if __name__ == "__main__":
    register()
    bpy.ops.view3d.imperial_snapping('INVOKE_DEFAULT')
