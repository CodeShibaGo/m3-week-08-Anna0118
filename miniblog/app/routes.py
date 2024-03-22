from app import app, db, mail
from flask import Flask, request, render_template, redirect, url_for, flash,g
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit
from datetime import datetime, timezone
from flask_mail import Message
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app.translate import translate

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        #  不需要add，因為數據已存在，current_user會自動去追蹤
        db.session.commit()
    g.locale = str(get_locale())


# 首頁
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # print(current_user.is_authenticated)
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post.strip()) == 0:
            flash('Post content cannot be empty.')
            return redirect(url_for('index'))
        try:
            language = detect(post)
        except LangDetectException:
            language = ''
        posts = Post(body=post, author=current_user, language=language)
        db.session.add(posts)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)  # defult當前頁碼為1
    # 撈出有追蹤的用戶的貼文後，進行分頁
    posts = current_user.following_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

# 全部貼文
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# 註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email,
                    password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register')

# 登入


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html',  title='Log In')


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# 忘記密碼(不需寄驗證信版)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email.')
            return redirect(url_for('reset_password'))

        password_new = request.form.get('password_new')
        password_check = request.form.get('password_check')

        if password_new != password_check:
            flash('Passwords do not match.')
            return redirect(url_for('reset_password'))

        user.password_hash = generate_password_hash(password_new)
        db.session.commit()

        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password')

# 個人頁面


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(
        Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


# 編輯個人檔案
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # print(current_user)
        # 從表單獲取資料
        username = request.form.get('username')
        about_me = request.form.get('about_me')
        if not username:
            flash('Username is required.')
            return redirect(url_for('edit_profile'))
        # 不可與資料庫內的username重複
        user = User.query.filter_by(username=username).first()
        if user is not None and user.username != current_user.username:
            flash('This username is already in use. Please use a different username.')
            return redirect(url_for('edit_profile'))
        current_user.username = username
        current_user.about_me = about_me
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile',
                           username=current_user.username,
                           about_me=current_user.about_me)

# 追蹤


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# 退追蹤


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


# 測試db是否連線成功
@app.route('/test_db')
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"


# 發送信件
@app.route('/message')
def send_message():
    msg = Message('Hello', sender=app.config['MAIL_SERVER'],
                  recipients=['bellachu351@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'


@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    data = request.get_json()
    return {'text': translate(data['text'],
                              data['source_language'],
                              data['dest_language'])}
