# Pub/Sub Currency Arbitrage
An implementation of a publish/subscribe system for determining currency arbitrage opportunities using the Bellman-Ford algorithm.

# Forex Arbitrage Detection

This project is a Python implementation for detecting arbitrage opportunities in the foreign exchange (forex) market. It utilizes a price feed from a publisher, constructs a graph of currency exchange rates, and employs the Bellman-Ford algorithm to detect negative-weight cycles, which indicate potential arbitrage opportunities.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/sharonleo-su/pub-sub-currency-arbitrage.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pub-sub-currency-arbitrage
   ```

3. Install dependencies (ensure you have Python and pip installed):

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the arbitrage detection process, execute the following command:

```bash
python lab3.py
```

The program will subscribe to the forex price feed, update the graph with published prices, run the Bellman-Ford algorithm, and report any arbitrage opportunities detected.

## Files and Structure

- `bellman_ford.py`: Contains the implementation of the Bellman-Ford algorithm for detecting negative-weight cycles.
- `lab3.py`: Main driver program that subscribes to the forex price feed, constructs the graph, and performs arbitrage detection.
- `fxp_bytes.py`: Utility functions for constructing quote messages and decoding subscription requests.
- `forex_provider_v2.py`: Test publisher providing forex price data.
- `fxp_bytes_subscriber.py`: Utility functions inverses of those in `fxp_bytes.py` for deserializing data received from the publisher.

## Notes

- The subscription to the forex price feed lasts for 10 minutes.
- Published prices remain in force for 1.5 seconds or until superseded by a new rate for the same market.
- Quotes may arrive out of order due to the nature of UDP/IP communication.

## Contributions

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
