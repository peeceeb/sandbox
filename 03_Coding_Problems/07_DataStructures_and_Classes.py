from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Dict, Optional, Tuple
from collections import defaultdict, deque
import math

class OrderStatus(Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

@dataclass
class OrderItem:
    product_id: str
    price: float
    quantity: int

@dataclass
class Order:
    order_id: int
    customer_id: int
    status: OrderStatus
    timestamp: int  # Unix timestamp in seconds
    items: List[OrderItem]

    @property
    def total_value(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

@dataclass
class OrderResolution:
    order_id: int
    end_timestamp: int

@dataclass
class TimeWindow:
    start_timestamp: int
    end_timestamp: int
    active_count: int

#1. 
# Fix calculate_total_revenue() so that it only sums the total value of orders with status OrderStatus.DELIVERED.
def calculate_total_revenue(orders: List[Order]) -> float:
    return sum(
        order.total_value
        for order in orders
        if order.status == OrderStatus.DELIVERED
    )


#2. Return a list of orders for a given customer_id, sorted by timestamp in ascending order. If no orders exist, return an empty list.
def get_orders_by_customer(orders: List[Order], customer_id: int) -> List[Order]:
    customer_orders = [
        order for order in orders
        if order.customer_id == customer_id
    ]
    return sorted(customer_orders, key=lambda order: order.timestamp)



#3. Return the top n products generating the most revenue across DELIVERED orders.
# Primary Sort: Total revenue (Descending)
# Tie-breaker: product_id alphabetically (Ascending)
def get_top_products_by_revenue(orders: List[Order], n: int) -> List[Tuple[str, float]]:
    revenue_by_product: Dict[str, float] = defaultdict(float)

    for order in orders:
        if order.status != OrderStatus.DELIVERED:
            continue

        for item in order.items:
            revenue_by_product[item.product_id] += item.price * item.quantity

    return sorted(
        revenue_by_product.items(),
        key=lambda pair: (-pair[1], pair[0])
    )[:n]
