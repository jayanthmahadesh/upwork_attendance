// const video = document.getElementById("video");
// const captureBtn = document.getElementById("captureBtn");
// const capturedImage = document.getElementById("capturedImage");
// const canvas = document.getElementById("canvas");
// const context = canvas.getContext("2d");

// // Access camera
// navigator.mediaDevices
//   .getUserMedia({ video: true })
//   .then((stream) => {
//     video.srcObject = stream;
//     video.play();
//   })
//   .catch((error) => console.error("Error accessing camera:", error));

// // Capture and Send Image
// captureBtn.addEventListener("click", () => {
//   // Set canvas dimensions to video size
//   canvas.width = video.videoWidth;
//   canvas.height = video.videoHeight;

//   context.drawImage(video, 0, 0, canvas.width, canvas.height);
//   const dataURL = canvas.toDataURL("image/jpeg");

//   // Prepare image data for sending
//   const data = {
//     image: dataURL,
//     // Add other form fields if you've defined them
//   };

//   // Send to Django using fetch
//   fetch("/upload_image", {
//     method: "POST",
//     body: JSON.stringify(data),
//     headers: { "Content-Type": "application/json" },
//   })
//     .then((response) => {
//       if (response.ok) {
//         console.log("Image uploaded successfully");
//       } else {
//         console.error("Error uploading image:", response.status);
//       }
//     })
//     .catch((error) => console.error("Error:", error));
// });

// const video = document.getElementById("video");
// const canvas = document.getElementById("canvas");
// const captureButton = document.getElementById("capture-btn");

// navigator.mediaDevices
//   .getUserMedia({ video: true })
//   .then((stream) => (video.srcObject = stream))
//   .catch(console.error);

// captureButton.addEventListener("click", () => {
//   const context = canvas.getContext("2d");
//   canvas.width = video.videoWidth;
//   canvas.height = video.videoHeight;
//   context.drawImage(video, 0, 0);

//   canvas.toDataURL("image/jpeg").replace(/^data:image\/jpeg;base64,/, "");

//   let imageData = canvas.toDataURL("image/jpeg");
//   const imageField = document.createElement("input");
//   imageField.setAttribute("type", "hidden");
//   imageField.setAttribute("name", "image");
//   imageField.setAttribute("value", imageData);

//   const form = document.querySelector("form");
//   form.appendChild(imageField);
// });
