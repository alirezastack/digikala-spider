from digispider.store.mongo_connection import MongoConnection
from digispider.store.order_store import OrdersStore
from digispider import config, logger
from digispider.utils import login
from unidecode import unidecode
from bs4 import BeautifulSoup
import telegram
import argparse

_AVAILABLE_OPERATIONS = ['orders', 'invoices']


def fetch_resource(operation):
    assert operation in _AVAILABLE_OPERATIONS, f"{operation} is not known!"

    MongoConnection(config['mongo'])
    logger.info('connected to MongoDB!')
    bot = telegram.Bot(token=config['bot_credentials']['telegram']['token'])

    logger.debug(f'trying to get {operation} information...')
    session, response = login(operation)
    soup = BeautifulSoup(response.text, 'html.parser')


    result = soup.findAll('tr', {'class': 'c-ui-table__row c-ui-table__row--body c-ui-table__row--with-hover'})
    order_detail_url = config['base_url'] + '/ajax/order/details/search/'
    order_store = OrdersStore()
    inserted = False
    for order in result:
        image = order.img['src']
        title = order.find('td', {'class': 'c-ui-table__cell c-ui-table__cell--item-title'}).get_text()
        tds = order.findAll('td')
        dkp = tds[4:5][0].get_text()
        dkpc = tds[5:6][0].get_text()
        order_no = tds[8:9][0].get_text()
        order_detail_response = session.post(url=order_detail_url,
                                             data={'search[product_variant_id]': dkpc}
                                             )
        soup = BeautifulSoup(order_detail_response.text, 'html.parser')
        od_rows = soup.findAll('tr', {'class': 'c-ui-table__row c-ui-table__row--with-hover'})
        for od_row in od_rows:
            od_tds = od_row.findAll('td')
            order_id = od_tds[2].get_text()

            order_doc = order_store.get(order_id)
            if order_doc:
                continue

            ordered_at = od_tds[3].get_text()
            finalized_order_at = od_tds[4].get_text()
            due_date = od_tds[6].get_text()
            price = od_tds[7].get_text()
            discount = od_tds[8].get_text()
            final_price = od_tds[10].get_text()

            order_no = int(unidecode(order_no))
            ordered_at = unidecode(ordered_at)
            finalized_order_at = unidecode(finalized_order_at)
            due_date = unidecode(due_date)
            price = unidecode(price)
            discount = unidecode(discount)
            final_price = unidecode(final_price)
            order_doc_id = order_store.save(dict(
                order_id=int(order_id),
                product_image=image,
                product_title=title,
                product_id=dkp,
                product_variant_id=dkpc,
                order_no=order_no,
                ordered_at=ordered_at,
                finalized_order_at=finalized_order_at,
                due_date=due_date,
                default_price=int(price.replace(',', '')),
                discount=int(discount.replace(',', '')),
                final_price=int(final_price.replace(',', '')),
            ))
            inserted = True
            logger.info(f'order document has been saved: {order_doc_id}')
            caption = f'''
            {title}
            --------------------------
            OrderId: {order_id}
            Order No.: {order_no}
            --------------------------
            Ordered At: {ordered_at}
            Due Date: {due_date}
            --------------------------
            Price: {price}
            Discount: {discount}
            Final Price: {final_price}
            '''
            output = bot.send_photo(chat_id=config['bot_credentials']['telegram']['chat_id'],
                                    photo=image.replace('h_115,w_115', 'h_415,w_415'),
                                    caption=caption)
            logger.info(f'bot output: {output}')

    if not inserted:
        logger.info('No new order :(')

    return result


def main():  # pylint: disable=W0102
    """
    main function is the entry-point of the call api method
    :return: remote rest api response
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation',
                        required=True,
                        help='target resource to fetch e.g.: orders')
    args = parser.parse_args()

    operation = args.operation.lower()

    fetch_resource(operation)
