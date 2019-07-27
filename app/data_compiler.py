from app import db
from app.models import *

def get_track_data():
    """Compiles track data into a dictionary for conversion to JSON

    Organizes track data from the database into a nested dictionary. The dictionary
    is intended to be converted to JSON and sent off to Cesium to be displayed.
    The dictionary structure:
    data = 
        {
        track_id : 
            {
            id : track_id,
            point_count : number of points contained,
            point_id :
                {
                id : point_id
                latitude : latitude
                longitude : longitude
                }
            }
        }
    
    This will likely be expanded in the future
    """

    data = {}
    for track in Track.query.all():
        track_data = {'id':track.track_id, 'point_count':len(track.points.all())}

        for point in track.points.all():
            point_data = {'id':point.point_id, 'latitude':point.latitude,\
                    'longitude':point.longitude}
            track_data.update({str(point.point_id) : point_data})

        data.update({str(track.track_id) : track_data})
    return data
