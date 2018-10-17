# from PIL import Image
#
# import pytesseract
#
# text = pytesseract.image_to_string(Image.open('/Users/wjb/Desktop/test.png'),lang='chi_sim')
# print(text)

from aip import AipOcr
import re

appId = '14413062'
apiKey = 'KbvjcBhzuqILYefFp9Hf0RkY'
secretKey = 'zyUaYPAZlVxOsDWQBERogWxXwVulxCoU'

client = AipOcr(appId,apiKey,secretKey)

f = open('/Users/wjb/Desktop/test.png','rb')
img = f.read()

message = client.basicGeneral(img)

# print(message)

for i in message.get('words_result'):
    print(i.get('words'))
