from mongoengine import DoesNotExist

from digispider import logger
from digispider.models.order import Order
import json


class OrdersStore:
    def __init__(self):
        pass

    def save(self, data):
        logger.info(f'new order has arrived: \n{data}')
        order = Order(
            _id=data['order_id'],
            product_image=data['product_image'],
            product_title=data['product_title'],
            product_id=data['product_id'],
            product_variant_id=data['product_variant_id'],
            order_no=data['order_no'],
            ordered_at=data['ordered_at'],
            finalized_order_at=data['finalized_order_at'],
            due_date=data['due_date'],
            default_price=data['default_price'],
            discount=data['discount'],
            final_price=data['final_price'],
        )
        logger.debug('saving order: {}'.format(order._id))
        insert_result = order.save()
        return str(insert_result.pk)

    def get(self, _id):
        try:
            order_doc = Order.objects(_id=_id).get()
            order_doc = json.loads(order_doc.to_json())
            return order_doc
        except DoesNotExist:
            return None
