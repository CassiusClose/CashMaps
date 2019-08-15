import React from 'react';
import { Viewer, Entity, PointGraphics, EntityDescription, Polyline, PolylineCollection } from 'resium';
import { Cartesian3 } from 'cesium';
import Header from './header';

/**
 * Displays a cesium widget and displays track data on it from the server.
 */
export default class CesiumMap extends React.Component {
  constructor(props) {
    super(props);

    this.state = {tracks:null};

    this.get_track_data();
  }

  /* Gets track data from the server and passes it to set_track_data(). */
  get_track_data = () => {
    var successFunc = this.set_track_data;
    $.ajax({
      url: "/map/_get_data",
      type: "POST",
      success: function(response) {
        successFunc(response.tracks);
      }
    });
  }

  /* Loads track data into this components state. Formats the points into Cartesian3 form. */
  set_track_data = (data) => {
    //Replace the dicts of point objects with arrays of Cartesian3 objects so Cesium can read them
    for(var track of data) {
      var points = [];
      for(const point of track.points) {
        points.push(Cartesian3.fromDegrees(point.longitude, point.latitude));
      }
      track.points = points;
    }

    this.setState({tracks: data});
  }

  render() {
    return(
      <div>
        <Viewer>
            <Entity>
              <PolylineCollection>
                {
                  this.state.tracks != null &&
                  this.state.tracks.map((track) => (
                    <Polyline
                      key={track.database_id}
                      positions={track.points}
                    />
                  ))
                }
              </PolylineCollection>
            </Entity>
        </Viewer>
      </div>
    );
  }
}
