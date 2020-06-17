import math

def Sphere(sphere, ray):
    sphere_ray = ray.origin - sphere.position
    b = 2 * ray.direction.dotproduct(sphere_ray)
    c = sphere_ray.dotproduct(sphere_ray) - sphere.radius*sphere.radius
    discrims = b*b - 4 * c
    if discrims < 0:
        return None
    return (-b - math.sqrt(discrims)) /2

def Plane(plane, ray):
    r = (ray.direction.x*plane.position.x + ray.direction.y*plane.position.y + ray.direction.z*plane.position.z)
    assert (r!=0), "Plane shall not be on same y as the camera."
    t = (plane.plane_point.x*plane.position.x + plane.plane_point.y*plane.position.y + plane.plane_point.z*plane.position.z - plane.position.x*plane.position.x - plane.position.y*ray.origin.y - plane.position.z*ray.origin.z) / r
    if t<0:
        return None
    x,y,z = ray.origin.x+t*ray.direction.x, ray.origin.y+t*ray.direction.y, ray.origin.z+t*ray.direction.z
    return math.sqrt((ray.origin.x - x)**2 + (ray.origin.y - y)**2 + (ray.origin.z - z)**2)
