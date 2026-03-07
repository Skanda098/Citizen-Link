from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)



# Ensure upload directory exists
os.makedirs('static/uploads', exist_ok=True)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS issues
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT,
                  category TEXT,
                  latitude REAL,
                  longitude REAL,
                  image_path TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/issues')
def get_issues():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, category, latitude, longitude, image_path, status FROM issues ORDER BY id DESC")
    issues = [{'id': row[0], 'category': row[1], 'lat': row[2], 'lon': row[3], 'image': row[4], 'status': row[5]} for row in c.fetchall()]
    conn.close()
    return jsonify(issues)

# Handle the "Resolve" button click
@app.route('/api/resolve/<int:issue_id>', methods=['POST'])
def resolve_issue(issue_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("SELECT user_id FROM issues WHERE id = ?", (issue_id,))
    result = c.fetchone()
    
    if result:
        user_id = result[0]
        c.execute("UPDATE issues SET status = 'Resolved' WHERE id = ?", (issue_id,))
        conn.commit()
        
        if user_id:
            message = f"🎉 Good news! Your reported issue (ID: #{issue_id}) has been marked as RESOLVED by the authorities. Thank you for keeping the city safe!"
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(telegram_url, json={'chat_id': user_id, 'text': message})
            
        conn.close()
        return jsonify({'success': True})
    
    conn.close()
    return jsonify({'success': False, 'error': 'Issue not found'}), 404

# NEW ROUTE: Handle the "Delete" button click (HARD DELETE)
@app.route('/api/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # 1. Get the image path first so we can delete the file
    c.execute("SELECT image_path FROM issues WHERE id = ?", (issue_id,))
    result = c.fetchone()
    
    if result:
        image_path = result[0]
        
        # 2. Delete the record from the database
        c.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        conn.commit()
        
        # 3. Delete the physical image file from the server
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Failed to delete image file: {e}")
                
        conn.close()
        return jsonify({'success': True})
        
    conn.close()
    return jsonify({'success': False, 'error': 'Issue not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)