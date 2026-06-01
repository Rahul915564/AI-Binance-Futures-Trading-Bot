from rich.console import Console
from rich.table import Table

from bot.orders import place_market_order, place_limit_order

from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

console = Console()


def show_order_details(order):

    table = Table(title="Order Details")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Order ID", str(order.get("orderId")))
    table.add_row("Symbol", str(order.get("symbol")))
    table.add_row("Side", str(order.get("side")))
    table.add_row("Type", str(order.get("type")))
    table.add_row("Status", str(order.get("status")))
    table.add_row("Executed Qty", str(order.get("executedQty")))

    console.print(table)


def main():

    console.print("\n[bold blue]Binance Futures Testnet Trading Bot[/bold blue]\n")

    try:
        symbol = validate_symbol(
            input("Enter Symbol (Example: BTCUSDT): ")
        )

        side = validate_side(
            input("Enter Side (BUY/SELL): ")
        )

        order_type = validate_order_type(
            input("Enter Order Type (MARKET/LIMIT): ")
        )

        quantity = validate_quantity(
            input("Enter Quantity: ")
        )

        if order_type == "MARKET":

            console.print("\nPlacing MARKET order...\n")

            order = place_market_order(
                symbol=symbol,
                side=side,
                quantity=quantity
            )

        else:
            price = validate_price(
                input("Enter Limit Price: ")
            )

            console.print("\nPlacing LIMIT order...\n")

            order = place_limit_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price
            )

        console.print(
            "\n[bold green]Order placed successfully![/bold green]\n"
        )

        show_order_details(order)

    except Exception as error:

        console.print(
            f"\n[bold red]Error:[/bold red] {str(error)}"
        )


if __name__ == "__main__":
    main()