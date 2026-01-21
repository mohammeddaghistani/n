import sqlite3
import os
from datetime import datetime

# التأكد من المجلد
if not os.path.exists('data'): os.makedirs('data')
DB_PATH = 'data/system.db'

def init_db():
    """إنشاء الجداول بناءً على متطلبات اللائحة والتقييم"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # جدول المستخدمين وصلاحياتهم (Admin, Valuer, Committee)
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT UNIQUE, password TEXT, name TEXT, role TEXT)''')
    # جدول الصفقات المقارنة (Market Comparables) حسب دليل التقييم
    c.execute('''CREATE TABLE IF NOT EXISTS deals (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 property_type TEXT, location TEXT, neighborhood TEXT, area REAL, 
                 price REAL, deal_date DATE, latitude REAL, longitude REAL, 
                 activity_type TEXT, notes TEXT)''')
    # جدول إعدادات النظام (معاملات الخصم والتكلفة)
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # حساب المدير الافتراضي
    c.execute("INSERT OR IGNORE INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
              ('admin', 'admin123', 'مدير النظام', 'admin'))
    conn.commit()
    conn.close()

def ensure_settings():
    """تثبيت القيم الافتراضية من دليل التقييم"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    defaults = [('mult_temp', '0.85'), ('const_cost', '3500'), ('discount_rate', '0.10')]
    for key, value in defaults:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def add_deal(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO deals (property_type, location, neighborhood, area, price, 
                 deal_date, latitude, longitude, activity_type, notes) VALUES (?,?,?,?,?,?,?,?,?,?)''',
              (data['property_type'], data['location'], data.get('neighborhood'), data['area'], 
               data['price'], data['deal_date'], data.get('latitude'), data.get('longitude'), 
               data['activity_type'], data.get('notes')))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key=?', (key,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else default
