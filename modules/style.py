import sqlite3
import os
import pandas as pd
from datetime import datetime

# التأكد من وجود مجلد البيانات
if not os.path.exists('data'):
    os.makedirs('data')

DB_PATH = 'data/system.db'

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE, password TEXT, name TEXT, role TEXT)''')
    
    # 2. جدول الإعدادات
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMP)''')

    # 3. جدول الصفقات
    c.execute('''CREATE TABLE IF NOT EXISTS deals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
                  area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
                  activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # إضافة مدير افتراضي إذا لم يوجد
    c.execute("INSERT OR IGNORE INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
              ('admin', 'admin123', 'مدير النظام', 'admin'))
              
    conn.commit()
    conn.close()
    ensure_settings()

def ensure_settings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    defaults = [
        ('mult_temp', '0.85'), ('mult_long', '1.60'), ('mult_direct', '1.25'),
        ('const_cost', '3500'), ('discount_rate', '0.10'), ('system_name', 'HMMC')
    ]
    for key, value in defaults:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else default

def update_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)', 
              (key, str(value), datetime.now()))
    conn.commit()
    conn.close()

def add_deal(deal_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type, notes) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (deal_data['property_type'], deal_data['location'], deal_data['area'], 
               deal_data['price'], deal_data['deal_date'], deal_data.get('latitude'), 
               deal_data.get('longitude'), deal_data['activity_type'], deal_data.get('notes', '')))
    deal_id = c.lastrowid
    conn.commit()
    conn.close()
    return deal_id
