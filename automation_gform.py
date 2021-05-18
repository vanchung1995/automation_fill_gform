import requests
from bs4 import BeautifulSoup
import re
class AutomationFill:
    def __init__(self):
        pass

    def get_question_ids(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        content = soup.body.find_all(text = re.compile('var FB'))

        match = re.findall('[,]["][\w\s]+["][,]', str(content))
        #It will match all the questions in the form
        question_strings = [x.strip('"') for x in match]

        match_ids = re.findall('(?<=\[\[)(\d+)', str(content))
        #It will find all the numbers in the content
        question_ids = ['entry.' + x for x in match_ids[1:]]
        #It will leave the first numbers (they are not the ids)
        return question_ids

    def send_answers(self, url, fname, lname, grade, section, subject): #arrange this as per your form requirements
        ids = self.get_question_ids(url)

        answers = [fname, lname, grade, section, subject]
        response = dict(zip(ids, answers))

        if 'viewform' in url:
            s = url.index('viewform')
            response_url = url.replace(url[s::], 'formResponse?')

        try:
            r = requests.post(response_url, response)
            if r.status_code == 200:
                print(r.text)
                return '[!] Attendence posted !'
            #In case an error happens, it will raise an exception
            else:
                raise Exception

        #After raising the exception it will retry to submit using url reconstruction with prefilled values
        except:
            try:
                ans_list = [x + '=' + y for x, y in zip(ids, answers)]

                for i in range(0, len(ans_list)):
                    response_url += ans_list[i]
                    response_url += '&'

                response_url.strip("&")
                r = requests.get(response_url)
                status = r.status_code

                if status == 200:
                    return '[!] Attendance sent !'
                else:
                    raise Exception
            #If still an error happens, it will print out a message.
            except:
                return '[!] Attendance not sent !'

    def fill_link(self, gform_link, values):
        if not isinstance(values, list):
            raise Exception('values must be list of value')
        field_ids = self.get_question_ids(gform_link)
        if len(field_ids) != len(values):
            raise Exception("Length of values must be equals to field ids length")
        response = dict(zip(field_ids, values))

        if 'viewform' in gform_link:
            s = gform_link.index('viewform')
            response_url = gform_link.replace(gform_link[s::], 'formResponse?')
        try:
            r = requests.post(response_url, response)
            if r.status_code == 200:
                return '[!] Attendence posted !'
            #In case an error happens, it will raise an exception
            else:
                raise Exception

        #After raising the exception it will retry to submit using url reconstruction with prefilled values
        except:
            try:
                ans_list = [x + '=' + y for x, y in zip(field_ids, values)]

                for i in range(0, len(ans_list)):
                    response_url += ans_list[i]
                    response_url += '&'

                response_url.strip("&")
                r = requests.get(response_url)
                status = r.status_code

                if status == 200:
                    return '[!] Attendance sent !'
                else:
                    raise Exception
            #If still an error happens, it will print out a message.
            except:
                return '[!] Attendance not sent !'


if __name__ == '__main__':
    af = AutomationFill()
    gform_link = 'https://docs.google.com/forms/d/e/1FAIpQLSftSH6VDGrJ_iqd1SaTGsu4QiP9eZzgl2p4lIhQplEjeq5JNQ/viewform' #chung form
    # gform_link = 'https://docs.google.com/forms/d/e/1FAIpQLSfrGn49hcbeioNNa25Osp4fwTG2xV3BmmN9-cMWWC2-xvcQyg/viewform'
    fname = 'Your first name here'
    lname = 'Your last name here'
    grade = 'Your grade here'
    section = 'Section here'
    subject = 'Enter subject'

    # print(af.send_answers(gform_link, fname, lname, grade, section, subject))
    # print(af.fill_link(gform_link,[fname, lname, grade, section, subject]))
    chung_answers = ['O1','Chung test Q2',['O1','O2','O3'],'O3','Chung Test Q5']
    print(af.fill_link(gform_link, chung_answers))
