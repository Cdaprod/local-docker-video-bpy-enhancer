# enhance_screen_recording.py

import bpy
import sys
import cv2
import numpy as np
from enum import Enum
from typing import Tuple, Optional

class InteractionType(Enum):
    TYPING = 'typing'
    APP_SWITCH = 'app_switch'
    SCROLLING = 'scrolling'
    LOADING = 'loading'
    IDLE = 'idle'
    KEYBOARD_TRANSITION = 'keyboard_transition'

def detect_keyboard_presence(frame, threshold=0.4):
    # [Existing implementation]
    height, width = frame.shape[:2]
    bottom_section = frame[int(height * 0.6):, :]
    gray = cv2.cvtColor(bottom_section, cv2.COLOR_BGR2GRAY)
    
    # Look for horizontal lines characteristic of a keyboard
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi/180, threshold=100,
        minLineLength=width*0.3, maxLineGap=20
    )
    
    if lines is not None and len(lines) > 3:
        return int(height * 0.4)  # Approximate keyboard height
    return 0

def detect_loading_spinner(frame):
    # [Existing implementation]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
        param1=50, param2=30, minRadius=10, maxRadius=40
    )
    return circles is not None

def detect_scrolling_pattern(diff_thresh):
    # [Existing implementation]
    vertical_profile = np.sum(diff_thresh, axis=1)
    continuous_motion = np.count_nonzero(vertical_profile > vertical_profile.mean())
    return continuous_motion > diff_thresh.shape[0] * 0.7

def detect_typing_pattern(diff_thresh, keyboard_height):
    # [Existing implementation]
    text_area = diff_thresh[:-keyboard_height, :]
    changes = np.count_nonzero(text_area)
    area = text_area.shape[0] * text_area.shape[1]
    change_ratio = changes / area
    return 0.01 < change_ratio < 0.2  # Adjust thresholds as needed

def detect_frame_changes(prev_frame, curr_frame, keyboard_height):
    # [Existing implementation]
    height, width = curr_frame.shape[:2]
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray, curr_gray)
    
    # Exclude keyboard area
    mask = np.ones(diff.shape, dtype=np.uint8)
    mask[int(height - keyboard_height):, :] = 0
    diff = cv2.bitwise_and(diff, diff, mask=mask)
    
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # Find contours of the changes
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    if contours:
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        return x, y, w, h
    return None

