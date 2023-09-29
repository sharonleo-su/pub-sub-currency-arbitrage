import time
import datetime
import socket
import fxp_bytes_subscriber
import bellman_ford

PROVIDER_ADDRESS = ('127.0.0.1', 50403)
SERVER_ADDRESS = ('127.0.0.1', 10000)
BUF_SZ = 4096
SUBSCRIPTION_TIMEOUT = 600


class Subscriber(object):

    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(SERVER_ADDRESS)
        self.tic = time.perf_counter()
        self.quotes = []
        self.currency_rates = {}
        self.currencies = []
        self.rates_graph = []
        print('START TIME: {}'.format(self.tic))
        self.toc = None

    def subscribe_to_forex_provider(self):
        """ Sends subscription message to Forex Provider."""
        subscribe_message = fxp_bytes_subscriber.serialize_address(SERVER_ADDRESS[0], SERVER_ADDRESS[1])
        self.listener.sendto(subscribe_message, PROVIDER_ADDRESS)
        self.listener.settimeout(60)
        print('\nSENDING MESSAGE TO FOREX PROVIDER: {}'.format(SERVER_ADDRESS))

    def out_of_order(self, quote):
        """ Checks whether given quote has been received out of order."""
        for previous_quote in self.quotes:
            if quote[1] == previous_quote[1] and quote[2] == previous_quote[2]:
                if quote[0] < previous_quote[0]:
                    return True

    def remove_stale_quotes(self):
        """ Removes all quotes older than 1.5 seconds."""
        if self.quotes:
            for i in range(len(self.quotes)):
                if self.quotes[i] != 'NA':
                    if (datetime.datetime.utcnow() - self.quotes[i][0]).total_seconds() >= 1.5:
                        print('REMOVING STALE QUOTE: {}'.format(self.quotes[i]))
                        self.quotes[i] = 'NA'

    def update_currencies(self):
        """ Update list of currencies. """
        for quote in self.quotes:
            if quote != 'NA':
                if quote[1] not in self.currencies:
                    self.currencies.append(quote[1])
                if quote[2] not in self.currencies:
                    self.currencies.append(quote[2])

    def update_currency_rates(self):
        """ Update currency exchange rates. """
        for quote in self.quotes:
            if quote != 'NA':
                self.currency_rates[quote[1] + '/' + quote[2]] = quote[3]
                self.currency_rates[quote[2] + '/' + quote[1]] = 1 / quote[3]
                self.currency_rates[quote[1] + '/' + quote[1]] = 1
                self.currency_rates[quote[2] + '/' + quote[2]] = 1

    def update_rates_graph(self):
        """ Update currency rates matrix. """
        self.rates_graph = []
        for currency1 in self.currencies:
            all_rates_for_currency = []
            for currency2 in self.currencies:
                if currency1 + '/' + currency2 not in self.currency_rates:
                    all_rates_for_currency.append(float('inf'))
                else:
                    all_rates_for_currency.append(self.currency_rates[currency1 + '/' + currency2])
            self.rates_graph.append(all_rates_for_currency)

    def report_arbitrage_opportunities(self):
        """ Run the Bellman-Ford algorithm and report arbitrage opportunities."""
        bellman_ford.arbitrage(self.currencies, self.rates_graph)

    def run(self):
        """ Driver method """
        self.subscribe_to_forex_provider()
        while True:
            data = None
            try:
                self.toc = time.perf_counter()
                if (self.toc - self.tic) > SUBSCRIPTION_TIMEOUT:
                    print('END TIME: {}'.format(self.toc))
                    self.timeout_handler()
                data = self.listener.recv(BUF_SZ)
            except TimeoutError:
                print('TIMEOUT! EXITING ...')
                self.listener.close()
                exit(0)
            if data is not None:
                provider_message = fxp_bytes_subscriber.unmarshal_message(data)
                self.remove_stale_quotes()
                for item in provider_message:
                    print(item)
                    if self.out_of_order(item):
                        print('IGNORING OUT-OF-ORDER QUOTE: {}'.format(item))
                        # self.remove_stale_quotes()
                    else:
                        self.quotes.append(item)
                    self.update_currencies()
                    self.update_currency_rates()
                    self.update_rates_graph()
                    self.report_arbitrage_opportunities()

    def timeout_handler(self):
        """ Exit and close if subscription time exceeds 10 minutes. """
        print('SUBSCRIPTION TIMEOUT! EXITING ...')
        self.listener.close()
        exit(0)


if __name__ == '__main__':
    subscriber = Subscriber()
    try:
        subscriber.run()
    except Exception as err:
        print(err)
