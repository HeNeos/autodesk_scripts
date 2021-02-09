import math
from win32com.client import Dispatch, GetActiveObject, gencache, constants 
try:
    invApp = GetActiveObject('Inventor.Application')
except:
    invApp = Dispatch('Inventor.Application')
    invApp.Visible = True

mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
invApp = mod.Application(invApp)
# invApp.SilentOperation = True

# Create a new part
invDoc = invApp.Documents.Add(constants.kPartDocumentObject, "", True)

# Casting Document to PartDocument
invPartDoc = mod.PartDocument(invDoc)

compdef = invPartDoc.ComponentDefinition

# Create a sketch
xyPlane = compdef.WorkPlanes.Item(3)
origin_point = invApp.TransientGeometry.CreatePoint(0, 0, 0)
x_axis = invApp.TransientGeometry.CreateUnitVector(1, 0, 0)
y_axis = invApp.TransientGeometry.CreateUnitVector(0, 1, 0)

l = 4
h = 2*(3**0.5)
r = 4/(3**0.5)
for i in range(0, 30):
    angle = i*0.1
    offPlane = compdef.WorkPlanes.AddByPlaneAndOffset(xyPlane, 2*i+2)
    #offPlane = compdef.WorkPlanes.AddFixed(origin_point, x_axis, y_axis)
    #compdef.Constraint.AddFlushConstraint(offPlane, xyPlane, 10)

    sketch = compdef.Sketches.Add(offPlane)

    # Set Geometry variables
    tg = invApp.TransientGeometry
    lines = sketch.SketchLines

    # Draw Triangle
    
    line1 = lines.AddByTwoPoints(tg.CreatePoint2d(r*math.cos(angle), r*math.sin(angle)), tg.CreatePoint2d(r*math.cos(angle+2*math.pi/3), r*math.sin(angle+2*math.pi/3)))
    line2 = lines.AddByTwoPoints(line1.EndSketchPoint, tg.CreatePoint2d(r*math.cos(angle+4*math.pi/3), r*math.sin(angle+4*math.pi/3)))
    line3 = lines.AddByTwoPoints(line2.EndSketchPoint, line1.StartSketchPoint)
    offPlane.Visible = False

'''
# Loft
objs = sketch.Profiles.AddForSolid()
loftDef = compdef.Features.LoftFeatures.CreateLoftDefinition(
    objs, constants.kJoinOperation)

loftFeat = compdef.Features.LoftFeatures.Add(loftDef)
'''

'''
# Extrude
profile = sketch.Profiles.AddForSolid()
extrudeDef = compdef.Features.ExtrudeFeatures.CreateExtrudeDefinition(
    profile, constants.kJoinOperation)
extrudeDef.SetDistanceExtent(1, constants.kNegativeExtentDirection)
extrude = compdef.Features.ExtrudeFeatures.Add(extrudeDef)
'''
