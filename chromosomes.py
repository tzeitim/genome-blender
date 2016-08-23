import bpy  
import numpy
import operator
import csv
import os
from mathutils import Vector  
from math import sqrt

# dictionary of colors on normal RGB
colors = {
    3:[[239,138,98],[247,247,247],[103,169,207]],
    4:[[202,0,32],[244,165,130],[146,197,222],[5,113,176]],
    5:[[202,0,32],[244,165,130],[247,247,247],[146,197,222],[5,113,176]],
    6:[[178,24,43],[239,138,98],[253,219,199],[209,229,240],[103,169,207],[33,102,172]],
    7:[[178,24,43],[239,138,98],[253,219,199],[247,247,247],[209,229,240],[103,169,207],[33,102,172]],
    8:[[178,24,43],[214,96,77],[244,165,130],[253,219,199],[209,229,240],[146,197,222],[67,147,195],[33,102,172]],
    9:[[178,24,43],[214,96,77],[244,165,130],[253,219,199],[247,247,247],[209,229,240],[146,197,222],[67,147,195],[33,102,172]],
    10:[[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[209,229,240],[146,197,222],[67,147,195],[33,102,172],[5,48,97]],
    11:[[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[247,247,247],[209,229,240],[146,197,222],[67,147,195],[33,102,172],[5,48,97]],
    12:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[103,0,31],[253,219,199],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    13:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[103,0,31],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    14:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[49,54,149],[103,0,31],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    15:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[49,54,149],[103,0,31],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    16:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[116,173,209],[49,54,149],[103,0,31],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    17:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[49,54,149],[103,0,31],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    18:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[49,54,149],[103,0,31],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    19:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[49,54,149],[103,0,31],[178,24,43],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    20:[[165,0,38],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    21:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    22:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26]],
    25:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26],[165,0,38],[253,174,97],[69,117,180]],
    30:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26],[165,0,38],[253,174,97],[69,117,180], [103,0,31],[178,24,43],[214,96,77],[209,229,240],[146,197,222]],
    32:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26],[165,0,38],[253,174,97],[69,117,180], [103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[209,229,240],[146,197,222]],
    35:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149],[103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77],[26,26,26],[165,0,38],[253,174,97],[69,117,180], [103,0,31],[178,24,43],[214,96,77],[244,165,130],[253,219,199],[209,229,240],[146,197,222],[67,147,195],[33,102,172],[5,48,97]]
    }

colors_simple = {

                10:[[165,0,38],[215,48,39],[244,109,67],[253,174,97],[254,224,144],[224,243,248],[171,217,233],[116,173,209],[69,117,180],[49,54,149]]
         }
         


         
if(bpy.ops.object.mode_set.poll()):
    bpy.ops.object.mode_set(mode="OBJECT")
    
def clean_tads():
    #bpy.ops.object.select_pattern(pattern="*tad_*")
    #bpy.ops.object.delete(use_global=False)
    for item in bpy.data.objects:
        if(item.name.startswith('tad_')):
            #print("will delete %s" % item)
            item.select =True
    bpy.ops.object.delete()
    for item in bpy.data.curves:
        if(item.name.startswith('tad_')):
            #print("will delete %s" % item)
            bpy.data.curves.remove(item)
            #item.select =True
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)
    #bpy.context.object.data.materials.clear()

def euclideanDistance(a=[4,0,7], b=[-2,1,3]):
    if len(a) == len(b):
        length = len(a)
        distance = 0
        for x in range(length):
            distance += pow((a[x] - b[x]), 2)
        return sqrt(distance)
    else:
        raise IntersectException("vectors have not the same dimensions.")
  
def recalcNormals(objname):
    bpy.data.objects[objname].select = True
    bpy.context.scene.objects.active = bpy.data.objects[objname]
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.normals_make_consistent()
    bpy.ops.object.mode_set(mode="OBJECT")

def ToBezier(objname, handle_type='ALIGNED'):
    bpy.data.objects[objname].select = True
    bpy.context.scene.objects.active = bpy.data.objects[objname]
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.spline_type_set(type='BEZIER')
    bpy.ops.curve.handle_type_set(type=handle_type)
    bpy.ops.object.mode_set(mode="OBJECT")

