from app import db
from app.models import *

def get_track_data():
    data = {}
    for track in Track.query.all():
        track_data = {'id':track.track_id, 'point_count':len(track.points.all())}
        for point in track.points.all():
            point_data = {'id':point.point_id, 'latitude':point.latitude, 'longitude':point.longitude}
            track_data.update({str(point.point_id) : point_data})
        data.update({str(track.track_id) : track_data})
    return data

