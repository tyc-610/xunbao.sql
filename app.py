from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
# 或者
# from flask_pymongo import PyMongo

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
# 或者
# app.config["MONGO_URI"] = "mongodb://localhost:27017/yourdatabase"

# 初始化数据库
db = SQLAlchemy(app)
# 或者
# mongo = PyMongo(app)

# 定义模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    scores = db.relationship('Score', backref='player', lazy=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# 创建数据库表
@app.before_first_request
def create_tables():
    db.create_all()

# 路由和视图函数
@app.route('/')
def index():
    return render_template('index.html')

# 其他路由和视图函数...

if __name__ == '__main__':
    app.run(debug=True)

# 获取玩家信息
@app.route('/player-info')
def player_info():
    player = Player.query.first()  # 假设只有一个玩家，或者你需要根据实际情况查询
    return jsonify({
        'id': player.id,
        'nickname': player.nickname,
        'scores': [score.score for score in player.scores]
    })

# 获取游戏历史
@app.route('/game-history')
def game_history():
    history = Score.query.all()
    return jsonify([{'score': score.score} for score in history])

# 在Flask后端保存玩家信息
@app.route('/set-nickname', methods=['POST'])
def set_nickname():
    nickname = request.form['nickname']
    player = Player(nickname=nickname)
    db.session.add(player)
    db.session.commit()
    return jsonify({'id': player.id, 'nickname': player.nickname}), 201

# 在Flask后端保存得分
@app.route('/add-score', methods=['POST'])
def add_score():
    score = request.form['score']
    player_id = request.form['player_id']
    player = Player.query.get(player_id)
    score_instance = Score(player_id=player_id, score=score)
    db.session.add(score_instance)
    db.session.commit()
    return jsonify({'score': score}), 201
# Flask 后端增加得分
@app.route('/add-score', methods=['POST'])
def add_score():
    data = request.get_json()
    player_id = data['player_id']
    score = data['score']
    
    player = Player.query.get(player_id)
    if player:
        new_score = Score(player_id=player_id, score=score)
        db.session.add(new_score)
        db.session.commit()
        return jsonify({'message': 'Score added successfully'})
    else:
        return jsonify({'message': 'Player not found'}), 404