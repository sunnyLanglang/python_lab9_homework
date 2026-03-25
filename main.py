from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 数据库模型：电脑配件支出
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_part = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Expense({self.hardware_part}, {self.price} rub.)'

# 主页：显示所有支出和总金额
@app.route('/')
def index():
    expenses = Expense.query.all()
    total = db.session.query(db.func.sum(Expense.price)).scalar() or 0
    return render_template('index.html', expenses=expenses, total=total)

# 添加新支出（POST 请求，JSON 格式）
@app.route('/add', methods=['POST'])
def add_expense():
    data = request.json
    if not data or 'hardware_part' not in data or 'price' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    try:
        price = int(data['price'])
    except ValueError:
        return jsonify({'error': 'Price must be integer'}), 400

    expense = Expense(hardware_part=data['hardware_part'], price=price)
    db.session.add(expense)
    db.session.commit()
    return jsonify({'status': 'ok'})

# 清除所有记录（附加任务）
@app.route('/clear', methods=['POST'])
def clear_expenses():
    db.session.query(Expense).delete()
    db.session.commit()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)