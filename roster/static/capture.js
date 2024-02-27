// capture.js
document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const captureButton = document.getElementById('capture');

    // Access the webcam
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (err) {
                console.log("Something went wrong!", err);
            });
    }

    // Capture the image and send data
    captureButton.addEventListener('click', function () {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas image to data URL (base64)
        const imageDataUrl = canvas.toDataURL('image/png');

        // Send the image data to Django backend using AJAX
        $.ajax({
            type: "POST",
            url: "/your-endpoint-url/", // Update this URL to your Django view endpoint
            data: {
                image_data: imageDataUrl,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), // Handle CSRF token
            },
            success: function (response) {
                // Handle success
                console.log("Image sent successfully!");
                console.log(response); // You can do something with the response
            },
            error: function (error) {
                // Handle error
                console.log("Error sending image:", error);
            }
        });
    });
});
