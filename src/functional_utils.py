def filter_sales_by_category(sales: list, category: str) ->list:
    return list(filter(lambda sale: sale.category.lower() == category.lower(), sales))