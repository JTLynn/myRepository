from flask import Flask, request, jsonify
from models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from werkzeug.security import generate_password_hash, check_password_hash
from function import *

app = Flask(__name__)

mysql_connect_url = 'mysql+pymysql://username:password@localhost/dbname'
# 配置MySQL数据库URI
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connect_url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# 未登录页面
@app.route('/')
def hello():
    return 'MiniProgram-api page'

#登录
@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            # 获取前端json数据
            data = request.get_json()
            # 从json数据中获取用户id和密码
            rec_id= data['userid']
            rec_password = data['password']
            if not rec_id or not rec_password:
                return jsonify('no data')
            if len(rec_id) == 8:
                # 从数据库中查询用户信息
                db_data = user.query.filter_by(user_id=rec_id).first()
                if db_data:
                    db_user = db_data.to_dict()
                    db_pwd = db_user.get('user_password')
                    if check_password_hash(db_pwd, rec_password):
                        return_data = {
                            'user_id': db_user.get('user_id'),
                            'user_name': db_user.get('user_name'),
                            'user_age': db_user.get('user_age'),
                            'user_gender': db_user.get('user_gender'),
                            'user_email': db_user.get('user_email'),
                            'user_phone': db_user.get('user_phone'),
                            'user_academy': db_user.get('user_academy')
                        }
                        return jsonify({**return_data, 'message': 'login success'})
                    else:
                        return jsonify('password incorrect')
                else:
                    return jsonify('user not found')
            elif len(rec_id) == 6:
                db_data = manager.query.filter_by(manager_id=rec_id).first()
                if db_data:
                    db_manager = db_data.to_dict()
                    db_pwd = db_manager.get('manager_password')
                    if check_password_hash(db_pwd, rec_password):
                        return_data = {
                            'manager_id': db_manager.get('manager_id'),
                            'manager_name': db_manager.get('manager_name'),
                            'manager_email': db_manager.get('manager_email'),
                            'manager_phone': db_manager.get('manager_phone')
                        }
                        return jsonify({**return_data, 'message': 'login success'})
                    else:
                        return jsonify('manager not found')
            else:
                return jsonify('id incorrect')
        else:
            return jsonify('post failed')
    except Exception as e:
        return jsonify({'error':str(e)})

#注册
@app.route('/register', methods=['GET','POST'])
def register():
    try:
        if request.method == 'POST':
            # 获取前端json数据
            if not(request.josn):
                return jsonify('no josn')
            else:
                data = request.get_json()
                rec_id= data['userid']
                rec_password = data['password']
                rec_age = data['age']
                rec_gender = data['gender']
                rec_name = data['name']
                rec_email = data['email']
                rec_academy = data['academy']
                rec_phone = data['phone']
                if rec_id and rec_password and rec_age and rec_gender and rec_name and rec_email and rec_academy and rec_phone:
                    if(len(rec_id) == 8):   # 判断id长度是否为8,是否符合用户要求
                            # 从数据库中查询用户信息
                        db_data = user.query.filter_by(user_id=rec_id).first()
                        if db_data is None:
                            # 生成哈希密码
                            rec_password = generate_password_hash(rec_password)
                            # 创建新用户对象
                            new_user = user(user_id=rec_id, user_name=rec_name, user_age=rec_age,
                                            user_gender=rec_gender, user_password=rec_password, user_email=rec_email,
                                            user_academy=rec_academy, user_phone=rec_phone)

                            # 将新用户对象添加到数据库会话中
                            db.session.add(new_user)
                            # 提交数据库会话
                            db.session.commit()
                            return jsonify('register success')
                        else:
                            return jsonify('user already exists')
                    else:
                        return jsonify('id length incorrect')
                else:
                    return jsonify('missing required fields')
        else:
            return jsonify('post failed')
    except Exception as e:
        return jsonify({'error':str(e)})


# 搜索帖子
@app.route('/user/homepage', methods=['GET','POST'])
def homepage():
    try:
        if request.method == 'POST':
            # 获取前端json数据
            data = request.get_json()
            if not(request.josn):
                return jsonify('no json')
            else:
                # 获取数据中的帖子title
                rec_title = data['post_title']        
                if rec_title is None:
                    return jsonify('title is null')
                else:
                    result = search_post(rec_title)
                    return result
        else:
            return jsonify('post failed') 
    except Exception as e:
        return jsonify({'error':str(e)})

# 展示帖子
@app.route('/user/showpost', methods=['GET','POST'])
def show_post():
    try:
        if request.method == 'POST':
             # 从数据库中查询所有帖子
            posts = post.query.all()
            post_list = []
            for post in posts:
                post_list.append(post.to_dict())
            return jsonify(post_list)
    except Exception as e:
        return jsonify({'error':str(e)})

# 排行榜
@app.route('/user/chart', methods=['GET','POST'])
def chart():
    try:
        if request.method == 'POST':
            result = getchart()
            return result
        else:
            return jsonify('post failed')
    except Exception as e:
        return jsonify({'error':str(e)})

# 发帖
@app.route('/user/post', methods=['GET','POST'])
def post():
    try:
        if request.method == 'POST':
            # 获取前端json数据
            if not(request.josn):
                return jsonify('no json')
            else:
                data = request.get_json()
                # 获取数据中的帖子title
                rec_title = data['post_title']
                rec_content = data['post_content']
                rec_type = data['post_type']
                rec_img = data['post_img']
                rec_author = data['post_author']
                rec_time = data['post_time']
                # 初始化点赞数和评论数为0
                rec_comment = 0
                rec_like = 0
                rec_post = post(post_title=rec_title, post_content=rec_content, 
                            post_type=rec_type, post_img=rec_img, post_author=rec_author,
                            post_time=rec_time, post_comment=rec_comment, post_like=rec_like)
                # 将新用户对象添加到数据库会话中
                db.session.add(rec_post)
                # 提交数据库会话
                db.session.commit()
                return jsonify('post success')
        else:
            return jsonify('post failed')
    except Exception as e:
        return jsonify({'error':str(e)}) 
    
