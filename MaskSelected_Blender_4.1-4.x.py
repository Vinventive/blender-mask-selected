bl_info = {
    "name": "Mask from Edit Mode Selection",
    "description": "Sets the paint mask for selected vertices in Edit Mode",
    "author": "Vinventive",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "Sculpt Mode > Mask",
    "category": "Sculpting",
}

import bpy
import bmesh

class MaskSelected(bpy.types.Operator):
    """Mask selected vertices in Sculpt Mode"""
    bl_idname = "sculpt.mask_selected"
    bl_label = "Mask from Edit Mode Selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        # Ensure the active object is a mesh
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh")
            return {'CANCELLED'}
        
        # Store the current mode to return to it later
        initial_mode = obj.mode
        
        # Switch to Edit Mode to access vertex selection
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Access the BMesh representation
        bm = bmesh.from_edit_mesh(obj.data)
        
        # Ensure the '.sculpt_mask' attribute exists
        mask_layer = bm.verts.layers.float.get('.sculpt_mask')
        if mask_layer is None:
            mask_layer = bm.verts.layers.float.new('.sculpt_mask')
        
        # Set mask value for selected vertices
        mask_value = 1.0
        for vert in bm.verts:
            if vert.select:
                vert[mask_layer] = mask_value
        
        # Update the mesh to apply changes
        bmesh.update_edit_mesh(obj.data)
        
        # Return to the initial mode
        bpy.ops.object.mode_set(mode=initial_mode)
        
        # If the initial mode was not Sculpt Mode, switch to Sculpt Mode
        if initial_mode != 'SCULPT':
            bpy.ops.object.mode_set(mode='SCULPT')
        
        # Redraw the viewport to reflect changes
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        return {'FINISHED'}

def draw_mask_selected(self, context):
    self.layout.operator("sculpt.mask_selected")

def register():
    bpy.utils.register_class(MaskSelected)
    bpy.types.VIEW3D_MT_mask.append(draw_mask_selected)

def unregister():
    bpy.utils.unregister_class(MaskSelected)
    bpy.types.VIEW3D_MT_mask.remove(draw_mask_selected)

if __name__ == "__main__":
    register()
