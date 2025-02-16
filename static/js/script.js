// static/js/script.js
item_names = [
  "Banana",
  "Bomb",
  "redShroom",
  "goldShroom",
  "redShell",
  "blueShell",
  "lightning",
  "bulletBill",
];

const images = document.querySelectorAll(".slideshow img");
let index = 0;

function changeImage() {
  images.forEach((img) => img.classList.remove("active"));
  index = (index + 1) % images.length;
  images[index].classList.add("active");
}

// let intervalId = setInterval(changeImage, 100);

function runAnimationFor3Seconds() {
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    changeImage();
    if (new Date().getTime() - startTime >= 3000) {
      clearInterval(intervalId);
      images.forEach((img) => img.classList.remove("active"));
      images[0].classList.add("active");
    }
  }, 100);
}

// runAnimationFor3Seconds();

// Connect to the WebSocket server using Socket.IO
const socket = io.connect("http://127.0.0.1:8000/");

// Event listener for successful connection
socket.on("connect", function () {
  console.log("Connected to Flask-SocketIO!");
});

// Listen for messages from the server
socket.on("item_pickup", function (data) {
  console.log("Item Pickup");
  runAnimationFor3Seconds();
});

// Event listener for when disconnected
socket.on("disconnect", function () {
  console.log("Disconnected from WebSocket server");
});
