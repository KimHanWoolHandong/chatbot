#flask run --host 192.168.10.45


from flask import Flask, request, jsonify, render_template
#from konlpy.tag import Komoran
import sys

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route("/image")
def home():
    return render_template('d3.html')

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