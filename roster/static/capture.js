document.addEventListener('DOMContentLoaded', function () {
    var video = document.querySelector('#webcam');
    var captureButton = document.getElementById('capture');
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    // Request access to the webcam
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
            video.srcObject = stream;
            video.play();
        });
    }

    // Capture the photo on button click
    captureButton.addEventListener('click', function () {
        context.drawImage(video, 0, 0, 640, 480); // Draw the video frame to the canvas
        var imageDataURL = canvas.toDataURL('image/png'); // Get image data as a URL

        // Get current timestamp
        var timestamp = new Date().toISOString();

        // Send the image data and timestamp to the server using AJAX
        $.ajax({
            type: "POST",
            url: "/capture_attendance/", // URL to Django view handling the post
            data: {
                image: imageDataURL,
                timestamp: timestamp,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() // Handle CSRF token
            },
            success: function (response) {
                alert("Attendance captured successfully!");
            },
            error: function (error) {
                console.log(error);
                alert("Error capturing attendance.");
            }
        });
    });
});
