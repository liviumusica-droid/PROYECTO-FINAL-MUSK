from src.sale import Sale


class SalesCollection:
    def __init__(self, sales_list: list[Sale]):
        self.sales = sales_list

    def sales_by_client(self, client_id: int) -> list[Sale]:
        return [sale for sale in self.sales if str(sale.client_id) == str(client_id)]

    def total_amount_by_client(self, client_id) -> float:
        return sum(sale.amount for sale in self.sales_by_client(client_id))

    def total_amount_by_category(self, category: str) -> float:
        return sum(sale.amount for sale in self.sales if sale.category.lower() == category.lower())
    

    def average_sale_by_client(self, client_id: int) -> float:
        client_sales = self.sales_by_client(client_id)
        if not client_sales:
            return 0.0
        return round(self.total_amount_by_client(client_id) / len(client_sales), 2)
        