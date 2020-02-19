#set FLASK_APP=vote
#set FLASK_ENV=development
#flask run --host 192.168.10.45

from datetime import datetime
from flask import Flask, request, jsonify, render_template
from konlpy.tag import Komoran
import sys
import csv

app = Flask(__name__)
# with open('./vote/static/data.csv', 'r', 'utf-8') as f:
#     reader = csv.reader(f)
#     a_list = list(reader)
#     print(a_list)
# for line in rdr:
#     print(line)
#     if count != 0:
#         vote1 = int(line[1])/int(line[5])
#         vote2 = int(line[2])/int(line[5])
#         turnout = int(line[4])/int(line[3])
#         status = int(line[5])/int(line[4])
#         lst = [vote1, vote2, turnout, status]
#         data[line[0]] = lst
#     count += 1
# print(data)



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
    content_morphs = Komoran.pos(content)
    nnp_lst = [morph for (morph, key) in content_morphs if key == 'NNP']



@app.route('/morphs', methods=['POST'])
def Morphs():
    print(1)
    content = request.get_json()
    content = content['userRequest']['utterance']
    komoran = Komoran(userdic='./user_dic.txt')

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

@app.route('datetime', methods=['POST'])
def Datetime():
    time1 = datetime(2020, 4, 15)
    time2 = datetime.now()
    time_cal = str(-(time2 - time1).days)
    dataSend = {
        "version": "2.0",
        "data": {
            "datetime": time_cal
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