from productionentry.classes.Site import Site
from productionentry.classes.Product import Product
from productionentry.classes.SiteProduct import SiteProduct


def main():
    Site.create_table()
    Product.create_table()
    SiteProduct.create_table()
    new_site = Site(name="Karuah East Quarry", is_simple=False, obj_id=None)
    new_site.save_self()


if __name__ == '__main__':
    main()
