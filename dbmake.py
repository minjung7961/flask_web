import pymysql

# db 연결해주는 명령어
db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)

cursor = db.cursor() # 쿼리문을 날려주기 준비해주는 칭구
# 쿼리문 db 에 날려주는 문장 -> execute(쿼리문)
cursor.execute('SELECT * FROM users;')
# 쿼리문 결과를 받아와주는 문장
users = cursor.fetchall()
# 결과보쟈아ㅏ
print(users)