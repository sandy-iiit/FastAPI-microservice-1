from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

redis = get_redis_connection(
    host="redis-11281.c212.ap-south-1-1.ec2.redns.redis-cloud.com",  # Host only, no port
    port=11281,  # Only the port number, as an integer
    password="oqPty3GvKTefiYMJQyHXOtNW784qt5kB",
    decode_responses=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for request validation
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post("/products")
def add(product: ProductCreate):
    # Create an instance of Product with data from the request body
    product_instance = Product(name=product.name, price=product.price, quantity=product.quantity)
    product_instance.save()  # Save to Redis
    return product_instance

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)