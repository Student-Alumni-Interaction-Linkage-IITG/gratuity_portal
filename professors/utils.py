import cv2
import numpy as np
from PIL import Image, ImageOps
import io
from django.core.files.base import ContentFile

def process_teacher_photo(professor):
    if not professor.profile_picture:
        return False
        
    try:
        # Open image
        img = Image.open(professor.profile_picture)
        
        # Correct EXIF
        img = ImageOps.exif_transpose(img)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Convert to numpy array for OpenCV
        img_cv = np.array(img)
        # Convert RGB to BGR
        img_cv = img_cv[:, :, ::-1].copy()
        
        # Face detection
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        width, height = img.size
        
        if len(faces) > 0:
            # Get largest face
            faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
            x, y, w, h = faces[0]
            
            # Center of the face
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            
            crop_size = int(max(w, h) * 2.5) # Provide margin around the face
            crop_size = min(crop_size, width, height) # Don't exceed image dimensions
            
            # Calculate top-left corner of the crop
            # We want face_center_y to be at 40% of crop_size
            crop_y = face_center_y - int(crop_size * 0.4)
            crop_x = face_center_x - int(crop_size * 0.5)
            
            # Adjust if out of bounds
            if crop_x < 0:
                crop_x = 0
            elif crop_x + crop_size > width:
                crop_x = width - crop_size
                
            if crop_y < 0:
                crop_y = 0
            elif crop_y + crop_size > height:
                crop_y = height - crop_size
                
            box = (crop_x, crop_y, crop_x + crop_size, crop_y + crop_size)
            cropped_img = img.crop(box)
        else:
            # Fallback: intelligent center crop (square)
            crop_size = min(width, height)
            crop_x = (width - crop_size) // 2
            crop_y = (height - crop_size) // 3 # Shifted slightly up for portraits
            box = (crop_x, crop_y, crop_x + crop_size, crop_y + crop_size)
            cropped_img = img.crop(box)
            
        # Resize to 400x400
        cropped_img = cropped_img.resize((400, 400), Image.Resampling.LANCZOS)
        
        # Save to buffer
        buffer = io.BytesIO()
        cropped_img.save(buffer, format="WEBP", quality=85)
        
        # Save to model
        filename = f"{professor.id}_processed.webp"
        professor.processed_profile_picture.save(filename, ContentFile(buffer.getvalue()), save=False)
        professor.save(update_fields=['processed_profile_picture'])
        return True
    except Exception as e:
        print(f"Error processing {professor.name}: {e}")
        return False
