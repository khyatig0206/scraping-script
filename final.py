import json
from reqbody import generate_request_body
import requests
import csv

csv_file_path = 'doctors.csv'

# Open and read the CSV file
with open(csv_file_path, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Iterate over each row in the CSV file
    for href in csvreader:
        
        # print(href)
        body = generate_request_body(href[0])

        # Print the body for debugging
        # print("Request Body:", body)

        url = "https://www.justdial.com/api/detail?searchReferer=gen|lst"

        # Define the headers (without the Cookie header)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "requestTime": "2024-8-21 5:23:01 pm",
            "securityToken": "2a282a2c202a292d2a2b2829",  # This may need to be refreshed
            "Origin": "https://www.justdial.com",
            "Cookie":"ppc=; _abck=3CE4EAA56AFA091EA488B23D44DBE0E0~-1~YAAQT2w/F7yIMmeRAQAApa1WdAxVxm7lfugp05X8eQ2oNnhZoteMwA83r6I8MpghZ8vGebQ3XzNTmniDavCqoiQDCW0GJMxwmtWZmZkgzekQMzwk0wkRpu2QN+DbZTFul6xxUb1Ymox4iFSm2xdu930V6MpjkdDERAqA16+xno59D+g+KGb4EcO9CHVkzf+mWvkw98Opz+CqyaR/Spp/xaHBxHRN0/lmbgUsnGRGa5b8ydc1COVWRDmH99+6WkBH9xSELqRi+ZnvHl8VCG+FvQRPxZMuNUaiZwxhADZmhu1hqxINmV3bfKGLi3bkH7xhU6R72ZyoDJXsaKRAhhiOjdLKt+FtgjmQ3H+fVAt3cn1/WTljpSqdBG3gQSVUBk/ml981VYdEyXBRYn71D8XnA3Ig9K2sc5aT2Yk=~0~-1~1724237243; bm_sz=FC678ECFF173FFFF99FEC7A9D0577EC7~YAAQT2w/F64SLmeRAQAAYNBTdBjMDS5qIa6HW7q9knm6R+RuKYunVrZV67Yq8Aj0CBYuUHYWpua9ir0HGpH84ssjHjBRDBtsdm/33gcRi9/hdo0CrDtBrVx+/zLlV2ODe9AOf69wkc9LcthXSBTKKOuPY1Lf5+t3iYLyJ5CT6qPyod15z1VKdDrVm0IBPzw+GfMeKl5gTGWBQ66mqyQaokc5FW47gTyLh7ngSJF/wu6dSBcWmBEBkhxFvUJXVY23DEHAQNbOyD8aCQfooimSaZBokhNYiuUFPijZe0fb7z+TxQWN/pDG8dyGQJf5LPlN7dx9LitzktvvWbq+gR6601Ay2rEnE2wZ0+rHj1JV9A==~3551298~4600118; Ak_City=JHANSI; Continent=AS; touch=3859654848.11043.0000"
        }

        # Print headers for debugging
        # print("Headers:", headers)

        # Make the POST request
        response = requests.post(url, headers=headers, json=json.loads(body))
        data_hi=response.json()
        data = data_hi.get('results', {})

        # Create the details object with the specific fields
        details = {
            "DrName": data.get('contactperson', ''),
            "FirmName": data.get('name', ''),
            "email": data.get('email', ''),
            "YOEstablishment": data.get('YOE', ''),
            "totJdReviews": data.get('totJdReviews', ''),
            "building": data.get('building', ''),
            "street": data.get('street', ''),
            "area": data.get('area', ''),
            "pincode": data.get('pincode', ''),
            "PhoneNumber": data.get('VNumber', ''),
            "city": data.get('city', ''),
            "qualification": data.get('qualification', ''),
            "award_certificate": data.get('award_certificate', ''),
            "Firm_Images": data.get('catalog_slider', []),
            "addressln": data.get('addressln', ''),
            "categories": [item.get('category', '') for item in data.get('AlsoListedIn', [])],
        }
        print("Response Status Code:", response.status_code)
                # print("Response Headers:", response.headers)
        print("Response Body:", details)