from app.schemas.product_scheme import ProductPublic


def product_create(product: ProductPublic) -> ProductPublic:
    print("Database에 입력을 처리합니다.")
    return product


def product_get_all() -> list[ProductPublic]:
    return [
        ProductPublic(id=100, name="pant01", price=20000),
        ProductPublic(id=101, name="pant02", price=30000),
        ProductPublic(id=102, name="pant03", price=40000),
    ]


def product_get(product_id: int) -> ProductPublic:
    return ProductPublic(id=product_id, name="크록스", price=30000)
