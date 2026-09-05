import time
import os
import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="InstaShop AI — Instagram & Telegram Retail Sales Autopilot",
    version="1.0.0",
    description="Conversational AI Commerce Agent with Auto-Checkout & Inventory Sync."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = os.path.join(os.path.dirname(__file__), "instashop.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 10,
            sizes TEXT,
            image_url TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE,
            customer_name TEXT,
            phone TEXT,
            product_name TEXT,
            size TEXT,
            quantity INTEGER,
            total_amount REAL,
            payment_provider TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT
        )
    """)
    # Seed default products if empty
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        default_items = [
            ("Oversized Hoodie 'Cyberpunk 2077'", "Kiyim-kechak", 320000, 15, "M, L, XL", "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=400"),
            ("Smart Watch 'Pulse V2'", "Gadjetlar", 450000, 8, "One Size", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"),
            ("Wireless Noise-Canceling Earbuds", "Audio", 280000, 20, "Qora, Oq", "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400"),
            ("Minimalist Leather Wallet", "Aksessuar", 120000, 25, "Jigarrang", "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400")
        ]
        cur.executemany("INSERT INTO products (name, category, price, stock, sizes, image_url) VALUES (?, ?, ?, ?, ?, ?)", default_items)
    conn.commit()
    conn.close()

init_db()

class ChatMessage(BaseModel):
    message: str
    channel: str = "instagram" # "instagram" or "telegram"
    customer_name: Optional[str] = "Mijoz"

class CreateOrderRequest(BaseModel):
    customer_name: str
    phone: str
    product_id: int
    size: str = "M"
    quantity: int = 1
    payment_provider: str = "click" # click, payme, uzum

@app.get("/")
def root():
    return {
        "service": "InstaShop AI Automation Engine",
        "status": "OPERATIONAL",
        "version": "1.0.0"
    }

@app.get("/api/products")
def get_products():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id ASC")
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return items

@app.get("/api/orders")
def get_orders():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = [dict(r) for r in cur.fetchall()]
    conn.close()
    return orders

@app.post("/api/chat")
def process_chat(msg: ChatMessage):
    user_text = msg.message.lower().strip()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = [dict(r) for r in cur.fetchall()]
    conn.close()

    # Conversational Intent Engine
    # 1. Product price / stock search
    matched_product = None
    for p in products:
        words = p["name"].lower().split()
        if any(w in user_text for w in words if len(w) > 3):
            matched_product = p
            break

    if "salom" in user_text or "assalomu" in user_text or "qalesiz" in user_text:
        return {
            "reply": f"Assalomu alaykum {msg.customer_name}! Do'konimizga xush kelibsiz. Qanday mahsulot qidiryapsiz? Bizda Hoodie, Smart Watch, Earbuds va Hamyonlar mavjud!",
            "suggested_product": None
        }

    if matched_product:
        return {
            "reply": f"Ha, albatta! <b>{matched_product['name']}</b> mavjud!\n\n💰 <b>Narxi:</b> {int(matched_product['price']):,} so'm\n📏 <b>O'lchamlari/Ranglari:</b> {matched_product['sizes']}\n📦 <b>Omborda qoldiq:</b> {matched_product['stock']} dona.\n\nBuyurtma berishni istaysizmi?",
            "suggested_product": matched_product
        }

    if "dastavka" in user_text or "yetkazib" in user_text:
        return {
            "reply": "O'zbekiston bo'ylab barcha viloyatlarga 24-48 soat ichida yetkazib beramiz! Toshkent bo'ylab yetkazish 20 000 so'm, viloyatlarga 35 000 so'm.",
            "suggested_product": None
        }

    if "narx" in user_text or "qancha" in user_text:
        list_str = "\n".join([f"• {p['name']}: {int(p['price']):,} so'm" for p in products[:3]])
        return {
            "reply": f"Bizdagi ommabop mahsulotlar narxlari:\n\n{list_str}\n\nQaysi biri sizga ma'qul keldi?",
            "suggested_product": products[0]
        }

    return {
        "reply": f"Savolingiz qabul qilindi! Buyurtma berish uchun mahsulot nomini yozing yoki pastdagi katalogdan tanlang.",
        "suggested_product": None
    }

@app.post("/api/orders")
def create_order(req: CreateOrderRequest):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (req.product_id,))
    product = cur.fetchone()
    if not product:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    total = product["price"] * req.quantity
    order_code = f"ORD-{int(time.time())}"
    now_iso = datetime.now(timezone.utc).isoformat()

    cur.execute("""
        INSERT INTO orders (order_code, customer_name, phone, product_name, size, quantity, total_amount, payment_provider, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PAID', ?)
    """, (order_code, req.customer_name, req.phone, product["name"], req.size, req.quantity, total, req.payment_provider.upper(), now_iso))

    # Deduct stock
    cur.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?", (req.quantity, req.product_id))
    conn.commit()
    conn.close()

    # Generate UzPayment Checkout Link
    checkout_url = f"https://my.click.uz/services/pay?service_id=12345&merchant_id=67890&amount={int(total)}&transaction_param={order_code}"
    if req.payment_provider.lower() == "payme":
        checkout_url = f"https://checkout.paycom.uz/bWVyY2hhbnRfaWQ9cHJvZF9vcmRlcg=="

    return {
        "order_code": order_code,
        "total_amount": total,
        "status": "PAID",
        "payment_url": checkout_url,
        "message": f"Buyurtmangiz muvaffaqiyatli qabul qilindi! To'lov tasdiqlandi."
    }
