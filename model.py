import cv2
import pytesseract


# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text_with_ink_color(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text
# C:\Users\shreeji soni\Desktop\flask_task\train\IMG20231119120652.jpg
image_path = r'C:\\Users\\shreeji soni\\Desktop\\flask_task\\train\\IMG20231119120652.jpg'
data=extract_text_with_ink_color(image_path)
print(data)


