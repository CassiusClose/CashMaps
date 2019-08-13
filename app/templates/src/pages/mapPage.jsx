import React from 'react';
import { Viewer, Entity, PointGraphics, EntityDescription } from 'resium';
import { Cartesian3 } from 'cesium';
import Header from './header';

export default class CesiumMap extends React.Component {
  constructor(props) {
    super(props);

    this.test();
  }

  test = () => {
    $.ajax({
      url: "/map/_get_data",
      type: "POST",
    });
  }

  render() {
    return(
      <div>
        <Viewer>
          <Entity position={Cartesian3.fromDegrees(-74.0707383, 40.7117244, 100)} name="Test">
            <PointGraphics pixelSize={5}/>
            <EntityDescription>
              <h1>Hi there</h1>
              <p>This is sick!</p>
            </EntityDescription>
          </Entity>
        </Viewer>
      </div>
    );
  }
}
