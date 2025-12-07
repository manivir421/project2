#comp 3450 <Ashima,ripan>
import cv2
import mediapipe as mp
import numpy as np

def overlay_lipstick(frame, landmarks, lipstick_color, alpha=0.6):
    """
    Overlay a lipstick color onto the lip region of the face.
    
    Parameters:
    - frame: The video frame (BGR).
    - landmarks: A list of normalized face landmark points.
    - lipstick_color: The BGR color tuple for the lipstick.
    - alpha: The transparency factor for blending.
    """
    lips_indices = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 
                    78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
    
    h, w, _ = frame.shape
    lip_points = []
    for idx in lips_indices:
        if idx < len(landmarks):  # Ensure index is valid
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            lip_points.append([x, y])
    
    if len(lip_points) == 0:
        return frame  # Return original frame if no valid landmarks
    
    lip_points = np.array(lip_points, np.int32)
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [lip_points], lipstick_color)
    
    blended_frame = cv2.addWeighted(frame, 1.0, mask, alpha, 0)
    return blended_frame

def main():
    cap = cv2.VideoCapture(0)
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    lipstick_shades = [
        (0, 0, 255),       # Bright red
        (147, 20, 255),    # Deep magenta
        (255, 105, 180)    # Light pink
    ]
    shade_index = 0
    current_color = lipstick_shades[shade_index]
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                frame = overlay_lipstick(frame, face_landmarks.landmark, current_color, alpha=0.6)
        
        cv2.putText(frame, "Press 'n' for next shade, 'q' to quit.", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Virtual Lipstick", frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('n'):
            shade_index = (shade_index + 1) % len(lipstick_shades)
            current_color = lipstick_shades[shade_index]
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