def detect_interaction_type(curr_frame, prev_frame, prev_keyboard_height) -> Tuple[InteractionType, int]:
    # [Existing implementation]
    height, width = curr_frame.shape[:2]
    curr_keyboard_height = detect_keyboard_presence(curr_frame)
    
    # Check for keyboard transition
    if curr_keyboard_height != prev_keyboard_height:
        return InteractionType.KEYBOARD_TRANSITION, curr_keyboard_height
    
    # Convert frames to grayscale
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate frame difference
    diff = cv2.absdiff(prev_gray, curr_gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # Calculate motion metrics
    motion_pixels = np.count_nonzero(thresh)
    motion_ratio = motion_pixels / (width * height)
    
    # Detect loading spinner
    if detect_loading_spinner(curr_frame):
        return InteractionType.LOADING, curr_keyboard_height
    
    # App switch detection (large motion across whole frame)
    if motion_ratio > 0.4:
        return InteractionType.APP_SWITCH, curr_keyboard_height
    
    # Scrolling detection (vertical motion pattern)
    if detect_scrolling_pattern(thresh):
        return InteractionType.SCROLLING, curr_keyboard_height
    
    # Typing detection (changes in text area above keyboard)
    if curr_keyboard_height > 0 and detect_typing_pattern(thresh, curr_keyboard_height):
        return InteractionType.TYPING, curr_keyboard_height
    
    # Idle state
    if motion_ratio < 0.01:
        return InteractionType.IDLE, curr_keyboard_height
    
    return InteractionType.STATIC, curr_keyboard_height

def apply_interaction_animation(camera, frame, interaction_type, focus_box, resolution):
    # [Existing implementation]
    if interaction_type == InteractionType.APP_SWITCH:
        # Zoom out during app switches
        camera.location.x = 0
        camera.location.y = 0
        camera.data.lens = 35  # Wide angle
        
    elif interaction_type == InteractionType.SCROLLING:
        # Subtle vertical movement during scrolling
        if focus_box:
            x, y, w, h = focus_box
            cam_y = ((y + h/2) / resolution[1] - 0.5) * 10
            camera.location.y = cam_y
            camera.data.lens = 50  # Normal lens
            
    elif interaction_type == InteractionType.LOADING:
        # Slight zoom in during loading
        camera.location.x = 0
        camera.location.y = 0
        camera.data.lens = 55  # Slight zoom in
        
    elif interaction_type == InteractionType.TYPING:
        # Focus on text area above keyboard
        if focus_box:
            x, y, w, h = focus_box
            cam_x = ((x + w/2) / resolution[0] - 0.5) * 10
            cam_y = ((y + h/2) / resolution[1] - 0.5) * 10
            camera.location.x = cam_x
            camera.location.y = cam_y
            camera.data.lens = 60 - (w / resolution[0] * 20)
                
    elif interaction_type == InteractionType.KEYBOARD_TRANSITION:
        # Smooth transition when keyboard appears/disappears
        camera.location.x = 0
        camera.location.y = 0
        camera.data.lens = 50  # Reset lens to normal
            
    elif interaction_type == InteractionType.IDLE:
        # Neutral view during idle
        camera.location.x = 0
        camera.location.y = 0
        camera.data.lens = 50  # Normal lens
    
    # Add keyframes with smooth interpolation
    camera.keyframe_insert(data_path="location", frame=frame)
    camera.data.keyframe_insert(data_path="lens", frame=frame)
        
    # Set smooth interpolation
    if camera.animation_data and camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.handle_left_type = 'AUTO_CLAMPED'
                keyframe.handle_right_type = 'AUTO_CLAMPED'

def setup_scene(video_path, output_path, resolution=(1080, 2340), fps=30):
    # [Existing implementation]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Configure scene settings
    scene = bpy.context.scene
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.fps = fps
    scene.frame_start = 1

    # Set up Video Sequence Editor
    scene.sequence_editor_create()
    bpy.ops.sequencer.movie_strip_add(filepath=video_path, frame_start=1)
    video_strip = scene.sequence_editor.sequences_all[0]

    # Configure output settings for high quality
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.ffmpeg.audio_codec = "AAC"

    return video_strip

def setup_camera():
    # [Existing implementation]
    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    camera.name = "DynamicCamera"
    camera.data.type = 'PERSP'
    camera.location = (0, 0, 10)
    camera.rotation_euler = (0, 0, 0)
    
    # Set camera as the active camera
    bpy.context.scene.camera = camera
    
    return camera

def process_video(video_path, output_path):
    """
    Process the video with enhanced interaction detection and apply camera animations.
    """
    # iPhone XS Max resolution and aspect ratio (9:19.5)
    resolution = (1242, 2688)  # Adjusted for iPhone XS Max
    fps = 30  # Adjust as per your video's FPS
    
    # Setup scene and camera
    video_strip = setup_scene(video_path, output_path, resolution, fps)
    camera = setup_camera()
    
    # Process frames
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_frame = None
    prev_keyboard_height = 0
    
    print(f"Processing {frame_count} frames...")
    
    for frame_num in range(1, frame_count + 1):
        ret, curr_frame = cap.read()
        if not ret:
            break
                
        if prev_frame is not None:
            # Detect interaction type and keyboard presence
            interaction_type, keyboard_height = detect_interaction_type(
                curr_frame, prev_frame, prev_keyboard_height
            )
            
            # Detect focus area based on interaction type
            focus_box = None
            if interaction_type != InteractionType.APP_SWITCH:
                focus_box = detect_frame_changes(
                    prev_frame, 
                    curr_frame,
                    keyboard_height
                )
            
            # Apply appropriate animation
            apply_interaction_animation(
                camera,
                frame_num,
                interaction_type,
                focus_box,
                resolution
            )
            
            prev_keyboard_height = keyboard_height
                
        prev_frame = curr_frame.copy()
            
        # Progress update
        if frame_num % 100 == 0:
            print(f"Processed frame {frame_num}/{frame_count}")
        
    cap.release()
    
    # Set the end frame for rendering
    bpy.context.scene.frame_end = frame_count
    
    print("Rendering final video...")
    # Render the animation headlessly
    bpy.ops.render.render(animation=True, write_still=False, use_viewport=False)
    print("Processing complete!")

if __name__ == "__main__":
    # Ensure the script is run in Blender's Python environment
    if not bpy.context.space_data:
        print("This script must be run in Blender's Python environment.")
        sys.exit()
    
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Process iPhone screen-recorded videos with dynamic camera movements.")
    parser.add_argument('--input', required=True, help='Path to the input video file.')
    parser.add_argument('--output', required=True, help='Path to the output video file.')
    args = parser.parse_args()
    
    # Call the main processing function
    process_video(args.input, args.output)