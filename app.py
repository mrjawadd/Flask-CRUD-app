from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    items = Item.query.all()  # READ
    return render_template('list.html', items=items)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Item(name=name)  # CREATE
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']  # UPDATE
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', item=item)


@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)  # DELETE
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
