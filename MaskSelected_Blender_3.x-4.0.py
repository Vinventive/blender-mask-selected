bl_info = {
    "name": "Mask from Edit Mode Selection",
    "description": "Sets the paint mask for selected vertices in edit mode",
    "author": "Vinventive",
    "version": (1, 0),
    "blender": ((3, 0, 0)),
    "location": "Sculpt Mode > Mask",
    "category": "Sculpting"
}
# Feel free to tidy up the code, I'm not a programmer, I just wanted this functionality and couldn't find it anywhere :p

import bpy
import bmesh
import numpy as np

class MaskSelected(bpy.types.Operator):
    """Mask selected vertices in Sculpt Mode"""
    bl_idname = "sculpt.mask_selected"
    bl_label = "Mask from Edit Mode Selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = bpy.context.active_object
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        # Push the operator's undo step onto the undo stack
        bpy.ops.ed.undo_push(message="Mask Selected")

        #get selected verts
        v_sel = np.empty(len(obj.data.vertices), dtype=bool)
        obj.data.vertices.foreach_get('select', v_sel)
        sel_idx, = np.where(v_sel)

        #get custom data layer paint_mask
        mask_layer= bm.verts.layers.paint_mask.verify()
        bm.verts.ensure_lookup_table()

        #set every selected vert to mask_value
        mask_value = 1.0
        for idx in sel_idx:
            bm.verts[idx][mask_layer]=mask_value

        bm.to_mesh(obj.data)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}
    
    def undo(self, context):
        obj = bpy.context.active_object
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        #get custom data layer paint_mask
        mask_layer= bm.verts.layers.paint_mask.verify()
        bm.verts.ensure_lookup_table()

        #clear paint mask
        for v in bm.verts:
            v[mask_layer] = 0.0

        bm.to_mesh(obj.data)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}

def draw_mask_selected(self, context):
    self.layout.operator("sculpt.mask_selected")

def register():
    bpy.utils.register_class(MaskSelected)
    bpy.types.VIEW3D_MT_mask.prepend(draw_mask_selected)

def unregister():
    bpy.utils.unregister_class(MaskSelected)
    bpy.types.VIEW3D_MT_mask.remove(draw_mask_selected)

if __name__ == "__main__":
    register()
