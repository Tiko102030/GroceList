from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = lambda cursor, row: row[0]
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT item FROM list').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    data = request.get_json()
    item = data.get('item', '').strip()

    if item:
        conn = get_db_connection()
        conn.execute('INSERT INTO list (item) VALUES (?)', (item,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'item': item})

    return jsonify({'success': False}), 400

@app.route('/remove_all', methods=['POST'])
def delete_all():
    conn = get_db_connection()
    conn.execute('DELETE FROM list')
    conn.commit()
    conn.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
