from mongoengine import Document, StringField, IntField


class Order(Document):
    _id = IntField()
    product_image = StringField()
    product_title = StringField()
    product_id = StringField()
    product_variant_id = StringField()
    order_no = IntField()
    ordered_at = StringField()
    finalized_order_at = StringField()
    due_date = StringField()
    default_price = IntField()
    discount = IntField()
    final_price = IntField()
