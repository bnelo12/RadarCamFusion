var socket = io('192.168.0.163:5000')

var camera_canvas = document.getElementById('camera-view-canvas');
var camera_ctx = camera_canvas.getContext('2d');
camera_canvas.width = camera_canvas.offsetWidth;
camera_canvas.height = camera_canvas.offsetHeight;

socket.on('connect', () => {
    console.log('Connected to PiCam');
    socket.on('image', (arrayBuffer, callback) => {
        var blob = new Blob( [ arrayBuffer ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        var img = new Image();
        img.src = imageUrl;
        img.onload = () => {
            camera_ctx.drawImage(img, 0, 0, img.width,    img.height,
                0, 0, camera_canvas.width, camera_canvas.height);
                callback();
        }
    });
    socket.on('test', (data) => {
        console.log(data);
    });
})
