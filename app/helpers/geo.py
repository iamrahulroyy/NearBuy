from shapely.geometry import Point
from geoalchemy2.shape import to_shape
from geoalchemy2.shape import from_shape

def create_point_geometry(latitude: float, longitude: float):
    if latitude is not None and longitude is not None:
        return from_shape(Point(float(longitude), float(latitude)), srid=4326)
    return None

def geometry_to_latlon(geometry):
    if geometry is not None:
        try:
            point = to_shape(geometry)
            return {
                "latitude": point.y,
                "longitude": point.x
            }
        except Exception:
            pass
    return {"latitude": None, "longitude": None}
