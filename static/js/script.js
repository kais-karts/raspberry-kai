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
const powerUpImages = document.querySelectorAll(".slideshow img");

// Countdown
const canvas = document.getElementById("countdownCanvas");
const ctx = canvas.getContext("2d");
let countDownDuration = 5000; // Total countdown time in miliseconds
let countDownStart = 0;
let timerVisible = false;

function drawArc(elapsedTime, durationTime) {
  console.log("drawArc", elapsedTime, durationTime);
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
  ctx.beginPath();
  const percentage = durationTime == 0 ? 0 : elapsedTime / durationTime;
  ctx.arc(
    canvas.width / 2, // x: The x-coordinate of the center of the arc
    canvas.height / 2, // y: The y-coordinate of the center of the arc
    170, // radius: The radius of the arc
    1.5 * Math.PI, // startAngle: The angle at which the arc starts (in radians)
    1.5 * Math.PI + 2 * Math.PI * percentage,
    true // anticlockwise: A boolean indicating whether the arc should be drawn counter-clockwise (false means clockwise)
  );
  ctx.lineWidth = 8;
  ctx.strokeStyle = "blue";
  ctx.stroke();
  ctx.closePath();
  console.log(1.5 * Math.PI, 1.5 * Math.PI + 2 * Math.PI * percentage);
}

function hidePowerUp() {
  powerUpImages.forEach((img) => img.classList.remove("active"));
}

function updateTimer() {
  let elapsed = new Date().getTime() - countDownStart;
  if (elapsed < countDownDuration && timerVisible) {
    console.log(elapsed, countDownDuration, countDownStart);
    drawArc(elapsed, countDownDuration);
    requestAnimationFrame(updateTimer); // Call the next frame
  } else {
    hideTimer(); // Ensure the arc is fully drawn at the end
    hidePowerUp();
    console.log("Countdown finished!");
  }
}

function showTimer() {
  console.log("show timer");
  drawArc(0.0001, 1);
  timerVisible = true;
}

function hideTimer() {
  console.log("hide timer");
  drawArc(1, 1);
  timerVisible = false;
}

// Show powerup
let index = 0;

function changeImage() {
  powerUpImages.forEach((img) => img.classList.remove("active"));
  index = (index + 1) % powerUpImages.length;
  powerUpImages[index].classList.add("active");
}

function showItem(item) {
  console.log("show item");
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    changeImage();
    if (new Date().getTime() - startTime >= 1000) {
      clearInterval(intervalId);
      powerUpImages.forEach((img) => img.classList.remove("active"));
      powerUpImages[item].classList.add("active");
    }
  }, 100);
  console.log(powerUpImages[item]);
}
const trapImages = document.querySelectorAll(".warning img");
const warningPopup = document.querySelectorAll(".warning");
let imageShowing = false;
function blinkImage(item) {
  if (imageShowing) {
    trapImages[item].classList.remove("active");
  } else {
    trapImages[item].classList.add("active");
  }
  imageShowing = !imageShowing;
}

//Show warning
function showWarning(item) {
  hidePowerUp();
  hideTimer();
  console.log("incoming item");
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    // console.log("warning popup", warningPopup);
    // warningPopup.classList.add("active");
    // document.getElementById("warningDiv").style.backgroundColor = "#2d3747";
    document.getElementById("warningDiv").style.backgroundColor = "red";
    blinkImage(item);
    if (new Date().getTime() - startTime >= 5000) {
      clearInterval(intervalId);
      trapImages[item].classList.remove("active");
      document.getElementById("warningDiv").style.backgroundColor =
        "transparent";
    }
  }, 100);
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
  showTimer();
  showItem(data.item);
  powerUpImages.forEach((img) => img.classList.remove("active"));
});
socket.on("item_hit", function (data) {
  console.log("Item Hit", data.item);

  showWarning(data.item);
});
socket.on("item_use", function (data) {
  console.log("Item Use", data.duration);
  // showTimer(); // TODO: Remove
  if (timerVisible) {
    countDownStart = new Date().getTime();
    countDownDuration = data.duration * 1000;
    updateTimer();
  }
});

// Event listener for when disconnected
socket.on("disconnect", function () {
  console.log("Disconnected from WebSocket server");
});
