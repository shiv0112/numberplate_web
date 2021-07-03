import cv2
import imutils
import numpy as np
import pytesseract
import requests
import json
import xmltodict
import re 
import string 
table = str.maketrans('', '', string.ascii_lowercase)

def capture_plate(video):
    vimal_model = cv2.face.LBPHFaceRecognizer_create()
    vimal_model.read('lbph_car_detection.yml')
    cap = cv2.VideoCapture(video)
    fcount=0
    s=0
    while True:
        ret, frames = cap.read()
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        results = vimal_model.predict(gray)
        if results[1] <500:
            confidence = int( 100 * (1 - (results[1])/400) )
        if confidence>= 85:
            fcount =fcount+1
        if fcount == 2:
            cv2.imwrite("C:/Users/sriva/Desktop/Task8/site/static/styles/carcont.jpeg",frames)
            s = 1
        if s==1:
            pytesseract.pytesseract.tesseract_cmd = r'D:\pytesseract\tesseract.exe'
            img = cv2.imread('photo.jpeg',cv2.IMREAD_COLOR)
            img = cv2.resize(img, (500,600) )
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            gray = cv2.bilateralFilter(gray, 13, 15, 15) 
            edged = cv2.Canny(gray, 30, 200) 
            contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
            screenCnt = None
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                    screenCnt = approx
                    break

            if screenCnt is None:
                detected = 0
                print ("No contour detected")
                return " ", " " , False
            
            else:
                detected = 1

            if detected == 1:
                cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
                mask = np.zeros(gray.shape,np.uint8)
                new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
                new_image = cv2.bitwise_and(img,img,mask=mask)

                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx+1, topy:bottomy+1]
                cv2.imwrite("C:/Users/sriva/Desktop/Task8/site/static/styles/number.jpeg",Cropped)
                string = pytesseract.image_to_string(Cropped, config='--psm 11')

                text = re.sub('[^A-Za-z0-9]+', '', string)
                #Removing all Small character (Data Filtering)
                s = text
                result = s.translate(table)
                final_text =result[-10:]
                print(string)
                print(text)
                print(final_text)
                return string, final_text , True

def Car_info(text):
    vehicle_reg_no = text.strip() #insert the correct registration number
    username = "bheem4" #insert your user name
    url = "http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber=" + vehicle_reg_no + "&username="+username
    url=url.replace(" ","%20")
    r = requests.get(url)
    n = xmltodict.parse(r.content)
    k = json.dumps(n)
    df = json.loads(k)
    l=df["Vehicle"]["vehicleJson"]
    p=json.loads(l)
    s="<h3>Your car's details are: </h3>\n"+"Owner name: "+str(p['Owner'])+"\n"+"Car Company: "+str(p['CarMake']['CurrentTextValue'])+"\n"+"Car Model: "+str(p['CarModel']['CurrentTextValue'])+"\n"+"Fuel Type: "+str(p['FuelType']['CurrentTextValue'])+"\n"+"Registration Year: "+str(p['RegistrationYear'])+"\n"+"Insurance: "+str(p['Insurance'])+"\n"+"Vehicle ID: "+str(p['VechileIdentificationNumber'])+"\n"+"Engine No.: "+str(p['EngineNumber'])+"\n"+"Location RTO: "+str(p['Location'])
    return(s)

def final():
        org, text , success =capture_plate('C:/Users/sriva/Desktop/Task8/site/static/new.mp4')
        print(text)

        if success:
                ans=Car_info(text)
                return(ans)
        else:
                return("Sorry, No Number Plated by the Model..Try more stable video ")