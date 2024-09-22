from flask import Flask, Blueprint,request, jsonify, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import os
from werkzeug.utils import secure_filename

# from models import db, User, ImageUpload, ExtractionResult



authetication_bp = Blueprint('auth', __name__)



# new user register-----------
@authetication_bp.post('/register')
def register():
    try:
        data = request.json
        username = data.get('username', '')
        name = data.get('name', '')
        email = data.get("email", '')
        mobile_number = data.get("mobile_number", '')
        password = data.get("password", '')

        if not username:
            return jsonify({'error':'Enter valid username'}), 400
        
        if  not name:
            return jsonify({'error':'Enter valid name'}), 400
        
        if  not email:
            return jsonify({'error':'Enter valid Email'}), 400 
               
        if  not mobile_number:
            return jsonify({'error':'Enter valid mobile number'}), 400
        
        if  not password:
            return jsonify({'error':'Enter valid password'}), 400
        cursor = g.db.cursor()

        pswd = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        cursor.execute('INSERT INTO tbl_user (username,name,email,mobile_number,password) VALUES (%s, %s, %s, %s, %s)',
                    (username,name,email,mobile_number,pswd,))
        g.db.commit()
        return jsonify({'message': 'User registered'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



#User_login-----------
@authetication_bp.post('/login')
def login():
     try:
        data = request.json
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        pswd = data.get('password')

        if not email or not pswd:
            return jsonify({'error': 'Invalid name or passowrd'}), 400
        cursor = g.db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM tbl_user WHERE email = %s OR mobile_number=%s AND is_activate=1 AND is_delete=0', (email,mobile_number,))
        user = cursor.fetchone()    
        if user: 
            is_pass_correct = check_password_hash(user["password"], pswd)
            print("data",is_pass_correct)
            if is_pass_correct:
                access = create_access_token(identity=user["id"])
                print("access",access)
                return jsonify({
                    'user': {
                    'access': access,
                    'full_name': user["username"]  
                }
            }), 200
        return jsonify({'message' : 'User not found make registration'}), 404
     except Exception as e:
        return jsonify({'error': str(e)}), 500


import pytesseract
import cv2

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def process_image(image_path):

    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray_image)
    print(extracted_text)
    result = {
        "batch": "B12345",
        "expiry_date": "2025-12-1",
        "manufacturing_date": "2023-02-19",
        "price_mrp": "500"
    }
   
    return result


# Upload an 
@authetication_bp.post('/upload')
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    print('usernameuser_id ',user_id)
    filename = secure_filename(file.filename)
    print("ddddddddddddddddddddddddddd",filename)
    # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # file.save(filepath)

    # Process the image using the model
    result = process_image(filename)
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO tbl_image_upload (user_id,batch,expiry_date,manufacturing_date,price_mrp) VALUES (%s, %s, %s, %s, %s)',
                    (user_id,result['batch'],result['expiry_date'],result['manufacturing_date'],result['price_mrp'],))
    g.db.commit()

   
    return jsonify({'message': 'Data registered successfully',"data":result}), 201

@authetication_bp.get('/get_history/<int:user_id>')
def get_history(user_id):
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM tbl_image_upload WHERE user_id ={user_id}')
    history = cursor.fetchall()
    if history:
        print(history)
        return jsonify({"product_history":history})
    else:
        return jsonify({'error': 'No data found'}), 400
        