#Author-HeNeos
#Description-Many triangles, I love triangles

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def run(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Are you ready')
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        # Create a new ObjectCollection.
        objColl = adsk.core.ObjectCollection.create()
        revolves = rootComp.features.revolveFeatures
        

        sketch = sketches.add(xyPlane)
        circles = sketch.sketchCurves.sketchCircles
        lines = sketch.sketchCurves.sketchLines
        r = 4
        loftFeats = rootComp.features.loftFeatures
        loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSectionsObj = loftInput.loftSections
        for i in range(0,100):
            angle = (math.pi)/25*i
            
            if i >= 0:
                ctorPlanes = rootComp.constructionPlanes
                plane = ctorPlanes.createInput()
                offset = adsk.core.ValueInput.createByString(str(i)+" cm")
                plane.setByOffset(xyPlane, offset)
                Plane = ctorPlanes.add(plane)
                sketch = sketches.add(Plane)
                lines = sketch.sketchCurves.sketchLines

            point1 = adsk.core.Point3D.create(r*math.sin(angle), r*math.cos(angle), i)
            point2 = adsk.core.Point3D.create(r*math.sin(angle+2*math.pi/3), r*math.cos(angle+2*math.pi/3), i)
            point3 = adsk.core.Point3D.create(r*math.sin(angle+4*math.pi/3), r*math.cos(angle+4*math.pi/3), i)

            lines.addByTwoPoints(point1, point2)
            lines.addByTwoPoints(point2, point3)
            lines.addByTwoPoints(point3, point1)
            
            profile = sketch.profiles.item(0)

            loftSectionsObj.add(profile)        
        
        loftInput.isSolid=True
        loftFeats.add(loftInput)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    #axis = lines.addByTwoPoints(adsk.core.Point3D.create(-1,-4,0), adsk.core.Point3D.create(1,-4,0))
    #circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)


def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Finished')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
