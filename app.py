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
    count = int(data.get('count', 1))
    description = data.get('description', '').strip()

    if item:
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO list (item, count, description) VALUES (?, ?, ?)',
            (item, count, description)
        )
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'item': item, 'id': item_id, 'count': count, 'description': description})

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
    sort = request.args.get('sort', 'added')

    conn = get_db_connection()

    if sort == 'az':
        items = conn.execute('SELECT id, item, count, description FROM list ORDER BY item COLLATE NOCASE ASC').fetchall()
    elif sort == 'za':
        items = conn.execute('SELECT id, item, count, description FROM list ORDER BY item COLLATE NOCASE DESC').fetchall()
    elif sort == 'amount':
        items = conn.execute('SELECT id, item, count, description FROM list ORDER BY count DESC').fetchall()
    else:
        items = conn.execute('SELECT id, item, count, description FROM list').fetchall()

    conn.close()
    return jsonify(items)

@app.route('/update-description/<int:item_id>', methods=['POST'])
def update_description(item_id):
    data = request.get_json()
    description = data.get('description', '').strip()

    conn = get_db_connection()
    conn.execute('UPDATE list SET description = ? WHERE id = ?', (description, item_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

