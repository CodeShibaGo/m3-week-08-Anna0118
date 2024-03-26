from faker import Faker
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

from app.models import Post
from app import app, db

# 初始化 Faker
fake = Faker()

# 假設想為 user_id=105 生成 3 條隨機貼文
user_id = 103
num_posts = 3

with app.app_context():
    for _ in range(num_posts):
        # 生成隨機的貼文內容和時間戳
        body = fake.sentence(nb_words=6)  # 生成一個包含 6 個單詞的句子
        timestamp = datetime.now(timezone.utc)  # 使用當前時間作為貼文時間戳
        post = Post(body=body, timestamp=timestamp, user_id=user_id)

        # 將生成的貼文添加到資料庫
        db.session.add(post)
        db.session.commit()
print(f"Inserted {num_posts} posts for user_id {user_id}.")
