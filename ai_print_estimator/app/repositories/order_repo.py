from sqlalchemy.orm import Session
from app.models.order import Order
from app.domain.enums import OrderStatus


class OrderRepository:
    @staticmethod
    def create(db: Session, raw_input: str, input_type: str) -> Order:
        order = Order(
            raw_input=raw_input,
            input_type=input_type,
            status=OrderStatus.RECEIVED.value
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_specs(db: Session, order: Order, specs: dict) -> Order:
        order.parsed_specs = specs
        order.status = OrderStatus.ESTIMATED.value
        db.commit()
        db.refresh(order)
        return order