import unittest
from fastapi.testclient import TestClient
from server.main import app, init_db

client = TestClient(app)

class TestInstaShop(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_root(self):
        res = client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("InstaShop", res.json()["service"])

    def test_get_products(self):
        res = client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 4)

    def test_chat_nlp_intent(self):
        res = client.post("/api/chat", json={
            "message": "Hoodie narxi qancha?",
            "channel": "instagram",
            "customer_name": "Javohir"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Hoodie", data["reply"])
        self.assertIsNotNone(data["suggested_product"])

    def test_create_order_checkout(self):
        res = client.post("/api/orders", json={
            "customer_name": "Anvar Aliyev",
            "phone": "+998901234567",
            "product_id": 1,
            "size": "L",
            "quantity": 1,
            "payment_provider": "click"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "PAID")
        self.assertIn("click", data["payment_url"])

if __name__ == "__main__":
    unittest.main()
