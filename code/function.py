from models import *
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy



# 获取用户的点赞信息
def get_user_likes(user_id):
    try:
        likes = mylikes.query.filter_by(user_id=user_id).all()
        user_likes = []
        for like in likes:
            user_likes.append(like.to_dict())
        return user_likes
    except Exception as e:
        return jsonify({'error':str(e)})
    
# 获取排行榜
def getchart():
    # 从数据库中查询帖子信息
    try:
        db_data = post.query.order_by(post.post_like.desc()).all()
        if db_data is None:
            return jsonify('post not found')
        else:
            keys = ['post_title', 'post_id', 'post_like', 'post_author']
            return_data = [dict(zip(keys,(item.to_dict()[key] for key in keys))) 
                           for item in db_data]
            return (jsonify(return_data))
    except Exception as e:
        return jsonify({'error':str(e)})


# 搜索帖子
def search_post(rec_title):
    try:
        # 从数据库中查询帖子信息
        db_data = post.query.filter_by(post_title=rec_title).all()
        if db_data is None:
            return jsonify('post not found')
        else:
            # 存储结果的列表
            return_data = []
            for item in db_data:
                # 将 item 转换为字典
                item_dict = item.to_dict()
                # 提取所需信息添加到 return_data 列表中
                return_data.append({
                    'post_title': item_dict['post_title'],
                    'post_id': item_dict['post_id'],
                    'post_content': item_dict['post_content'],
                    'post_time': item_dict['post_time'],
                    'post_author': item_dict['post_author'],
                    'post_type': item_dict['post_type'],
                    'post_like': item_dict['post_like'],
                    'post_comment': item_dict['post_comment'],
                    'post_img': item_dict['post_img']
                })
            return jsonify(return_data)
    except Exception as e:
        return jsonify({'error':str(e)})