def bevel_tad(objname, name="tad_circ", radius=0.05):
    tad = bpy.data.objects[objname]
    if not bpy.data.objects.get(name, False):
        print("Didn't find %s, creating it" % name)
        bpy.ops.curve.primitive_nurbs_circle_add(radius=radius, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.context.object.name = name
        bpy.data.objects[name].hide = True
    circ = bpy.data.objects[name]
    tad.data.bevel_object = circ   
    tad.data.splines[0].resolution_u = 4 #3 is low
    tad.data.splines[0].order_u = 3 #6 is high

#================= PATH
def importWalk(filename):
# reads a tab delimited file with 3 columns for x,y,z coords
    with open(filename, 'r', newline='') as csvfile:
        ofile = csv.reader(csvfile, delimiter='\t')
        next(ofile) # <-- skip the x,y,z header
        # this makes a generator of the remaining non-empty lines
        rows = (r for r in ofile if r)
        # this converts the string representation of each line
        # to an x,y,z list, and stores it in the verts list.
        verts = [[float(i) for i in r] for r in rows]
        return verts

def MakeTad(objname, curvename, cList, w=1, bezier=False , consistent_normals=True, bevel=True, type='NURBS', radius=0.03, warp=None):  
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')  
    curvedata.dimensions = '3D'  
    
    objectdata = bpy.data.objects.new(objname, curvedata)  
    objectdata.location = (0,0,0) #object origin  
    bpy.context.scene.objects.link(objectdata)  
  
    polyline = curvedata.splines.new(type)  
    polyline.points.add(len(cList)-1)  
    for num in range(len(cList)):  
        polyline.points[num].co = tuple(cList[num])+(w,)  
  
    # set the extent of influence each point
    #polyline.order_u = len(polyline.points)-1
    polyline.order_u = 6 # seems to be the max
    polyline.order_v = len(polyline.points)-1
    polyline.use_endpoint_u = True
    polyline.use_endpoint_v = True
    
    texture = True
    if(warp == None):
        warp = len(bpy.data.curves[curvename].splines[0].points)/10
      
    if(texture): 
    # create material
        matname = objname+'_colramp_mat'
        gen_materials(matname, steps=len(bpy.data.curves[curvename].splines[0].points), warp=warp)
        tad = bpy.data.objects[objname]
        tadc = bpy.data.curves[curvename]
        tad.select = True
        tad.data.use_uv_as_generated = True
        bpy.context.scene.objects.active = tad
        bpy.ops.object.material_slot_add()
        mat = bpy.data.materials.get(matname)
        print(mat)
        bpy.context.object.active_material_index = 0
        tad.data.materials[0] = mat    
        points = bpy.data.curves[curvename].splines[0].points
        for i in range(int(len(points))):
           #tad = bpy.data.objects[objname]
            #tadc = bpy.data.curves[curvename]
            tad.select = True

            #bpy.ops.material.new()
            #tad.mate
                
                #bpy.context.object.modifiers["tad_hook_000_m"].falloff_type = 'CONSTANT'


    if(bezier):
        print("Converting to BEZIER")
        ToBezier(objname)
    if(consistent_normals):
        recalcNormals(objname)
    if(bevel):
        bevel_tad(objname, radius=radius)
    
def hookTad(tadname='tad_object', curvename='tad_curve', add_new=True, bezier=False, scope = 10, warp = 250, start_f=1, end_f=24*4):
    # bezier bool var defines if the curve will be a bezier curve and it is processed accordingly
    # bezier mode not fully tested
    tad = bpy.data.objects[tadname]
    tadc = bpy.data.curves[curvename]
    tad.select = True
    bpy.context.scene.objects.active = tad
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.select_all(action="DESELECT")
    #bpy.context.tool_settings.mesh_select_mode = (True , False , False) # Assign a tuple of 3 booleans to set Vertex, Edge, Face selection
    bpy.ops.object.mode_set(mode="OBJECT")
    
    #points = tadc.splines[0].bezier_points
    points = tadc.splines[0].points
    
    for i in range(len(points)):
        if(bezier):
            p = tadc.splines[0].bezier_points[i]
        else:
            p = tadc.splines[0].points[i]
        
        if(not add_new):
            bpy.ops.object.mode_set(mode="OBJECT")
            print(p.co)
            print(p.co[0:3])
            bpy.ops.object.add( type='EMPTY', enter_editmode=False, location=p.co[0:3])
            ob = bpy.context.object 
            ob.name = 'tad_hook_'+str(i).zfill(5)
            ob.hide = False

        tad.select = True
        bpy.context.scene.objects.active = tad

        bpy.ops.object.mode_set(mode="EDIT")
        if(bezier):
            p = tadc.splines[0].bezier_points[i]
            p.select_control_point = True
            p.select_left_handle = True
            p.select_right_handle = True
        else:
            p = tadc.splines[0].points[i]
            p.select = True
        
        if(not add_new):
            hook_name = ob.name+'_m'
            tad.modifiers.new(hook_name, type='HOOK')
            bpy.ops.object.hook_assign(modifier=hook_name)
            bpy.ops.object.hook_reset(modifier=hook_name)
            bpy.context.object.modifiers[hook_name].falloff_type = 'SMOOTH'

            tad.modifiers[ob.name+'_m'].object = bpy.context.scene.objects[ob.name] # parent the object to the modifier
        else:
            bpy.ops.object.hook_add_newob()
            hmod = tad.modifiers[i]
            hmod.name = 'tad_hook_m_'+str(i).zfill(5)          
            hobj = hmod.object 
            hobj.hide = False
            hobj.name = 'tad_hook_o_'+str(i).zfill(5)
            frac = i/len(bpy.data.curves[curvename].splines[0].points)
            pos = frac * scope - (scope/2)
            if(int(i)%warp == 0):
                print("pos=%.5f i=%s frac=%.4f scope=%s" % (pos, i, frac, scope))
            hobj.location[0] = pos
            hobj.location[1] = 0
            hobj.location[2] = 0
            #print(hobj.location)
            hobj.keyframe_insert(data_path="location", frame=start_f, index=0)
            hobj.keyframe_insert(data_path="location", frame=start_f, index=1)
            hobj.keyframe_insert(data_path="location", frame=start_f, index=2)
            hobj.location = p.co[0:3]
            hobj.keyframe_insert(data_path="location", frame=end_f, index=0)
            hobj.keyframe_insert(data_path="location", frame=end_f, index=1)
            hobj.keyframe_insert(data_path="location", frame=end_f, index=2)
            bpy.data.objects[hobj.name].layers[1] = True
            bpy.data.objects[hobj.name].layers[0] = False
            
        if(bezier):
            p = tadc.splines[0].bezier_points[i]
            p.select_control_point = False
            p.select_left_handle = False
            p.select_right_handle = False
        else:
            p = tadc.splines[0].points[i]
            p.select = False
        
        bpy.ops.curve.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")

def RGB_to_sRGB(rgb=[255,255,255]):
    rgb[0] = (rgb[0]/255)**2.2
    rgb[1] = (rgb[1]/255)**2.2
    rgb[2] = (rgb[2]/255)**2.2
    rgb.append(1)
    return(rgb)

def gen_materials(matname='tad_mat', steps=2000, warp = 250):  
    material = bpy.data.materials.new(name=matname)
    material.use_nodes = True
    
    # Remove default nodes
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    for i in nodes:
        nodes.remove(i)
    # add all nodes needed for UV mapping along the X axis
    nodes.new(type="ShaderNodeOutputMaterial") 
    nodes[len(nodes)-1].name = "output"
    nodes.new(type="ShaderNodeBsdfDiffuse")   
    nodes[len(nodes)-1].name = "diffuse"
    ColorRamp = nodes.new(type="ShaderNodeValToRGB")
    nodes[len(nodes)-1].name = "colramp"
    Separate = nodes.new(type="ShaderNodeSeparateXYZ")
    nodes[len(nodes)-1].name = "separate"
    TextCoordi = nodes.new(type="ShaderNodeTexCoord")
    nodes[len(nodes)-1].name = "texcoord"
    # connect the nodes output-input accordingly
    links.new(nodes['texcoord'].outputs['UV'], nodes['separate'].inputs['Vector'])
    links.new(nodes['separate'].outputs['X'], nodes['colramp'].inputs['Fac'])
    links.new(nodes['colramp'].outputs['Color'], nodes['diffuse'].inputs['Color'])
    links.new(nodes['diffuse'].outputs['BSDF'], nodes['output'].inputs['Surface'])
     
    for i in range(len(nodes)):
        nodes[i].location = (i*-300,0)  
    colramp = nodes['colramp'].color_ramp
    # this sets the changes of colors into discrete transitions instead of gradients
    colramp.interpolation = "CONSTANT"
    # set color for first two elements and reset position
    total = int(steps/warp)
    print("total colors %s" % total)
    ##print("total %s" % total)
    
    for i in range(len(colramp.elements)):
        colramp.elements[i].position = 0
    for i in range(total):
        #print("turn %s total of %s" %(i, total))
        colramp = nodes['colramp'].color_ramp
        pos = i/total
        # horrible trick to convert to sRGB
        color = RGB_to_sRGB(colors[total][i])
        #color[0] = (color[0]/255)**2.2
        #color[1] = (color[1]/255)**2.2
        #color[2] = (color[2]/255)**2.2
        
        if(i < 2):
            #print("%s old pos %s" % (i,colramp.elements[i].position))
            colramp.elements[i].position = pos
        if(i == total):
            color = RGB_to_sRGB(colors[total][i-1])
            #color[0] = (color[0]/255)**2.2
            #color[1] = (color[1]/255)**2.2
            #color[2] = (color[2]/255)**2.2
            
        if(i >= 2):
            colramp.elements.new(pos)  
        ##print("%s  now %s %s" %(i, color, pos))
        colramp.elements[i].color = color
        
    #for i in range(len(colramp.elements)):
    #    print(colramp.elements[i].position)
        
        
 ####
 ####
 ####
 
 
#clean_tads()
# weight  
w = 1 

listOfVectors = [(0,0,0),(1,0,0),(2,0,0),(2,3,0),(0,2,1),(20,3,4)]  
hops = 50

walk = numpy.random.normal(1,1,3*hops)
#random cloud
#listOfVectors = list(walk.reshape(hops, 3))

limit=2
scale = limit/9
min_delta = scale/6
max_delta = scale/5
radius = limit/100
cis = 10
#tad_path = MakeTadPath(hops, scale=scale, limit=limit, min_delta=min_delta, radius=radius, mingle=100)
#to_origin = connect_tad(hops=100,a=tad_path[hops][0:3], b=(0,0,0))

#tad_path+=to_origin
#knn =getNeighbors_radius(tad_path, tad_path, k=10, cis=5)
#for i in knn: print("%s\n"%i)
#tad_path = importWalk("C:/Users/pedro/Dropbox/blender/path_test.txt")
#tad_path = importWalk("/home/pedro/Dropbox/blender/path_test.txt")
#tad_path1 = importWalk("C:/Users/pedro/Dropbox/blender/path_10k_dense_warp_300.txt")
#tad_path2 = importWalk("C:/Users/pedro/Dropbox/blender/path_2k_dense_w_200.txt")
tad_path6 = importWalk("C:/Users/pedro/Dropbox/blender/path_6k_dense_w_200_l_0.5_al_2.4.txt")
#tad_path3= importWalk("C:/Users/pedro/Dropbox/blender/path_test3.txt")
#tad_path = importWalk("C:/Users/pedro/Dropbox/blender/path_test4.txt")

#mem_path = importWalk("C:/Users/pedro/Dropbox/blender/mem_test.txt")
#mem_path = importWalk("/home/pedro/Dropbox/blender/mem_test.txt")
#knn_path = importWalk("C:/Users/pedro/Dropbox/blender/knn_test.txt")
#for i in tad_path: print("%s\n"%i)
    
    
prev  = [1,1,0]
current = [0,0,0]
proposal = [1,-1,0]
#theta = theta_AB(prev, current, proposal)
#tad_path = [prev, current, proposal]
#print(theta[0])

#MakeTad("tad_object", "tad_curve", tad_path, warp = 300)
#MakeTad("tad_object", "tad_curve", tad_path6, warp = 200)
#hookTad("tad_object", warp = 200, scope=12)
gen_materials(matname='tad_ma', steps=6000, warp = 200)

#MakeTad("tad_object1", "tad_curve1", tad_path1)
#MakeTad("tad_object2", "tad_curve2", tad_path2)
#MakeTad("tad_object3", "tad_curve3", tad_path3)
#MakeTad("tad_object4", "tad_curve4", tad_path4)
#MakeTad("tad_objectm", "tad_curvem", mem_path)
#MakeTad("tad_knn", "tad_curveknn", knn_path, type='POLY', bevel=False)
#MakeTad("tad_origin", "tad_curve", to_origin)
