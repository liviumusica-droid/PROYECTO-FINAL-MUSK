import json
import pandas as pd
from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from src.functional_utils import filter_sales_by_category

def generate_report():
    with open("data/clients.json", "r", encoding="utf-8") as f:
        clients_data = json.load(f)

    df_sales = pd.read_csv("data/sales.csv")
    df_clients = pd.DataFrame(clients_data)

    clients_list =[Client(client["client_id"], client["name"], client["country"], client["signup_date"]) for client in clients_data]
    client_col = ClientCollection(clients_list)

    sales_list = []
    for _, row in df_sales.iterrows():
        sales_list.append(Sale(row["sale_id"], row["client_id"], row["product"], row["category"], row["amount"], row["date"]))
    sales_col = SalesCollection(sales_list)

    df_merged = pd.merge(df_sales, df_clients, on="client_id", how="inner")

    total_clients = len(client_col.clients)
    total_sales = len(df_sales)
    total_revenue = float(df_sales["amount"].sum())

    clients_report = []
    for client in client_col.clients:
        c_id = client.client_id

        total_spent = sales_col.total_amount_by_client(c_id)
        sale_count = len(sales_col.sales_by_client(c_id))
        average_sale = sales_col.average_sale_by_client(c_id)

        clients_report.append({
            "client_id": c_id,
            "name": client.name,
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale
        })
    
    countries =set(c.country for c in client_col.clients)
    top_clients_by_country = {}
    for country in countries:
        clients_in_country = client_col.clients_by_country(country)
        best_client = max(clients_in_country, key=lambda c: sales_col.total_amount_by_client(c.client_id), default=None)
        if best_client:
            top_clients_by_country[country] = {
                "client_id": best_client.client_id,
                "name": best_client.name,
                "total_spent": sales_col.total_amount_by_client(best_client.client_id)
            }

    sales_by_category =df_sales.groupby("category")["amount"].sum().to_dict()

    #cliente con gasto minimo > 500
    gasto_minimo = 500
    high_spending_clients = []
    for client in client_col.clients:
        total_spent = sales_col.total_amount_by_client(client.client_id)
        if total_spent > gasto_minimo:
            high_spending_clients.append({
                "client_id": client.client_id,
                "name": client.name,
                "total_spent": total_spent
            })
    #Ventas acumuladas mes a mes
    df_sales_copy = df_sales.copy()
    df_sales_copy["date"] = pd.to_datetime(df_sales_copy["date"])
    df_sales_copy["month"] = df_sales_copy["date"].dt.to_period("M")
    monthly_sales = {str(k): float(v) for k, v in df_sales_copy.groupby("month")["amount"].sum().to_dict().items()}

    #informe de json

    report = {
        "summary": {
            "total_clients": total_clients, 
            "total_sales": total_sales,
            "total_revenue": total_revenue
        },
        "clients": clients_report,
        "top_clients_by_country": top_clients_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }

    return report

def main():
    report = generate_report()

    # Guardar el informe en un archivo JSON
    with open("data/report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print("Informe generado y guardado en 'data/report.json'.")

if __name__ == "__main__":
    main()
