# 🖱️ Virtual Mouse

[![Python](https://img.shields.io/badge/Python-blue)](https://www.python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-green)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-orange)](https://developers.google.com/mediapipe)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-yellow)](https://pyautogui.readthedocs.io/)

---

## Overview

The **Virtual Mouse** is a Python-based project that enables **mouse control using hand gestures**. With the help of a webcam, the system detects hand landmarks using **MediaPipe** and translates gestures into mouse actions such as moving the cursor, left click, right click, and scrolling.

This project leverages **OpenCV** for video processing, **MediaPipe** for real-time hand tracking, and **PyAutoGUI** for simulating mouse events.

---

## Features

- 🎯 **Cursor Control**: Move the mouse pointer using your index finger.
- 🖱️ **Left Click**: Raise index and middle fingers together.
- 🖱️ **Right Click**: Raise index, middle, and ring fingers.
- ⬆️ **Scroll Up**: Raise four fingers.
- ⬇️ **Scroll Down**: Raise all five fingers.
- 🔄 **Smooth Movement**: Adjustable smoothening for stable control.
- ⛔ **Active Area Boundary**: Prevents cursor from jumping outside frame edges.

---

## Directory Structure
```
virtual-mouse
│
├── virtual_mouse.py        # Main project script
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/virtual-mouse.git
cd virtual-mouse
```

2. Create a virtual environment (recommended):

For Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

1. Run the script:
```bash
python virtual_mouse.py
```

2. Raise your hand in front of the webcam and perform gestures:
   - ☝️ Index finger → Move cursor
   - ✌️ Index + Middle → Left click
   -    Index + Middle + Ring → Right click
   - ✋ Four fingers → Scroll up
   - 🖐️ Five fingers → Scroll down

3. Press **'q'** to exit the program.

---

## Technologies Used

- **Python 3**
- **OpenCV** → For video capture & image processing
- **MediaPipe** → For real-time hand tracking
- **PyAutoGUI** → For mouse control automation
- **NumPy** → For numerical operations

---

## Future Improvements

- 🛠️ Add customizable gesture mappings
- 🖐️ Multi-hand support
- ✍️ Drag & Drop functionality
- ⚡ Performance optimizations for low-end systems

---

## Contact

📧 For questions, suggestions, or collaborations, feel free to reach out:

- GitHub: [tayyabalitech](https://github.com/tayyabalitech)
- LinkedIn: [tayyabalitech](https://www.linkedin.com/in/tayyabalitech)
- Email: [tayyabalitechpro@gmail.com](mailto:tayyabalitechpro@gmail.com)

---

## Made with ❤️ by Tayyab Ali
