from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

# 用户表
class user(db.Model):
    __tablename__ = 'user'
    user_name = db.Column(db.VARCHAR(255), primary_key=True)
    user_id = db.Column(db.INT)
    user_age = db.Column(db.INT)
    user_gender = db.Column(db.VARCHAR(255))
    user_academy = db.Column(db.VARCHAR(255))
    user_password = db.Column(db.VARCHAR(255))
    user_email = db.Column(db.VARCHAR(255))
    user_phone = db.Column(db.INT)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# 管理员表
class manager(db.Model):
    __tablename__ = 'manager'
    manager_id = db.Column(db.INT, primary_key=True)
    manager_name = db.Column(db.VARCHAR(255))
    manager_password = db.Column(db.VARCHAR(255))
    manager_email = db.Column(db.VARCHAR(255))
    manager_phone = db.Column(db.INT)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# 评论表
class comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.INT, primary_key=True)
    comment_author = db.Column(db.VARCHAR(255))
    comment_content = db.Column(db.TEXT())
    comment_time = db.Column(db.VARCHAR(255))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# 帖子表
class post(db.Model):
    __tablename__ = 'post'
    user_id = db.Column(db.INT, db.ForeignKey('user.user_id'))  # 与用户表关联
    post_id = db.Column(db.INT, primary_key=True)  # 帖子 id
    post_title = db.Column(db.VARCHAR(255))  # 标题
    post_content = db.Column(db.MEDIUMTEXT())  # 内容
    post_time = db.Column(db.VARCHAR(255))  # 时间
    post_author = db.Column(db.VARCHAR(255))  # 作者
    post_type = db.Column(db.VARCHAR(255))  # 帖子类型
    post_like = db.Column(db.INT)  # 点赞量
    post_comment = db.Column(db.INT)  # 评论量
    post_img = db.Column(db.VARCHAR(255))  # 图片

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

# 我的喜欢表
class mylikes(db.Model):
    __tablename__ = 'mylike'

    mylike_id = db.Column(db.INT, primary_key=True)  # 点赞 id
    user_id = db.Column(db.String(8),db.ForeignKey('user.user_name'))  # 与用户表关联
    post_id = db.Column(db.INT, db.ForeignKey('post.post_id'))  # 与帖子表关联
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    
# 我的收藏表
class mycollection(db.Model):
    __tablename__ ='mycollection'
    mycollection_id = db.Column(db.INT, primary_key=True)  # 收藏 id
    user_id = db.Column(db.String(8),db.ForeignKey('user.user_id'))  # 与用户表关联
    post_id = db.Column(db.INT, db.ForeignKey('post.post_id'))  # 与帖子表关联

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}