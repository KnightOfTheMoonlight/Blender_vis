# blender --background --python 11_mesh_visualization.py --render-frame 1 -- </path/to/output/image> <resolution_percentage> <num_samples>

import bpy
import sys
import math
import os
import random
from typing import List, Tuple

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())
import utils

import pdb


def get_random_numbers(length: int) -> List[float]:
    numbers = []
    for i in range(length):
        numbers.append(random.random())
    return numbers


def get_color(x: float) -> Tuple[float, float, float]:
    colors = [
        (0.776470, 0.894117, 0.545098),
        (0.482352, 0.788235, 0.435294),
        (0.137254, 0.603921, 0.231372),
    ]

    a = x * (len(colors) - 1)
    t = a - math.floor(a)
    c0 = colors[math.floor(a)]
    c1 = colors[math.ceil(a)]

    return ((1.0 - t) * c0[0] + t * c1[0], (1.0 - t) * c0[1] + t * c1[1], (1.0 - t) * c0[2] + t * c1[2])


def set_scene_objects() -> bpy.types.Object:
    # Instantiate a floor plane
    utils.create_plane(size=200.0, location=(0.0, 0.0, -0.1))

    # load .obj mesh
    current_object = []
    bpy.ops.import_scene.obj(filepath="demo/1_0_chair_1.000.obj")
#    current_object = list(bpy.data.objects)[0]
    for obj in list(bpy.data.objects):
        if 'chair' in obj.name:
            current_object = obj
    # y upside down
    # current_object.data.
    if current_object == None:
        return None
    
    if len(list(current_object.data.materials)) > 0:
        current_object.data.materials.pop()
    
    # Assign random colors for each triangle
    mesh = current_object.data
    mesh.vertex_colors.new(name='Col')
    random_numbers = get_random_numbers(len(mesh.vertex_colors['Col'].data))
    for index, vertex_color in enumerate(mesh.vertex_colors['Col'].data):
        vertex_color.color = get_color(random_numbers[index // 3]) + tuple([1.0])
        # vertex_color.color = (0.776470, 0.894117, 0.545098, 0.1)

#    # Setup a material with wireframe visualization and per-face colors
#    mat = utils.add_material("Material_Visualization", use_nodes=True, make_node_tree_empty=True)
#    current_object.data.materials.append(mat)

#    output_node = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
#    principled_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
#    rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
#    mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
#    wire_node = mat.node_tree.nodes.new(type='ShaderNodeWireframe')
#    wire_mat_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
#    attrib_node = mat.node_tree.nodes.new(type='ShaderNodeAttribute')

#    attrib_node.attribute_name = 'Col'
#    rgb_node.outputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)

#    mat.node_tree.links.new(attrib_node.outputs['Color'], principled_node.inputs['Base Color'])
#    mat.node_tree.links.new(principled_node.outputs['BSDF'], mix_node.inputs[1])
#    mat.node_tree.links.new(rgb_node.outputs['Color'], wire_mat_node.inputs['Color'])
#    mat.node_tree.links.new(wire_mat_node.outputs['BSDF'], mix_node.inputs[2])
#    mat.node_tree.links.new(wire_node.outputs['Fac'], mix_node.inputs['Fac'])
#    mat.node_tree.links.new(mix_node.outputs['Shader'], output_node.inputs['Surface'])

#    utils.arrange_nodes(mat.node_tree)

    bpy.ops.object.empty_add(location=(0.0, -0.8, 0.0))
    focus_target = bpy.context.object

    return focus_target


# clean the pool
# Select objects by type
for o in bpy.context.scene.objects:
    if o.type == 'MESH' or o.type == 'CAMERA' or o.type == 'LIGHT':
        o.select_set(True)
    else:
        o.select_set(False)
# Call the operator only once
bpy.ops.object.delete()


# pdb.set_trace()
# Args
#output_file_path = str(sys.argv[sys.argv.index('--') + 1])
output_file_path = "demo/cube"
if not os.path.exists(output_file_path):
    os.mkdir(output_file_path)
print("output_file_path is {}".format(output_file_path))
#resolution_percentage = int(sys.argv[sys.argv.index('--') + 2])
resolution_percentage = 100
#num_samples = int(sys.argv[sys.argv.index('--') + 3])
num_samples = 126

# Parameters
hdri_path = "./assets/HDRIs/green_point_park_2k.hdr"

# Scene Building
scene = bpy.data.scenes["Scene"]
world = scene.world

## Reset
utils.clean_objects()

## Object
focus_target_object = set_scene_objects()

if focus_target_object != None:
    ## Camera
    camera_object = utils.create_camera(location=(0, 0, 0.0)) # 0 -10 0

    utils.add_track_to_constraint(camera_object, focus_target_object)
    utils.set_camera_params(camera_object.data, focus_target_object, lens=10, fstop=0.5)

    bpy.ops.object.light_add(type='SUN', align='WORLD', location=(-10, 10, 10))
    bpy.context.object.data.energy = 10

    #pdb.set_trace()
    # Render Setting
#    utils.set_output_properties(scene, resolution_percentage, output_file_path)
#    utils.set_cycles_renderer(scene, camera_object, num_samples, use_transparent_bg=True)
