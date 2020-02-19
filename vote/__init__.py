#set FLASK_APP=vote
#set FLASK_ENV=development
#flask run --host 192.168.10.45

from datetime import datetime
from flask import Flask, request, jsonify, render_template
from konlpy.tag import Komoran
import csv
import codecs
import re

app = Flask(__name__)

def data_creating():
    data = {}
    with codecs.open('./vote/static/data.csv', 'r', encoding='utf-8') as csvf:
        rd = csv.reader(csvf)
        next(rd)
        for line in rd:
            vote1 = round(int(line[1]) / int(line[5])*100, 2)
            vote2 = round(int(line[2]) / int(line[5])*100, 2)
            turnout = round(int(line[4]) / int(line[3])*100, 2)
            status = round(int(line[5]) / int(line[4])*100, 2)
            dic = {}
            dic['vote1'] = str(vote1)
            dic['vote2'] = str(vote2)
            dic['turnout'] = str(turnout)
            dic['status'] = str(status)
            data[line[0]] = dic
            data[line[0][:-1]] = dic
    return data


komoran = Komoran(userdic='./user_dic.txt')
data = data_creating()



@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route("/image")
def home():
    return render_template('d3.html')

@app.route('/matching', methods=['POST'])
def Matching():
    content = request.get_json()
    content = content['userRequest']['utterance']
    #형태소 분할
    content_morphs = komoran.pos(content)
    #형태소중에서 고유명사 추출
    nnp_lst = [morph for (morph, key) in content_morphs if key == 'NNP']

    regex = re.compile('\w\w[률율]')
    match = regex.search(content)

    # 도시 하나만 묻는 경우만 한정
    for city in nnp_lst:
        if city in data:
            #목록별 데이터 정리
            result = data[city]
            tell_city = "{}선거 결과".format(city)
            tell_turnout = "투표율 {}%\n".format(result['turnout'])
            tell_vote1 = "OO 후보 {}%\n".format(result['vote1'])
            tell_vote2 = "OO 후보 {}%\n".format(result['vote2'])
            tell_status = "개표율 {}%".format(result['status'])

            if match is None:
                #비율 관련 요청이 없을 경우 종합 정보 제공
                text = tell_city + "(" + tell_turnout + ")\n" + \
                        tell_vote1 + tell_vote2 + tell_status + "기준"
            else:
                #string 형태로 변환
                rate = match.group()
                #알맞게 text 제작
                if rate == "투표율":
                    text = tell_city + " " + tell_turnout
                elif rate == "개표율":
                    text = tell_city + " " + tell_status
                else:
                    text = tell_city + "(" + tell_turnout + ")\n" + \
                           tell_vote1 + tell_vote2 + tell_status + "기준"

            dataSend = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": text
                            }
                        }
                    ]
                }
            }
    return dataSend




@app.route('/morphs', methods=['POST'])
def Morphs():
    print(1)
    content = request.get_json()
    content = content['userRequest']['utterance']
    content_morphs = komoran.pos(content)
    nnp_lst = [morph for (morph, key) in content_morphs if key == 'NNP']
    print(nnp_lst)
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "뽑아온 NNP는 {} 입니다".format(nnp_lst)
                    }
                }
            ]
        }
    }

    return jsonify(dataSend)

@app.route('/datetime', methods=['POST'])
def Datetime():
    time1 = datetime(2020, 4, 15)
    time2 = datetime.now()
    print(time2.day)
    time_cal = str(-(time2 - time1).days)
    dataSend = {
        "version": "2.0",
        "data": {
            "datetime": time_cal,
            "datemonth": str(time2.month),
            "dateday": str(time2.day)
        }
    }

    return jsonify(dataSend)



@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    #print(content)
    content = content['userRequest']['utterance']
    print(content[:3])
    if content[:3] == "분당구":
        print(1)
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "description": "선거구 결과입니다",
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "결과보기",
                                    "webLinkUrl": "http://125.252.26.28:5000/image"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    else:
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "정확히 말씀해주시겠어요?"
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='192.168.10.45')