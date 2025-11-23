
def create_point_geometry(latitude: float, longitude: float):
    if latitude is not None and longitude is not None:
        return {"latitude": float(latitude), "longitude": float(longitude)}
    return None

def geometry_to_latlon(geometry):
    # This might need adjustment depending on how we read back from DB, 
    # but since we are now storing as columns, we might not need this conversion 
    # in the same way. For now, let's assume 'geometry' is the shop object or dict
    if isinstance(geometry, dict):
        return {
            "latitude": geometry.get("latitude"),
            "longitude": geometry.get("longitude")
        }
    # If it's an object with attributes
    if hasattr(geometry, "latitude") and hasattr(geometry, "longitude"):
         return {
            "latitude": geometry.latitude,
            "longitude": geometry.longitude
        }
    return {"latitude": None, "longitude": None}
