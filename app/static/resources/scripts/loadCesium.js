Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIwYmJlYzNlYS0yN2UwLTRmMGMtOWMyMi1iYjMwMzQzMzgzYjYiLCJpZCI6ODI4Nywic2NvcGVzIjpbImFzciIsImdjIl0sImlhdCI6MTU1MTY3OTM2OX0.EGK5EcrEjcL-Wi6CN_iPtzHKsxwHOn_vhXep3qjbfQU';

var viewer = new Cesium.Viewer('cesiumContainer');


//Requests track data from the server
$.ajax({
    url: '/_get_data',
    type: 'POST',
    success: function(response) {
        process_data(response);
    }
});

function process_data(data) {
    """Processes JSON track data from the server and adds it to the Cesium widget"""

    //For each track
    for(var track_key in data) {
        if(data.hasOwnProperty(track_key)) {
            var track = data[track_key];

            point_list = [] //List of floats in long, lat, long, lat format for Cesium

            //For each point
            for(var point_key in track) {
                if(track.hasOwnProperty(point_key)) {

                    //Processes data based on the key
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

            //Ad the point list to the Cesium widget to create a line
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
