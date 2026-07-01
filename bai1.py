from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    # Kiểm tra trùng mã sản phẩm
    for item in products:
        if item["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }

    # LỖI:
    # API tạo sản phẩm mới ngay mà không kiểm tra
    # xem mã sản phẩm (code) đã tồn tại trong danh sách products hay chưa.
    # Vì vậy có thể tạo nhiều sản phẩm có cùng code.

    # CÁCH SỬA:
    # Trước khi tạo sản phẩm mới, duyệt danh sách products.
    # Nếu tìm thấy sản phẩm có code trùng với product.code
    # thì raise HTTPException(status_code=400, detail="Product code already exists").
    # Nếu không trùng thì mới tạo và thêm sản phẩm vào danh sách.
    # Đồng thời trả về HTTP status code 201 Created.
