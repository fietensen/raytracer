from utilities import vector, color, ray
from math import sqrt

def phong(engine, color_, hit_pos, hit_obj, scene):
    norm = None
    if hit_obj.obj_type == "Sphere":
        norm      = (hit_pos - hit_obj.position) * (1.0 / hit_obj.radius)
    elif hit_obj.obj_type == "Plane":
        norm = hit_obj.position
    rayorig   = (scene.camera - hit_pos).normalize()
    nudge     = hit_pos + norm * .0001
    light_ray = ray.Ray(nudge, scene.light.position-hit_pos)
    
    phong_    = norm.dotproduct((light_ray.direction + rayorig).normalize())
    color_ += color.Color(1, 1, 1) * min(max(phong_, 0), 1)**50
    return color_

def lambert(engine, color_, hit_pos, hit_obj, scene):
    nudge = None
    if hit_obj.obj_type == "Sphere":
        norm  = (hit_pos - hit_obj.position) * (1.0 / hit_obj.radius)
        nudge = hit_pos + norm * .0001
    elif hit_obj.obj_type == "Plane":
        nudge = hit_pos + hit_obj.position * .0001
    else:
        print("[ERROR]: trying to apply lambert to unknown object type. (%s)" % hit_obj.ID)
        sys.exit(1)
    light_ray = ray.Ray(nudge, scene.light.position-hit_pos)
    
    c = color.Color(0.05, 0.05, 0.05)
    lv = max(norm.dotproduct(light_ray.direction), 0)
    c += (color_ * lv)
    return c

def lowlightshade(engine, color_, hit_pos, hit_obj, scene):
    nudge = None
    if hit_obj.obj_type == "Sphere":
        norm  = (hit_pos - hit_obj.position) * (1.0 / hit_obj.radius)
        nudge = hit_pos + norm * .0001
    elif hit_obj.obj_type == "Plane":
        bias = .0001
        hit_pos.y += -bias if hit_obj.plane_point.y <= hit_obj.position.y else bias
        nudge = hit_pos
    else:
        print("[ERROR]: trying to apply lowlightshade to unknown object type. (%s)" % hit_obj.ID)
        sys.exit(1)
    light_ray = ray.Ray(nudge, scene.light.position-hit_pos)

    obj_distance, obj_hit = engine.find_nearest(light_ray, scene)
    if obj_hit:
        color_ -= color.Color(.6, .6, .6)
    return color_

def lightfade(engine, color_, hit_pos, hit_obj, scene):
    distance = sqrt((scene.light.position.x - hit_pos.x)**2 + (scene.light.position.y - hit_pos.y)**2 + (scene.light.position.z - hit_pos.z)**2)
    if distance != 0:
        dimm = 1 - ((float(scene.light.brightness/10.0)*100/(distance)) / 100)
        color_ -= color.Color(dimm, dimm, dimm)
    return color_

def planestyle_chess(engine, color_, hit_pos, hit_obj, scene):
    if type(color_) != list:
        color_ = [color_, color_]
    if len(color_) == 1:
        color_ *= 2
    nX = hit_pos.x % 0.5
    nZ = hit_pos.z % 0.5
    c = None

    if (nX < .25 and nZ < .25) or (nX > .25 and nZ > .25):
        c = color_[0]
    elif (nX > .25 and nZ < .25) or (nX < .25 and nZ > .25):
        c = color_[1]
    else:
        c = color.Color().from_hex("#000000")
    return c

bounce = 0

def lightbounce(engine, color_, hit_pos, hit_obj, scene):
    global bounce
    norm = None
    
    if hit_obj.obj_type == "Sphere":
        norm  = (hit_pos - hit_obj.position) * (1.0 / hit_obj.radius)
    elif hit_obj.obj_type == "Plane":
        norm = hit_obj.position
        
    rayorig = (hit_pos-scene.camera)
    nudge = hit_pos + norm * .001
    
    mray = ray.Ray(nudge, rayorig - norm * 2 * rayorig.dotproduct(norm))

    if not bounce:
        bounce = 1
        color__ = color.Color(.0, .0, .0)
        dist_hit, obj_hit = engine.find_nearest(mray, scene, exclude=hit_obj)
        if obj_hit is not None:
            hit_pos_ = mray.origin + mray.direction * dist_hit
            color__ += engine.color_at(obj_hit, hit_pos_, scene)
            

            color_ += color__ * ((hit_obj.extra["reflect"] if "reflect" in hit_obj.extra.keys() else 80)/100)
        else:
            color_ += color__ 
    bounce = 0
    return color_

effects = {
    "phong":   (phong, ["Sphere", "Plane"]),
    "lambert": (lambert, ["Sphere", "Plane"]),
    "lowlightshade": (lowlightshade, ["Sphere", "Plane"]),
    "lightfade": (lightfade, ["Sphere", "Plane"]),
    "lightbounce": (lightbounce, ["Sphere", "Plane"]),
    "planestyle-chess": (planestyle_chess, ["Plane"])
    }
