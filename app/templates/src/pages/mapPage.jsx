import React from 'react';
import { Viewer, Entity, PointGraphics, EntityDescription, Polyline, PolylineCollection } from 'resium';
import { Cartesian3 } from 'cesium';
import Header from './header';

export default class CesiumMap extends React.Component {
  constructor(props) {
    super(props);

    this.state = {tracks:null};

    this.get_track_data();
  }

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

  set_track_data = (data) => {
    //Replace point dicts with CartesianCoords
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
