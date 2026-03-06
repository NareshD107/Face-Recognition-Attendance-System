import cv2
import face_recognition
import numpy as np
import pickle
import os

class RecognitionEngine:
    def __init__(self, encodings_path="encodings.pickle", tolerance=0.6):
        self.encodings_path = encodings_path
        self.tolerance = tolerance
        self.data = self.load_encodings()
        
        # Blink detection constants
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 2
        
    def load_encodings(self):
        """Loads face encodings from the pickle file."""
        if not os.path.exists(self.encodings_path):
            print(f"[ERROR] {self.encodings_path} not found.")
            return {"encodings": [], "names": []}
        
        try:
            with open(self.encodings_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load encodings: {e}")
            return {"encodings": [], "names": []}

    @staticmethod
    def eye_aspect_ratio(eye):
        """Calculates the Eye Aspect Ratio (EAR) for blink detection."""
        A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
        B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
        C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
        return (A + B) / (2.0 * C)

    def process_frame(self, frame, blink_state=None):
        """
        Processes a single frame for detection, recognition, and liveness.
        Args:
            frame: BGR image from OpenCV
            blink_state: Dictionary tracking blink status per user
        Returns:
            processed_data: List of dicts containing {name, location, confidence, has_blinked}
        """
        if blink_state is None:
            blink_state = {}

        # Resize for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect and Encode
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame, face_locations)

        results = []

        for encoding, location, landmarks in zip(face_encodings, face_locations, face_landmarks_list):
            name = "Unknown"
            confidence = 0.0
            has_blinked = False

            if self.data["encodings"]:
                # Match
                matches = face_recognition.compare_faces(self.data["encodings"], encoding, tolerance=self.tolerance)
                face_distances = face_recognition.face_distance(self.data["encodings"], encoding)
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.data["names"][best_match_index]
                        # Convert distance to confidence (approximate)
                        distance = face_distances[best_match_index]
                        confidence = round((1 - distance) * 100, 2)

            # Blink Detection (Liveness)
            if name != "Unknown":
                if name not in blink_state:
                    blink_state[name] = {"consec_frames": 0, "has_blinked": False}
                
                left_eye = landmarks.get('left_eye')
                right_eye = landmarks.get('right_eye')
                
                if left_eye and right_eye:
                    ear = (self.eye_aspect_ratio(left_eye) + self.eye_aspect_ratio(right_eye)) / 2.0
                    
                    if ear < self.EYE_AR_THRESH:
                        blink_state[name]["consec_frames"] += 1
                    else:
                        if blink_state[name]["consec_frames"] >= self.EYE_AR_CONSEC_FRAMES:
                            blink_state[name]["has_blinked"] = True
                        blink_state[name]["consec_frames"] = 0
                
                has_blinked = blink_state[name]["has_blinked"]

            # Scale location back up (since we processed at 1/4 size)
            top, right, bottom, left = [coord * 4 for coord in location]
            
            results.append({
                "name": name,
                "location": (top, right, bottom, left),
                "confidence": confidence,
                "has_blinked": has_blinked
            })

        return results, blink_state
