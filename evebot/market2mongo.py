#!/usr/bin/python3

def main(args):
    #alright, every time i do something new i start with alright...
    # https://esi.tech.ccp.is/latest/markets/10000002/orders/?datasource=tranquility&order_type=sell&page=1
    #the region idea for jita is 10000002
    #60003760   Jita IV - Moon 4 - Caldari Navy Assembly Plant
    #i have to grab the data by region, which is a pain, but its free
    #then i can filter it down to the station and dump it into mongo
    #i want to have it dump to a temorary collection, then replace the exising
    #collection once the data has all been collected and dumped... idk how to do
    #that, but i hope its easy and internal to mongo
    #there are lots of pages of data, so there will need to be tons of functions
    #to sort and get whatever i want, probably need a class for that at some point
    pass


if __name__ == '__main__':
    main(None)