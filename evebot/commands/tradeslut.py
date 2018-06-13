import argparse

from operator import itemgetter

from .. import config

from .. connectors import evemongo

def get_item_id_mongo(name):
    eve_items = evemongo.EveMongo(config.MONGOITEMS)
    request = {'name': name.lower()}
    record = eve_items.collection.find_one(request)
    eve_items.close()
    if not record:
        raise LookupError('"%s" not found, check spelling' % name)
    return record['typeid']


def get_price(mongo, item_id, quantity, sell=True):
    """ we are buying the item, looking at sell orders"""
    request = {'type_id': item_id}
    results = mongo.collection.find(request)
    sorted_results = sorted(results, key=itemgetter('price'), reverse=sell)
    total_price = 0
    quantity_remain = int(quantity)
    for order in sorted_results:
        remain = order['volume_remain']
        price = order['price']
        if remain > quantity_remain:
            return (total_price + (price * quantity_remain), quantity)
        else:
            quantity_remain = quantity_remain - remain
            total_price += remain * price
    return(total_price, int(quantity) - quantity_remain)


def parse_inventory(inventory):
    inventory_dict = {'skipped': []}
    for line in inventory.splitlines():
        if not line:
            continue
        elif line.startswith('*'):
            inventory_dict['skipped'].append(line)
        else:
            item = line.split('    ')
            try:
                name = item[0]
            except IndexError:
                inventory_dict['skipped'].append(line)
                continue

            try:
                quantity = int(item[1].replace(',', ''))
            except IndexError:
                quantity = 1
            except ValueError:
                quantity = 1

            try:
                item_id = get_item_id_mongo(name)
            except LookupError:
                inventory_dict['skipped'].append(line)
                continue

            if not inventory_dict.get(item_id):
                inventory_dict[item_id] = 0

            inventory_dict[item_id] += quantity
    return inventory_dict


def parse_fitting(fitting):
    fitting_dict = {'skipped': []}
    for line in fitting.splitlines():
        if not line:
            continue

        if line.startswith('['):
            item = line.split(',')[0]
            item = item.replace('[', '')
            quantity = 1
        else:
            try:
                last = line.split(' ')[-1]
                if last.startswith('x'):
                    item = ' '.join(line.split(' ')[:-1])
                    quantity = last.replace('x', '')
                    quantity = int(quantity)
                else:
                    item = ' '.join(line.split(' '))
                    quantity = 1

            except IndexError:
                item = line
                quantity = 1
        try:
            item_id = get_item_id_mongo(item)
        except LookupError:
            fitting_dict['skipped'].append(item)
            continue

        if not fitting_dict.get(item_id):
            fitting_dict[item_id] = 0
        fitting_dict[item_id] += quantity

    return fitting_dict

def main(args):
    subcmd = vars(args).pop('subcmd')

    math_percent = 100/int(args.percent)
    if subcmd == 'item':
        item_name = args.name.lower()
        try:
            item_id = get_item_id_mongo(item_name)
        except LookupError as e:
            return str(e)
        # we look at buy orders to sell things
        sell_mongo = evemongo.EveMongo(config.MONGOMARKET_SELL)
        # and sell orders to buy things
        buy_mongo = evemongo.EveMongo(config.MONGOMARKET_BUY)
        sell_price, sell_quantity = get_price(buy_mongo, item_id, args.quantity, sell=True)
        buy_price, buy_quantity = get_price(sell_mongo, item_id, args.quantity, sell=False)

        message = 'Sell {} for {:,.2f}\n'.format(sell_quantity, sell_price * math_percent)
        message += 'Buy {} for {:,.2f}'.format(buy_quantity, buy_price * math_percent)

        buy_mongo.close()
        sell_mongo.close()

        return message

    elif subcmd == 'inventory':
        inventory_content = parse_inventory(args.contents)
        buy_mongo = evemongo.EveMongo(config.MONGOMARKET_BUY)
        value = 0
        for item_id, quantity in inventory_content.items():
            if item_id == 'skipped':
                continue
            tmp_value, _ = get_price(buy_mongo, item_id, quantity, sell=True)
            value += tmp_value

        message = 'Sell for {:,.2f} - Tax'.format(value * math_percent)

        if inventory_content.get('skipped'):
            message = message + '\n\n Some items were skipped:' \
                                '\n%s' % '\n'.join(inventory_content.get('skipped'))

        return message

    elif subcmd == 'fitting':
        fitting_content = parse_fitting(args.contents)
        sell_mongo = evemongo.EveMongo(config.MONGOMARKET_SELL)
        value = 0
        for item_id, quantity in fitting_content.items():
            if item_id == 'skipped':
                continue
            tmp_value, _ = get_price(sell_mongo, item_id, quantity, sell=False)
            value += tmp_value

        message = 'Buy for {:,.2f} + Tax'.format(value * math_percent)

        if fitting_content.get('skipped'):
            message = message + '\n\n Some items were skipped:' \
                                '\n%s' % '\n'.join(fitting_content.get('skipped'))

        return message

    else:
        return 'requested command is not valid, use item, inventory, or fitting.'


def do_args(inargs=None):
    parser = argparse.ArgumentParser('get jita prices for items, invintories, and fittings')
    parser.add_argument('-p', '--percent',
                        help='percent of the cost you wish to display, default=100',
                        default=100)
    subparser = parser.add_subparsers(dest='subcmd')
    subparser.required = True
    item = subparser.add_parser('item',
                                help='get the current price for one item')
    item.add_argument('name',
                      help='name of an item to find the price for, wrapped in quotes')
    item.add_argument('quantity',
                      help='number of the item you are interested in')
    inventory = subparser.add_parser('inventory',
                                     help='get sell value for an invintory of items')
    inventory.add_argument('contents',
                           help='inventory of items to sell, as copied from eve.  wraped in quotes')
    fitting = subparser.add_parser('fitting',
                                   help='get the buy cost of a fitting in eve')
    fitting.add_argument('contents',
                         help='a fitting to get the buy cost of wrapped in quotes')
    if inargs:
        args = parser.parse_args(inargs)
    else:
        args = parser.parse_args()
    return args



if __name__ == '__main__':
    ARGS = do_args()
    print(main(ARGS))