# 爬取用户 aadhaar
# 2020-09-08 
# dwh

import requests
from io import BytesIO
import pytesseract
# import muggle_ocr
from PIL import Image
import re
from bs4 import BeautifulSoup
from flask import Flask
from flask import request

app = Flask(__name__) 
# sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

class VerifyReultObject:
    def __init__(self):
        self.gender =''
        self.ageBand = ''
        self.state=''
        self.mobileNumber=''
        self.verifyResult=''
# def __init__(self):
# 验证码url
captchaUrl = "https://resident.uidai.gov.in/CaptchaSecurityImages.php?width=100&height=40&characters=5"
# 验证aadhaarUrl
verifyaadhaarUrl = "https://resident.uidai.gov.in/verify"
a=0

sess = requests.Session()

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'ContentType': 'text/html; charset=utf-8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection' : 'keep-alive',
}

cookies = {

}

# 处理灰度
def convert_img(img, threshold):
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img
# 获取验证码
def _get_captcha():
    response=sess.get(captchaUrl)
    captcha=Image.open(BytesIO(response.content))

    captcha.show()
    captcha=convert_img(captcha, 69.03)
    captcha.show()  #可以打印出图片，供预览

    # imgByteArr = BytesIO()
    # captcha.save(imgByteArr,format='png')
    # result= sdk.predict(image_bytes=imgByteArr.getvalue())
    
    result=pytesseract.image_to_string(captcha,lang='captcha')
    # print(result)    
    return result
# 处理html

def _parse_html(html):
    verifyReult=VerifyReultObject()
    soup = BeautifulSoup(html, 'lxml')
    alertMessage=soup.find('div',class_='alert-message')
    if alertMessage:
        if alertMessage.text=="Please Enter Valid Captcha":
            verifyReult.verifyResult='Invalid Captcha'
    else: 
        authResult=soup.find("div",class_="col-md-10 col-sm-10 col-xs-9 pl-0").find("h2").text
        verifyReult.verifyResult=authResult
        if authResult =='':
           print("123")
        # results=soup.find("div",class_="col-xs-12 my-20").find_all("span",class_="d-block mb-5")
        results=soup.find_all("span",class_="d-block mb-5")
        if results:
            for item in results:
                result=item.text.split(":")
                if 'AgeBand'==result[0].replace(" ",""):
                    verifyReult.ageBand=result[1].strip()
                elif 'Gender' ==result[0].replace(" ",""):
                    verifyReult.gender=result[1].strip()
                elif 'State' ==result[0].replace(" ",""):
                    verifyReult.state=result[1].strip()
                elif 'MobileNumber' ==result[0].replace(" ",""):
                    verifyReult.mobileNumber=result[1].strip()
    return verifyReult 
#作为服务器启动
@app.route('/verifyAadhaar', methods=["GET","POST"])
def _verify_aadhaar():
    if request.method == "GET":
        aadhaarcode = request.args.get('aadhaarcode')
    if request.method =="POST":
        aadhaarcode = request.form['aadhaarcode']
    captcha = _get_captcha()
    captcha=re.sub('[\W_]+','',captcha)
    params = {
    'uidno': aadhaarcode,
    'security_code': captcha,
    'form_action': 'Proceed to Verify',
    'task': 'verifyaadhaar',
    'boxchexked': '0',
    'c597d422d5bb72782694abe33b327dc5': '1',
    } 
    
    html=sess.post(verifyaadhaarUrl, params,headers=headers)
    # # print(html.text)
    verifyaadhaarresult=_parse_html(html.text)
    if verifyaadhaarresult.verifyResult=='Invalid Captcha':
        captcha = _get_captcha()
        captcha=re.sub('[\W_]+','',captcha)
        params = {
        'uidno': aadhaarcode,
        'security_code': captcha,
        'form_action': 'Proceed to Verify',
        'task': 'verifyaadhaar',
        'boxchexked': '0',
        'c597d422d5bb72782694abe33b327dc5': '1',
        } 
        
        html=sess.post(verifyaadhaarUrl, params,headers=headers)
        # # print(html.text)
        verifyaadhaarresult=_parse_html(html.text)

    return verifyaadhaarresult.__dict__





if __name__ == '__main__':
    #启动服务器
    app.run(host='0.0.0.0', port=9002, debug=False)
    # for i in range(1000):
    #     _verify_aadhaar()
    #     print(a) 
    #     print(i)    
    # print(a)    
    # print(a/1000.0)    


    