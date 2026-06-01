from bot.client import client
from bot.logger_config import logger


def place_market_order(symbol, side, quantity):

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        logger.info(f"MARKET order placed: {response}")

        return response

    except Exception as error:
        logger.error(f"MARKET order failed: {str(error)}")
        raise


def place_limit_order(symbol, side, quantity, price):

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )

        logger.info(f"LIMIT order placed: {response}")

        return response

    except Exception as error:
        logger.error(f"LIMIT order failed: {str(error)}")
        raise