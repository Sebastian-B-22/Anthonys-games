"""
LEGO Minifigure Knight Sword - Classic Style
Handle fits LEGO minifigure hand (4.5mm diameter)
Total length: ~43mm
Run this in Blender: Scripting tab → paste → Run Script
"""

import bpy
import bmesh

# ── Clear scene ──────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ── Set units to millimetres ─────────────────────────────────
scene = bpy.context.scene
scene.unit_settings.system       = 'METRIC'
scene.unit_settings.scale_length = 0.001   # 1 Blender unit = 1 mm

# ── Helper: move object so its BOTTOM sits at z = bottom_z ──
def sit_at(obj, bottom_z):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)
    obj.location.z = bottom_z - obj.bound_box[0][2]
    bpy.ops.object.transform_apply(location=True)

# ─────────────────────────────────────────────────────────────
# 1. POMMEL  (rounded ball at bottom)
# ─────────────────────────────────────────────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(radius=3, location=(0, 0, 0))
pommel = bpy.context.active_object
pommel.name = "Pommel"
bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)
# sits 0–6 mm
sit_at(pommel, 0)

# ─────────────────────────────────────────────────────────────
# 2. HANDLE  (cylinder, 4.5 mm dia → fits LEGO hand grip)
# ─────────────────────────────────────────────────────────────
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=2.25,   # 4.5 mm diameter
    depth=12,      # 12 mm long
    location=(0, 0, 0)
)
handle = bpy.context.active_object
handle.name = "Handle"
bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)
# sits 6–18 mm
sit_at(handle, 6)

# ─────────────────────────────────────────────────────────────
# 3. CROSSGUARD  (wide flat bar)
# ─────────────────────────────────────────────────────────────
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
guard = bpy.context.active_object
guard.name = "Crossguard"
guard.scale = (6, 1.5, 1.5)   # 12 mm wide, 3 mm deep, 3 mm tall
bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)
# sits 18–21 mm
sit_at(guard, 18)

# ─────────────────────────────────────────────────────────────
# 4. BLADE  (tapered flat slab — classic straight sword)
# ─────────────────────────────────────────────────────────────
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
blade = bpy.context.active_object
blade.name = "Blade"
blade.scale = (2, 0.75, 11)   # 4 mm wide, 1.5 mm thick, 22 mm half-height
bpy.ops.object.transform_apply(scale=True, location=True, rotation=True)

# Taper the top 4 vertices to a point (tip of sword)
bm = bmesh.new()
bm.from_mesh(blade.data)
bm.verts.ensure_lookup_table()

top_z = max(v.co.z for v in bm.verts)   # find the tip end
for v in bm.verts:
    if v.co.z >= top_z - 0.01:          # top face vertices
        v.co.x = 0                       # collapse X → point
        v.co.y = 0                       # collapse Y → point

bm.to_mesh(blade.data)
blade.data.update()
bm.free()

# sits 21–43 mm
sit_at(blade, 21)

# ─────────────────────────────────────────────────────────────
# 5. JOIN all parts into one mesh
# ─────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='DESELECT')
for obj in [pommel, handle, guard, blade]:
    obj.select_set(True)
bpy.context.view_layer.objects.active = blade
bpy.ops.object.join()

sword = bpy.context.active_object
sword.name = "LEGO_Knight_Sword"

# ─────────────────────────────────────────────────────────────
# 6. DONE — report dimensions
# ─────────────────────────────────────────────────────────────
print("=" * 40)
print("✅ LEGO Knight Sword created!")
print("   Total length : ~43 mm")
print("   Handle dia   :  4.5 mm  (fits LEGO hand)")
print("   Blade length : ~22 mm")
print("=" * 40)
print("Next: File → Export → STL → send to Bambu Slicer!")
