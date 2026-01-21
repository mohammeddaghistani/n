import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = 'data/system.db'
if not os.path.exists('data'): os.makedirs('data')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, name TEXT, role TEXT)''')
    # جدول الإعدادات
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    # جدول الصفقات (يدعم الإحداثيات)
    c.execute('''CREATE TABLE IF NOT EXISTS deals (id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
                 neighborhood TEXT, area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
                 activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # حساب مدير افتراضي
    c.execute("INSERT OR IGNORE INTO users (username, password, name, role) VALUES (?, ?, ?, ?)", 
              ('admin', 'admin123', 'مدير النظام', 'admin'))
    conn.commit()
    conn.close()
    ensure_settings()

def ensure_settings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    defaults = [('mult_temp', '0.85'), ('mult_long', '1.60'), ('const_cost', '3500'), ('system_region', 'مكة المكرمة')]
    for key, value in defaults:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def add_deal(deal_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = '''INSERT INTO deals (property_type, location, neighborhood, area, price, deal_date, latitude, longitude, activity_type, notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(query, (deal_data['property_type'], deal_data['location'], deal_data.get('neighborhood'), deal_data['area'], 
                      deal_data['price'], deal_data['deal_date'], deal_data.get('latitude'), 
                      deal_data.get('longitude'), deal_data['activity_type'], deal_data.get('notes')))
    last_id = c.lastrowid
    conn.commit()
    conn.close()
    return last_id

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key=?', (key,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else default

def update_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()
