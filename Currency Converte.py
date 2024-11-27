import requests
from typing import Optional

class CurrencyConverter:
    def __init__(self, api_url: str = "https://api.exchangerate-api.com/v4/latest/"):
        """
        Initializes the CurrencyConverter with the given API URL.
        :param api_url: The URL for the API endpoint (defaults to 'https://api.exchangerate-api.com/v4/latest/')
        """
        self.api_url = api_url

    def _get_exchange_rates(self, from_currency: str) -> Optional[dict]:
        """
        Fetches the exchange rates for the given base currency.
        :param from_currency: The base currency code (e.g., USD, EUR)
        :return: A dictionary containing exchange rates, or None if the request fails.
        """
        try:
            response = requests.get(f"{self.api_url}{from_currency}")
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            return data.get("rates")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return None

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[str]:
        """
        Converts the given amount from one currency to another.
        :param amount: The amount to convert
        :param from_currency: The currency to convert from (e.g., USD)
        :param to_currency: The currency to convert to (e.g., EUR)
        :return: The converted amount as a formatted string, or None if there's an error.
        """
        # Fetch exchange rates
        rates = self._get_exchange_rates(from_currency)
        if not rates:
            return None

        # Check if the target currency is in the exchange rates
        if to_currency not in rates:
            print(f"Error: '{to_currency}' is not available in exchange rates.")
            return None

        # Calculate the converted amount
        exchange_rate = rates[to_currency]
        converted_amount = round(amount * exchange_rate, 2)

        return f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."

def main():
    while True:
        # User input handling
        try:
            amount = float(input("Enter the amount to convert: "))
            from_currency = input("Enter the currency to convert from (e.g., USD): ").upper()
            to_currency = input("Enter the currency to convert to (e.g., EUR): ").upper()

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue  # Prompts for new input without exiting the loop
            
            converter = CurrencyConverter()
            result = converter.convert(amount, from_currency, to_currency)
            
            if result:
                print(result)
            else:
                print("Conversion failed due to an error.")
            
            # Option to repeat or exit
            continue_conversion = input("\nDo you want to convert another currency? (yes/no): ").strip().lower()
            if continue_conversion != 'yes':
                print("Thank you for using the Currency Converter!")
                break  # Exit the loop and the program

        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")

if __name__ == "__main__":
    main()
