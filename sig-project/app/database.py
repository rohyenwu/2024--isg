import mysql.connector

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

cursor = conn.cursor()

# 데이터베이스 쿼리 실행
cursor.execute("SELECT * FROM yourtable")



# 결과 가져오기
rows = cursor.fetchall()

for row in rows:
    print(row)

# 연결 종료
cursor.close()
conn.close()
