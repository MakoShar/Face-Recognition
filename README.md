# Face Recognition App 🎯

A real-time **face detection and recognition web application** built with JavaScript, Face-API.js, TensorFlow.js, and Python.

The application uses a webcam to detect and recognize registered faces, record recognition events, and track attendance-related activity.

<img width="1918" height="877" alt="Screenshot 2026-08-17 195805" src="https://github.com/user-attachments/assets/afb01d89-a1df-4514-b658-55413b9bab4e" />


## ✨ Features

* 🎥 Real-time face detection through webcam
* 🧠 Face recognition of registered users
* 🟩 Visual feedback for recognized faces
* 🟥 Unknown face detection
* ⏱️ Timestamped recognition logs
* 🟢 Punch-in / Punch-out tracking
* 👥 Currently-online tracking
* 📥 Export recognition records as JSON
* 🚫 Duplicate recognition prevention
* 💾 Local data persistence

## 🛠️ Technologies

* **HTML5 / CSS3** — UI and application structure
* **JavaScript (ES6+)** — Application logic
* **Canvas API** — Face detection overlays
* **WebRTC / MediaDevices API** — Webcam access
* **Face-API.js v0.22.2** — Face detection and recognition
* **TensorFlow.js** — Machine learning runtime
* **Python 3** — Local server and launcher
* **JSON / LocalStorage** — Data storage and export

## 🤖 AI Models

The application uses three Face-API.js models:

| Model                    | Purpose                                    |
| ------------------------ | ------------------------------------------ |
| **SSD MobileNetV1**      | Face detection                             |
| **Face Landmark 68**     | Facial landmark detection                  |
| **Face Recognition Net** | Generates 128-dimensional face descriptors |

### Recognition Pipeline

```bash
Webcam
   ↓
SSD MobileNetV1
   ↓
Face Detection
   ↓
Face Landmark 68
   ↓
Face Recognition Net
   ↓
128-D Face Descriptor
   ↓
FaceMatcher
   ↓
Known / Unknown
```

The current recognition threshold is **0.35**.

```bash
const faceMatcher = new faceapi.FaceMatcher(
    labeledFaceDescriptors,
    0.35
);
```

## 📁 Project Structure

```bash
Face-Recognition/
│
├── index.html
├── launcher.py
├── launch.bat
├── face-api.min.js
│
├── models/
│   ├── ssd_mobilenetv1/
│   ├── face_landmark_68/
│   └── face_recognition/
│
├── Faces/
│   ├── Aaditya_Verma.png
│   └── Anoop_Verma.jpg
│
└── Record/
    └── Local.json
```

## 🚀 Getting Started

### Requirements

* Python 3.x
* Modern web browser
* Webcam
* Camera permission

### Clone the Repository

```bash
git clone https://github.com/MakoShar/Face-Recognition.git
cd Face-Recognition
```

### Run the Application

**Python launcher:**

```bash
python launcher.py
```

**Windows:**

```bash
launch.bat
```

**Manual server:**

```bash
python -m http.server 8000
```

Then open:

```bash
http://localhost:8000
```

> Running through a local HTTP server is recommended for webcam and model access.

## 👥 Adding New Faces

1. Add a clear, front-facing image to the `Faces/` folder.
2. Name it using:

```bash
FirstName_LastName.jpg
```

Example:

```bash
Rahul_Sharma.jpg
```

3. Restart the application.

## ⚙️ Configuration

### Recognition Threshold

Modify the `FaceMatcher` threshold:

```bash
0.35
```

Lower values make recognition stricter.

### Duplicate Prevention

The default duplicate prevention interval is **5 seconds**:

```bash
5000
```

`5000` = 5 seconds.

## 🛠️ Troubleshooting

**Camera not accessible**

* Allow browser camera permissions.
* Make sure another application isn't using the webcam.
* Run the application through the local server.

**Models not loading**

* Check that all folders exist inside `models/`.
* Verify the model files and paths.

**Faces not recognized**

* Use clear, front-facing images.
* Improve lighting.
* Check the recognition threshold.

## 🔮 Future Improvements

* Multiple reference images per user
* Database-backed attendance
* Admin dashboard
* Authentication
* Recognition analytics
* Multi-camera support
* Cloud deployment

## 👨‍💻 Author

**Anoop Verma**


---

⭐ If you find this project useful, consider giving it a star.
