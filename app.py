from flask import Flask, request, jsonify, current_app
from sqlalchemy import create_engine, text
import json

# app = Flask(__name__)

#############################################################

def create_app(test_config=None):
    app = Flask(__name__)
    #  1) create_app이라는 함수를 정의한다.
    # Flask가 create_app이라는 이름의 함수를 자동으로 팩토리(factory) 함수로 인식해서 해당 함수를 통해 Flask를 실행시킨다.
    # 그리고 create_app 함수가 test_config 인자를 받는다.
    # test_config는 단위 테스트(unit test)를 실행시킬 때 테스트용 데이터베이스 등의 테스트 설정 정보를 적용하기 위함이다.

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    app.json_encoder = json.CustomJSONEncoder

    if test_config is None:  # 2) 만일 test_conig 인자가 None이면 config.py파일에서 설정을 읽는다.
        app.config.from_pyfile("config.py")
    else: # 만일 test_config 인자가 None이 아니라면, 즉, test_config 값이 설정되어 들어왔다면, 단위 테스트를 실행 할 수 있다.
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    # 3) sqlalchemy의 create_engine 함수를 사용해서 데이터베이스의 연결을 한다.
    app.database = database
    # 4)  3)에서 생성한 Engine 객체를 Flask 객체에 저장함으로써 create_app 함수를 외부에서도 데이터베이스를 사용할 수 있도록 한다.

    return app
    # 5) Flask 객체를 리턴한다. 앞서 create_app이라는 함수는 Flask가 자동 인지하여 Flask객체를 찾아서 실행될 수 있다.

### 정리 ###################################################
# - SQLAlchemy의 create_engine 함수를 사용하여 데이터베이스에 연결하고 text 함수를 사용하여 실행시킬 SQL구문을 전달할 수 있다.
# - Flask가 create_app이라는 이름의 함수를 자동으로 팩토리(factory) 함수로 인식해서 해당 함수를 통해서 Flask를 실행한다.
#############################################################

#if __name__ == '__main__':
#    app.run()
