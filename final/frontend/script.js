function login() {
    let username = document.getElementById("username").value;
    if (username.trim() === "") {
        alert("Please enter your name!");
    } else {
        localStorage.setItem("username", username);
        window.location.href = "dashboard.html"; // Redirect to dashboard
    }
}

// Open webcam when attendance page loads
document.addEventListener("DOMContentLoaded", () => {
    let videoElement = document.getElementById("video");
    if (videoElement) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoElement.srcObject = stream;
            })
            .catch(error => {
                console.error("Error accessing webcam:", error);
                alert("Could not access webcam. Please check your permissions.");
            });
    }
});

// Function to capture image from video feed
function captureFace() {
    let username = localStorage.getItem("username");

    if (!username) {
        alert("Please log in first!");
        return;
    }

    let video = document.getElementById("video");
    let canvas = document.createElement("canvas");
    let context = canvas.getContext("2d");

    // Set canvas size equal to video frame
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64 image
    let imageData = canvas.toDataURL("image/png");

    fetch("http://127.0.0.1:5000/capture", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: username, image: imageData })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error. Try again later.");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        window.location.href = "dashboard.html";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to mark attendance. Please try again.");
    });
}

function startRecognition() {
    fetch("http://127.0.0.1:5000/recognize")
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error. Try again later.");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Recognition failed. Please try again.");
    });
}
