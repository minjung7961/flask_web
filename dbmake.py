import pymysql

# db 연결해주는 명령어
db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)
sql = '''
    CREATE TABLE `topic` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(100) NOT NULL,
	`body` text NOT NULL,
	`author` varchar(30) NOT NULL,
    `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
	) ENGINE=innoDB DEFAULT CHARSET=utf8;
'''

sql_2 = '''
    INSERT INTO `topic` 
    (`title`, `body`, `author`) 
    VALUES 
    ('부산', '부산와서 갈매기를 못봤네 ㅠㅠ', '김태경');
'''

sql_3 = '''
    SELECT * FROM busan.topic;
'''
sql_4 = '''
    INSERT INTO `busan`.`users` 
    (`name`, `email`, `username`, `password`) 
    VALUES 
    ('min', 'als@n', 'errorKim', 'jamwa');
'''
# 쿼리문을 날려주기 준비해주는 칭구
cursor = db.cursor() 

# 커서문 db에 날려주기
# cursor.execute(sql_4)
# db적용
# db.commit()
# db 연결 죽임
# db.close()


# 쿼리문 db 에 날려주는 문장 -> execute(쿼리문)
cursor.execute('SELECT * FROM users;')
# cursor.execute(sql_3)
# 쿼리문 결과를 받아와주는 문장
users = cursor.fetchall()
# 결과보쟈아ㅏ
print(users)
# db 연결 죽임
db.close()