import React from 'react';
import GridLayout from 'react-grid-layout';
import { Responsive, WidthProvider } from 'react-grid-layout';
import './gallery.css';
const config = require('./../config.json');

export default class Gallery extends React.Component {
  constructor(props) {
    super(props);

    //TODO
    var gridWidth = 1200;
    var colNumber = 4;
    var imageWidth = gridWidth/colNumber;
    this.state = {
      colNumber: colNumber,
      gridWidth: gridWidth,
      imageWidth: imageWidth, 
      gridLayout:[],
      images:[]
    };

    this.loadImages();
  }

  loadImages = () => {
    var successFunc = this.setImages;
    $.ajax({
      url: '/_get_photos',
      type: 'POST',
      success: function(response) { successFunc(response.photos); }
    });
  }

  setImages = (photos) => {
    var layout = [];
    var x = 0;
    var y = 0;
    for(var photo of photos) {
      var photo_layout = {i: photo.id.toString(), x:x, y:y, w:1, h:1, static:true};
      layout.push(photo_layout);
      x += 1;
      if(x == this.state.colNumber) {
        x = 0;
        y += 1;
      }
    }
    this.setState({gridLayout: layout, images: photos});
  }

  render() {
    return(
      <div>
        <h1>Gallery</h1>
        <GridLayout
          layout={this.state.gridLayout}
          cols={this.state.colNumber}
          width={this.state.gridWidth}
          rowHeight={this.state.imageWidth}
          margin={[15, 15]}
        >
          { this.state.images.map((item) => (
            <GalleryImage
              key={item.id.toString()}
              imagesrc={config.PHOTOS_FOLDER_RELATIVE_PATH + item.filepath}
            />
            ))
          }
        </GridLayout>
      </div>
    );
  }
}

class GalleryImage extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {imgSrc: src, imgWidth:0, imgHeight:0};

    var src = this.props.imagesrc;
    var image = new Image();
    image.onload = this.setDimensions.bind(image);//(image.width, image.height);//.bind(image.height, image.height);
    image.src=src;
  }

  setDimensions = (image) => {
    console.log("Dim:");
    console.log(image.originalTarget.width);
    console.log(image.originalTarget.height);
    this.setState({imgWidth:image.originalTarget.width, imgHeight:image.originalTarget.height});
  }

  render() {
    var dim = {};
    if(this.state.imgWidth > this.state.imgHeight) {
      dim = {width: this.props.style.width};
    } else {
      dim = {height: this.props.style.height};
    }
    return(
      <div {...this.props} className="GalleryImage_Container">
        <img
          style={dim}
          className="GalleryImage_Image"
          src={this.state.imageSrc} 
        />  
      </div>
    );
  }
}

class GalleryImageDiv extends React.Component {
  render() {
    return(
      <div {...this.props}>
        {React.cloneElement(this.props.child,
        )}
      </div>
    );
  }
}
