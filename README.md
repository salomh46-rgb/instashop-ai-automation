# 🛒 InstaShop AI — Instagram & Telegram E-Commerce Sales Autopilot

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![UzPayment SDK](https://img.shields.io/badge/UzPayment-Click%20%7C%20Payme%20%7C%20Uzum-00F0FF?style=for-the-badge&logo=npm&logoColor=white)](https://www.npmjs.com/package/@javohirbek3302/uzpayment-sdk)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)
[![License MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-100%25_Passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](tests/)

<p align="center">
  <b>Conversational AI Sales Agent automating Instagram Direct & Telegram store customer support, real-time inventory checks, and instant Click/Payme checkout links.</b>
</p>

</div>

---

## 🌟 Key Capabilities & Features

- 🛍️ **24/7 Conversational AI Sales Agent:** Automatically handles product price inquiries, size/color variations, and stock queries in Uzbek and Russian.
- 💳 **Integrated UzPayment Checkout:** Instantly issues signed Click, Payme, and Uzum Bank payment links directly inside chat messages.
- 📦 **Live CRM & Orders Sync:** Real-time dashboard updating revenue metrics, payment receipts, and delivery queues.
- 🔒 **SQLite / Postgres Inventory Engine:** Thread-safe stock decrement preventing over-selling.
- 🐳 **Docker Containerized:** Pre-configured Dockerfile and FastAPI test suite.

---

## 🚀 Quickstart

### 1. Run via Python / FastAPI:
```bash
cd server
pip install -r requirements.txt
uvicorn server.main:app --reload --port 8000
```

### 2. Run via Docker Compose:
```bash
docker build -t instashop-ai .
docker run -p 8000:8000 instashop-ai
```

### 3. Open Interactive Direct Simulator:
Open `client/index.html` directly or deploy to Vercel/Netlify!

---

## 🧪 Automated Testing

Run the test suite:
```bash
python -m unittest discover tests/
```

---

## 👨‍💻 Author

**Javohirbek Asqarov (Jasper)**
- GitHub: [@salomh46-rgb](https://github.com/salomh46-rgb)
- Portfolio: [javohirbek-portfolio.vercel.app](https://javohirbek-portfolio.vercel.app/)
- Telegram: [@Dr_eviluz](https://t.me/Dr_eviluz)
- Email: [salomh46@gmail.com](mailto:salomh46@gmail.com)

---

## 📄 License
MIT © [Javohirbek Asqarov](LICENSE)
