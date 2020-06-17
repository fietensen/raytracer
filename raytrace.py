"""
Experimental Raytracing Engine by Format_HDD (2020)
"""

import json, sys
from utilities import vector, engine, scene, light, dobject, color, lighteffects
pillow = False
try:
    from PIL import Image
    pillow = True
except:
    pass


def main():
    if len(sys.argv) != 2:
        print("[ERROR]: please append a model file.")
        sys.exit(1)
    model = None
    with open(sys.argv[1], "r") as fp:
        model = json.load(fp)

    width   = model["resolution"]["width"]
    height  = model["resolution"]["height"]
    AA      = model["resolution"]["AntiAliasing"]
    objects = []

    if AA:
        if not pillow:
            print("[ERROR]: Antialiasing doesn't work without Pillow installed.")
            sys.exit(1)
        width *= 2
        height *= 2

    for object_ in model["objects"]:
        if object_["type"] == "Sphere":
            x,y,z      = object_["X"],object_["Y"],object_["Z"]
            position   = vector.Vec3(x,y,z)
            radius     = object_["radius"]
            color_     = object_["color"]
            ID         = object_["ID"]
            effects    = object_["effects"]
            obj_effects= []
            extra      = None

            if "extra" in object_.keys():
                extra = object_["extra"]

            for effect in effects:
                if effect in lighteffects.effects.keys():
                    if object_["type"] in lighteffects.effects[effect][1]:
                        obj_effects.append(lighteffects.effects[effect][0])
                    else:
                        print("[ERROR]: Assigning effect \"%s\" to object \"%s\" failed. Effect not possible for \"%s\"." % (effect, ID, object_["type"]))
                        sys.exit(1)
                else:
                    print("[ERROR]: Assigning effect \"%s\" to object \"%s\" failed. No such effect." % (effect, ID))
                    sys.exit(1)

            obj      = dobject.dObject(
                    obj_id    =ID,
                    obj_type  ="Sphere",
                    position  =position,
                    radius    =radius,
                    color     =color.Color().from_hex(color_),
                    effects   =obj_effects,
                    extra     =extra)
            
            objects.append(obj)
            
        elif object_["type"] == "Plane":
            x,y,z      = object_["X"],object_["Y"],object_["Z"]
            direction  = vector.Vec3(x,y,z)
            x,y,z      = object_["dX"],object_["dY"],object_["dZ"]
            position   = vector.Vec3(x,y,z)
            color_     = object_["color"]
            ID         = object_["ID"]
            effects    = object_["effects"]
            obj_effects= []
            extra      = None

            if "extra" in object_.keys():
                extra = object_["extra"]

            if type(color_) == list:
                if len(color_) == 0:
                    print("[ERROR]: Cannot use empty list as object color.")
                    sys.exit(1)

            for effect in effects:
                if effect in lighteffects.effects.keys():
                    if object_["type"] in lighteffects.effects[effect][1]:
                        obj_effects.append(lighteffects.effects[effect][0])
                    else:
                        print("[ERROR]: Assigning effect \"%s\" to object \"%s\" failed. Effect not possible for \"%s\"." % (effect, ID, object_["type"]))
                        sys.exit(1)
                else:
                    print("[ERROR]: Assigning effect \"%s\" to object \"%s\" failed. No such effect." % (effect, ID))
                    sys.exit(1)

            obj      = dobject.dObject(
                    obj_id     =ID,
                    obj_type   ="Plane",
                    position   =position,
                    plane_point=direction,
                    color      =[color.Color().from_hex(c) for c in color_] if type(color_) == list else color.Color().from_hex(color_),
                    effects    =obj_effects,
                    extra      =extra)

            objects.append(obj)
            
        else:
            print("[ERROR] The object type \"%s\" does not exist." % object_["type"])
            sys.exit(1)

    ## light & camera
    camera = vector.Vec3(model["camera"]["X"], model["camera"]["Y"], model["camera"]["Z"])
    light_ = light.Light(vector.Vec3(model["light"]["X"], model["light"]["Y"], model["light"]["Z"]), model["light"]["brightness"])
    scene_ = scene.Scene(objects, camera, light_, width, height, AA)
        
    r_engine  = engine.RenderEngine()
    image_out = r_engine.render(scene_)
    if pillow and "fileformat" in model.keys():
        im = Image.new("RGB", (width, height))
        im.putdata(image_out.getdata())
        if AA:
            im.thumbnail((round(width/2), round(height/2)), Image.ANTIALIAS)
        im.save(model["Project"]+"."+model["fileformat"])
        sys.exit(0)
    elif not pillow and "fileformat" in model.keys():
        if fileformat.lower() != "ppm":
            print("[ERROR]: Pillow is not installed. Defaulting to PPM-file format.")
    image_out.save(model["Project"]+".ppm")

if __name__ == "__main__":
    main()	
