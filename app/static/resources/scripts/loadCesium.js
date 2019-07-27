Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIwYmJlYzNlYS0yN2UwLTRmMGMtOWMyMi1iYjMwMzQzMzgzYjYiLCJpZCI6ODI4Nywic2NvcGVzIjpbImFzciIsImdjIl0sImlhdCI6MTU1MTY3OTM2OX0.EGK5EcrEjcL-Wi6CN_iPtzHKsxwHOn_vhXep3qjbfQU';

var viewer = new Cesium.Viewer('cesiumContainer');


$.ajax({
    url: '/get_data',
    type: 'POST',
    success: function(response) {
        process_data(response);
    }
});

function process_data(data) {
    for(var track_key in data) {
        if(data.hasOwnProperty(track_key)) {
            var track = data[track_key];

            point_list = []
            for(var point_key in track) {
                if(track.hasOwnProperty(point_key)) {
                    if(point_key == 'id') {}
                    else if(point_key == 'point_count') {}
                    else {
                        var point = track[point_key];
                        var latitude = parseFloat(point['latitude']);
                        var longitude = parseFloat(point['longitude']);

                        point_list.push(longitude);
                        point_list.push(latitude);
                    }
                }
            }

            viewer.entities.add({
                polyline: {
                    positions: Cesium.Cartesian3.fromDegreesArray(point_list),
                    width : 2.0,
                    material : Cesium.Color.RED
                }
            });
        }
    }
}

function add_point(point) {
    console.log('Adding point');
    var latitude = parseFloat(point['latitude']);
    var longitude = parseFloat(point['longitude']);

    viewer.entities.add({
        position : Cesium.Cartesian3.fromDegrees(longitude, latitude),
        point : {
            pixelSize : 5,
            color : Cesium.Color.RED
        }
    });
}
