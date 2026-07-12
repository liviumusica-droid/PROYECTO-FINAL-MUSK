class Sale:
    def __init__(self, sale_id, client_id, product: str, category: str, amount, date):
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = str(product)
        self.category = str(category)
        self.amount = float(amount) 
        self.date = date

    def to_dict(self) -> dict:
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": str(self.date)
        }
        