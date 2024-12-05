# iPhone Screen Recorded Video Enhancer

![License](https://img.shields.io/badge/License-MIT-00B140)
![Blender](https://img.shields.io/badge/Blender-2.80%2B-F5792A?logo=blender&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)

Enhance your iPhone screen-recorded videos with dynamic camera movements and focus effects using Blender and Python. This tool automatically detects user interactions such as typing, app switching, scrolling, and loading, then applies smooth zoom and positioning to highlight the most relevant parts of the screen without distracting from essential elements like the keyboard.

## 📈 Features

- **Automatic Interaction Detection**: Identifies various user interactions (typing, app switching, scrolling, loading, idle) within your screen recordings.
- **Dynamic Camera Movements**: Applies smooth zoom and positioning based on detected interactions to keep the focus on relevant screen areas.
- **Keyboard-Aware Focus**: Avoids zooming into the keyboard area during typing, ensuring the focus remains on the text input.
- **Headless Processing**: Runs entirely in the background using Blender's Python API (`bpy`), eliminating the need for manual video loading or GUI interactions.
- **Optimized for iPhone Portrait Videos**: Tailored for the 9:19.5 aspect ratio of iPhone 10 Pro Max recordings.
- **High-Quality Output**: Renders enhanced videos in high quality with customizable settings.

## 🛠️ Installation

### Prerequisites

- **Blender**: Ensure you have Blender installed. This script is compatible with Blender 2.80 and above.
  - [Download Blender](https://www.blender.org/download/)
  
- **Python Dependencies**: Install required Python packages (`opencv-python`, `numpy`) within Blender's Python environment.

### Installing Python Dependencies

1. Locate Blender's Python executable. This is typically found in Blender's installation directory.

   - **Windows**: `C:\Program Files\Blender Foundation\Blender <version>\<version>\python\bin\python.exe`
   - **macOS**: `/Applications/Blender.app/Contents/Resources/<version>/python/bin/python3.7m`
   - **Linux**: `/usr/share/blender/<version>/python/bin/python3.7m`

2. Open your terminal or command prompt.

3. Install the required packages using `pip`:

   ```bash
   <path_to_blender_python> -m ensurepip
   <path_to_blender_python> -m pip install --upgrade pip
   <path_to_blender_python> -m pip install opencv-python numpy
   ```

   Replace `<path_to_blender_python>` with the actual path to Blender's Python executable.

## 🚀 Usage

Run the script headlessly using Blender's command-line interface. This allows processing without opening Blender's GUI.

### Command Syntax

```bash
blender -b -P enhance_screen_recording.py -- --input /path/to/input.mp4 --output /path/to/output.mp4
```

### Parameters

- `-b`: Runs Blender in background mode (headless).
- `-P enhance_screen_recording.py`: Specifies the Python script to execute.
- `--`: Separates Blender's arguments from the script's arguments.
- `--input`: Path to the input screen-recorded video file.
- `--output`: Path where the enhanced video will be saved.

### Example

```bash
blender -b -P enhance_screen_recording.py -- --input ~/Videos/input.mp4 --output ~/Videos/output_enhanced.mp4
```

## 📚 How It Works

1. **Frame Analysis**: The script analyzes each frame of the input video to detect user interactions.
2. **Interaction Classification**: Determines the type of interaction (typing, scrolling, app switching, etc.) based on motion patterns and specific visual cues.
3. **Camera Adjustment**: Adjusts the camera's position and zoom in Blender to focus on the relevant screen areas while avoiding distractions like the keyboard.
4. **Rendering**: Renders the enhanced video with smooth transitions and dynamic focus effects.

## 🔧 Customization

- **Resolution and FPS**: Adjust the `resolution` and `fps` parameters in the script to match your video's specifications.
- **Detection Thresholds**: Modify thresholds in detection functions (`detect_typing_pattern`, `detect_scrolling_pattern`, etc.) to better suit different video characteristics.
- **Camera Movements**: Tweak the camera movement parameters in `apply_interaction_animation` for desired zoom levels and positions.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Connect with Cdaprod

<div align="center">
  <p>
    <a href="https://youtube.com/@Cdaprod">
      <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube Channel" />
    </a>
    <a href="https://twitter.com/cdasmktcda">
      <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter Follow" />
    </a>
    <a href="https://www.linkedin.com/in/cdasmkt">
      <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
    </a>
    <a href="https://github.com/Cdaprod">
      <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub followers" />
    </a>
    <a href="https://sanity.cdaprod.dev">
      <img src="https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white" alt="Personal Blog" />
    </a>
  </p>
</div>

## 📜 License

This project is proprietary software owned by Cdaprod. All rights reserved.

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/Cdaprod">Cdaprod</a></p>
  <p><em>Making Enterprise Software Awesome!</em></p>
</div>

---

### Additional Notes:

- **Script Location**: Ensure that the `enhance_screen_recording.py` script is placed in the correct directory or provide the full path when executing the Blender command.
  
- **Blender Version Compatibility**: The script is tested with Blender 2.80 and above. Using an unsupported version may lead to unexpected behavior.

- **Performance Considerations**: Processing high-resolution videos can be resource-intensive. Ensure your system meets the necessary requirements and consider processing shorter clips if needed.

- **Error Handling**: The script includes basic error checks, such as verifying that it is run within Blender's Python environment. For advanced error handling, consider expanding the script to log detailed errors.

- **Support**: For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/Cdaprod/iphone-screen-recorded-video-enhancer).