from productionentry.models import Product


def initialise_db():
    Product.Product.create_table()
