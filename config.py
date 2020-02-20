db = {
    'user'     : 'root',		# 1) 데이터베이스에 접속할 사용자 id
    'password' : 'dlwnsgml1!',		# 2) 데이터베이스 사용자의 비밀번호
    'host'     : 'localhost',	# 3) 접속할 데이터베이스의 주소.
    'port'     : 3306,			# 4) 접속할 데이터베이스의 포트(port)번호. MySQL일 경우 보통 3306포트를 사용한다.
    'database' : 'election_chatbot'		# 5) 실제 연결하고자 하는 데이터베이스 명
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"