# 获取评论
@app.route('/user/comment', methods=['GET','POST'])
def comment():
    try:

        if request.method == 'POST':
            # 获取前端json数据
            if not(request.josn):
                return jsonify('no json')
            else:
                data = request.get_json()
                # 获取数据中的帖子title
                rec_comment = data['post_comment']
                rec_author = data['post_author']
                rec_time = data['post_time']
                rec_post_id = data['post_id']
                if rec_comment is None:
                    return jsonify('comment is null')
                else:
                    db.session.add(rec_comment)
                    db.session.commit()
                    return jsonify('comment success')
        else:
            return jsonify('post failed')
    except Exception as e:
        return jsonify({'error':str(e)}) 
    

#发评论
@app.route('/user/create_comment', methods=['GET','POST'])
def create_comment():
    try:
        if request.method == 'POST':
            data = request.get_json()
            # 从前端获取评论内容、评论用户 
            comment_content = data.get('comment_content')
            comment_author = data.get('comment_author')
            if comment_content and comment_author :
                new_comment = comment(comment_content=comment_content, 
                                    comment_author=comment_author,)
                db.session.add(new_comment)
                db.session.commit()
                return jsonify({'message': 'Comment created successfully'})
            else:
                return jsonify({'error': 'Missing required fields'})
    except Exception as e:
        return jsonify({'error': str(e)})
    

# 删评论
@app.route('/user/delete_comment', methods=['DELETE'])
def delete_comment():
    try:
        if request.method == 'DELETE':
            data = request.get_json()
            rec_comment_id = data.get('comment_id')
            if rec_comment_id:
                comment_to_delete = comment.query.filter_by(comment_id=rec_comment_id).first()
                if comment_to_delete:
                    db.session.delete(comment_to_delete)
                    db.session.commit()
                    return jsonify({'message': 'Comment deleted successfully'})
                else:
                    return jsonify({'error': 'Comment not found'})
            else:
                return jsonify({'error': 'Invalid comment ID'})
    except Exception as e:
        return jsonify({'error': str(e)})

# 更新评论
@app.route('/user/update_comment', methods=['PUT'])
def update_comment():
    try:
        if request.method == 'PUT':
            data = request.get_json()
            rec_comment_id = data.get('comment_id')
            new_content = data.get('comment_content')
            if rec_comment_id and new_content:
                comment_to_update = comment.query.filter_by(comment_id=rec_comment_id).first()
                if comment_to_update:
                    comment_to_update.comment_content = new_content
                    db.session.commit()
                    return jsonify({'message': 'Comment updated successfully'})
                else:
                    return jsonify({'error': 'Comment not found'})
            else:
                return jsonify({'error': 'Invalid comment ID or missing new content'})
    except Exception as e:
        return jsonify({'error': str(e)})
    

# 我的点赞
@app.route('/user/mylikes', methods=['GET', 'POST'])
def user_likes():
    try:
        if request.method == 'POST':
            # 获取前端 json 数据
            data = request.get_json()
            user_id = data.get('user_id')
            if user_id:
                # 从数据库中查询用户的点赞信息
                user_likes = get_user_likes(user_id)
                if user_likes:
                    return jsonify(user_likes)
                else:
                    return jsonify('No likes found')
            else:
                return jsonify('Invalid user ID')
        else:
            return jsonify('Method not allowed')
    except Exception as e:
        return jsonify({'error': str(e)})

# 创建点赞
@app.route('/user/create_like', methods=['POST'])
def create_like():
    try:
        if request.method == 'POST':
            data = request.get_json()
            rec_user_id = data.get('user_id')
            rec_post_id = data.get('post_id')
            if rec_user_id and rec_post_id:
                new_like = mylikes(user_id=rec_user_id, post_id=rec_post_id)
                db.session.add(new_like)
                db.session.commit()
                return jsonify({'message': 'Like created successfully'})
            else:
                return jsonify({'error': 'Invalid user ID or post ID'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
# 删除点赞
@app.route('/user/delete_like', methods=['DELETE'])
def delete_like():
    try:
        if request.method == 'DELETE':
            data = request.get_json()
            rec_like_id = data.get('mylike_id')
            if rec_like_id:
                like_to_delete = mylikes.query.filter_by(mylike_id=rec_like_id).first()
                if like_to_delete:
                    db.session.delete(like_to_delete)
                    db.session.commit()
                    return jsonify({'message': 'Like deleted successfully'})
                else:
                    return jsonify({'error': 'Like not found'})
            else:
                return jsonify({'error': 'Invalid like ID'})
    except Exception as e:
        return jsonify({'error': str(e)})

# 更新点赞
@app.route('/user/update_like', methods=['PUT'])
def update_like():
    try:
        if request.method == 'PUT':
            data = request.get_json()
            rec_like_id = data.get('mylike_id')
            new_user_id = data.get('user_id')
            new_post_id = data.get('post_id')
            if rec_like_id:
                like_to_update = mylikes.query.filter_by(mylike_id=rec_like_id).first()
                if like_to_update:
                    if new_user_id:
                        like_to_update.user_id = new_user_id
                    if new_post_id:
                        like_to_update.post_id = new_post_id
                    db.session.commit()
                    return jsonify({'message': 'Like updated successfully'})
                else:
                    return jsonify({'error': 'Like not found'})
            else:
                return jsonify({'error': 'Invalid like ID'})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)