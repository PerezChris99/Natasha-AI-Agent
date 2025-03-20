import cv2
import face_recognition
import numpy as np
import pickle
import os
from datetime import datetime

class SecuritySystem:
    def __init__(self):
        self.known_faces_file = "known_faces.pkl"
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
        self.camera = None

    def load_known_faces(self):
        if os.path.exists(self.known_faces_file):
            with open(self.known_faces_file, 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_names = data['names']

    def add_face(self, name):
        self.camera = cv2.VideoCapture(0)
        _, frame = self.camera.read()
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            encoding = face_recognition.face_encodings(frame)[0]
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(name)
            self._save_known_faces()
            return f"Added {name} to recognized faces"
        return "No face detected"

    def identify_person(self):
        self.camera = cv2.VideoCapture(0)
        _, frame = self.camera.read()
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            return "No face detected"

        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            if True in matches:
                name = self.known_face_names[matches.index(True)]
                return f"Welcome, {name}"
        return "Unrecognized person detected"

    def _save_known_faces(self):
        with open(self.known_faces_file, 'wb') as f:
            pickle.dump({
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }, f)
