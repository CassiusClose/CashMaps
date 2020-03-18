import React from 'react';
import { Viewer, Entity, PointGraphics, EntityDescription, Polyline, PolylineCollection, LabelGraphics } from 'resium';
import LoadingTextAnim from './../components/loading_text_anim';
import { Cartesian3 } from 'cesium';
import Header from './header';


Cesium.Ion.defaultAccessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIwYmJlYzNlYS0yN2UwLTRmMGMtOWMyMi1iYjMwMzQzMzgzYjYiLCJpZCI6ODI4Nywic2NvcGVzIjpbImFzciIsImdjIl0sImlhdCI6MTU1MTY3OTM2OX0.EGK5EcrEjcL-Wi6CN_iPtzHKsxwHOn_vhXep3qjbfQU";

/**
 * Displays a cesium widget and displays track data on it from the server.
 */
export default class CesiumMap extends React.Component {
  constructor(props) {
    super(props);

    this.state = {tracks:null, loading:true};

    this.load_map();
  }

  load_map = () => {
    this.get_track_data();
  }

  /* Gets track data from the server and passes it to set_track_data(). */
  get_track_data = () => {
    console.log("Fetching map data...");
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
    console.log("Loading map data...");
    //Replace the dicts of point objects with arrays of Cartesian3 objects so Cesium can read them
    for(var track of data) {
      var points = [];
      for(const point of track.points) {
        points.push(Cartesian3.fromDegrees(point.longitude, point.latitude));
      }
      track.points = points;
    }

    this.setState({tracks: data, loading: false});
    console.log("Done loading map data");
  }



  render() {
    return(
      <div>
        { this.state.loading &&
            <LoadingTextAnim/>
        }
        { !this.state.loading &&
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
        }
      </div>
    );
  }
}
