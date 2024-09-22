
# Virtual Mouse Application

A Python application that allows you to control your computer mouse using hand gestures detected by your webcam. This project utilizes OpenCV and MediaPipe for hand detection and PyAutoGUI for mouse control.

## Features

- **Scroll**: Scroll up and down using hand gestures.
- **Volume Control**: Adjust the volume using finger gestures.
- **Cursor Control**: Move the mouse cursor and click using hand movements.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI



## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/rkishanCodes/Virtual-Mouse.git
   cd Virtual-Mouse
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python virtual_mouse.py
   ```
4. Access the application using the webcam to start controlling the mouse with hand gestures.
5. To exit the application, press the `q` key.

## File Structure

```
/virtual_mouse
    ├── virtual_mouse.py       # Main application code
    └── hand_detector.py        # Hand detection module
```

## Troubleshooting

- Ensure your webcam is connected and accessible.
- If you encounter issues, check for any missing libraries or dependencies.

## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes.



