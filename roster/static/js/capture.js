const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const photo = document.getElementById("photo");
const captureBtn = document.getElementById("captureBtn");
const imageData = document.getElementById("imageData");

// Access webcam
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error("Error accessing camera:", error);
  });

// Capture image
captureBtn.addEventListener("click", () => {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataURL = canvas.toDataURL("image/jpeg");
  photo.setAttribute("src", dataURL);
  imageData.value = dataURL;
});
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
