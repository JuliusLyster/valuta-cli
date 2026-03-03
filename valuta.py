import argparse
import os
import sys
import requests
from dotenv import load_dotenv

ENV_FILE = ".env"

def save_api_key(key: str):
    """Gemmer API nøglen i .env filen"""
    with open(ENV_FILE, "w") as f:
        f.write(f"API_KEY={key}\n")
    print(f" API nøgle gemt i {ENV_FILE}\n")

def load_api_key() -> str:
    """Indlæser API nøglen fra .env filen"""
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        print(" Ingen API nøgle fundet!")
        print("   Kør programmet første gang med: python3 valuta.py --key DIN_NØGLE")
        sys.exit(1)
    return key

def get_exchange_rates(api_key: str, base_currency: str) -> dict:
    """Henter valutakurser fra exchangerate-api.com"""
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency.upper()}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("result") == "error":
            error = data.get("error-type", "Ukendt fejl")
            if error == "invalid-key":
                print(" Ugyldig API nøgle. Tjek din nøgle og prøv igen.")
            elif error == "unsupported-code":
                print(f" Valutakoden '{base_currency}' understøttes ikke.")
            else:
                print(f" API fejl: {error}")
            sys.exit(1)
        
        return data["conversion_rates"]
    
    except requests.exceptions.ConnectionError:
        print(" Ingen internetforbindelse. Tjek din forbindelse og prøv igen.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(" Forespørgslen tog for lang tid. Prøv igen.")
        sys.exit(1)

def convert_currency(rates: dict, amount: float, from_currency: str, to_currency: str) -> float:
    """Omregner et beløb fra én valuta til en anden"""
    from_upper = from_currency.upper()
    to_upper = to_currency.upper()
    
    if from_upper not in rates:
        print(f" Valutakoden '{from_currency}' kendes ikke.")
        sys.exit(1)
    if to_upper not in rates:
        print(f" Valutakoden '{to_currency}' kendes ikke.")
        sys.exit(1)
    
    # Konverter via base rate
    rate = rates[to_upper] / rates[from_upper]
    return amount * rate

def list_currencies(rates: dict):
    """Viser alle tilgængelige valutaer"""
    print("\n Tilgængelige valutaer:\n")
    currencies = sorted(rates.keys())
    # Print i kolonner
    for i, currency in enumerate(currencies):
        print(f"  {currency:<6}", end="")
        if (i + 1) % 10 == 0:
            print()
    print("\n")

def main():
    parser = argparse.ArgumentParser(
        prog="valuta.py",
        description=" Valutaomregner - omregn beløb mellem verdens valutaer",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Eksempler:
  Første gang (gem API nøgle):
    python3 valuta.py --key DIN_API_NØGLE

  Omregn 100 DKK til USD:
    python3 valuta.py --from DKK --to USD --amount 100

  Omregn 50 EUR til THB:
    python3 valuta.py --from EUR --to THB --amount 50

  Se alle tilgængelige valutaer:
    python3 valuta.py --list

  Brug anden API nøgle denne gang:
    python3 valuta.py --key NY_NØGLE --from DKK --to USD --amount 200
        """
    )

    parser.add_argument(
        "--key",
        metavar="API_NØGLE",
        help="Din API nøgle fra exchangerate-api.com\n(gemmes automatisk til .env til næste gang)"
    )
    parser.add_argument(
        "--from",
        dest="from_currency",
        metavar="VALUTA",
        help="Valuta du vil omregne FRA (f.eks. DKK)"
    )
    parser.add_argument(
        "--to",
        dest="to_currency",
        metavar="VALUTA",
        help="Valuta du vil omregne TIL (f.eks. USD)"
    )
    parser.add_argument(
        "--amount",
        type=float,
        metavar="BELØB",
        help="Beløb der skal omregnes (f.eks. 100)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Vis alle tilgængelige valutaer"
    )

    args = parser.parse_args()

    print(" Valutaomregner\n" + "─" * 30)

    # Håndter API nøgle
    if args.key:
        save_api_key(args.key)
        api_key = args.key
    else:
        api_key = load_api_key()

    # Vis valutaer
    if args.list:
        rates = get_exchange_rates(api_key, "USD")
        list_currencies(rates)
        return

    # Omregn valuta
    if args.from_currency and args.to_currency and args.amount is not None:
        rates = get_exchange_rates(api_key, "USD")
        result = convert_currency(rates, args.amount, args.from_currency, args.to_currency)
        
        print(f"\n  {args.amount:,.2f} {args.from_currency.upper()}")
        print(f"  = {result:,.2f} {args.to_currency.upper()}")
        rate = result / args.amount
        print(f"\n  Kurs: 1 {args.from_currency.upper()} = {rate:.4f} {args.to_currency.upper()}\n")
        return

    # Hvis ingen argumenter — vis hjælp
    if not args.key:
        parser.print_help()

if __name__ == "__main__":
    main()