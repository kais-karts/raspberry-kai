// static/js/script.js
const item_names = [
  "Banana",
  "Bomb",
  "redShroom",
  "goldShroom",
  "redShell",
  "blueShell",
  "lightning",
  "bulletBill",
];

// Countdown
const canvas = document.getElementById("countdownCanvas");
const ctx = canvas.getContext("2d");
let countDownDuration = 5000; // Total countdown time in miliseconds
let countDownStart = 0;

function drawArc(elapsedTime, durationTime) {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
  ctx.beginPath();
  ctx.arc(
    canvas.width / 2, // x: The x-coordinate of the center of the arc
    canvas.height / 2, // y: The y-coordinate of the center of the arc
    72, // radius: The radius of the arc
    1.5 * Math.PI + 2 * Math.PI * (elapsedTime / durationTime),
    1.5 * Math.PI, // startAngle: The angle at which the arc starts (in radians)
    false // anticlockwise: A boolean indicating whether the arc should be drawn counter-clockwise (false means clockwise)
  );
  ctx.lineWidth = 8;
  ctx.strokeStyle = "blue";
  ctx.stroke();
  ctx.closePath();
}

drawArc(1, 1);

function updateTimer() {
  let elapsed = new Date().getTime() - countDownStart;
  if (elapsed < countDownDuration) {
    console.log(elapsed, countDownDuration, countDownStart);
    drawArc(elapsed, countDownDuration);
    requestAnimationFrame(updateTimer); // Call the next frame
  } else {
    drawArc(0); // Ensure the arc is fully drawn at the end
    console.log("Countdown finished!");
  }
}

// Show powerup
const images = document.querySelectorAll(".slideshow img");
let index = 0;

function changeImage() {
  images.forEach((img) => img.classList.remove("active"));
  index = (index + 1) % images.length;
  images[index].classList.add("active");
}

function showItem(item) {
  console.log("show item");
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    changeImage();
    if (new Date().getTime() - startTime >= 1000) {
      clearInterval(intervalId);
      images.forEach((img) => img.classList.remove("active"));
      images[item].classList.add("active");
      countDownStart = new Date().getTime();
      countDownDuration = 5000;
      updateTimer();
    }
  }, 100);
  console.log(images[item]);
}

// Websocket

// Connect to the WebSocket server using Socket.IO
const socket = io.connect("http://127.0.0.1:8000/");

// Event listener for successful connection
socket.on("connect", function () {
  console.log("Connected to Flask-SocketIO!");
});

// Listen for messages from the server
socket.on("item_pickup", function (data) {
  console.log("Item Pickup", data.item);

  showItem(data.item);
});

// Event listener for when disconnected
socket.on("disconnect", function () {
  console.log("Disconnected from WebSocket server");
});
