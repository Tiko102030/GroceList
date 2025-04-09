from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    return conn  # remove row_factory


@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT id, item FROM list').fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    data = request.get_json()
    item = data.get('item', '').strip()

    if item:
        conn = get_db_connection()
        cursor = conn.execute('INSERT INTO list (item) VALUES (?)', (item,))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'item': item, 'id': item_id})

    return jsonify({'success': False}), 400


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM list WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/clear', methods=['POST'])
def clear_items():
    conn = get_db_connection()
    conn.execute('DELETE FROM list')
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/items')
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT id, item FROM list').fetchall()
    conn.close()
    return jsonify(items)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

