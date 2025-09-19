"""Menu-based entry point"""

from rich.console import Console
from trades import open_trade, close_trade, view_history

console = Console()

def main():
    while True:
        console.print("\n[bold yellow]Menu[/bold yellow]")
        console.print("1. Open Trade")
        console.print("2. Close Trade")
        console.print("3. View History")
        console.print("4. Exit")

        choice = input("Choose an option ...")

        if choice == "1":
            open_trade()
        elif choice == "2":
           close_trade()
        elif choice == "3":
           view_history()
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid choice, try again...[/red]")

if __name__ == "__main__":
    main()
