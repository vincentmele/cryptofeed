from multiprocessing import Process

from cryptofeed import FeedHandler
from cryptofeed.backends.rabbitmq import BookRabbit, TickerRabbit, TradeRabbit
from cryptofeed.exchanges import Kraken, Deribit, Huobi, OKEx, Bitfinex, HitBTC, DSX
from cryptofeed.defines import L2_BOOK, TRADES, TICKER


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())


def receiver(port):
    import pika
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=port))
    channel = connection.channel()
    channel.queue_declare(queue='cryptofeed')
#    channel.basic_consume(queue='cryptofeed',
#                          on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def main():
    try:
        p = Process(target=receiver, args=(5672,))

        p.start()

        f = FeedHandler()
        f.add_feed(Kraken(max_depth=50, channels=[L2_BOOK, TRADES, TICKER], pairs=['BTC-USD', 'ETH-USD'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(Deribit(max_depth=50, channels=[L2_BOOK, TRADES, TICKER], pairs=['BTC-PERPETUAL', 'ETH-PERPETUAL'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(Huobi(max_depth=50, channels=[L2_BOOK, TRADES], pairs=['BTC-USDT', 'ETH-USDT'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(OKEx(max_depth=50, channels=[L2_BOOK, TRADES], pairs=['BTC-USDT', 'ETH-USDT'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(Bitfinex(max_depth=50, channels=[L2_BOOK, TRADES], pairs=['BTC-USDT', 'ETH-USDT'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(HitBTC(max_depth=50, channels=[L2_BOOK, TRADES], pairs=['BTC-USD', 'ETH-USD'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))
        f.add_feed(DSX(max_depth=50, channels=[L2_BOOK, TRADES], pairs=['BTC-USDT', 'ETH-USDT'], callbacks={L2_BOOK: BookRabbit(), TRADES: TradeRabbit(), TICKER: TickerRabbit()}))


        f.run()

    finally:
        p.terminate()


if __name__ == '__main__':
    main()
