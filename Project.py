import math
import csv

class WoodProject:
    def __init__(self, project_name):
        self.project_name = project_name
        self.plywood_pieces = []

    def add_plywood_piece(self, length, width, quantity):
        piece = {
            "length": length,
            "width": width,
            "quantity": quantity
        }
        self.plywood_pieces.append(piece)
        print(f"Added {quantity} pieces: {length}\" x {width}\"")

    def calculate_plywood_sheets(self, sheet_length=96, sheet_width=48):
        total_sheets = 0

        for piece in self.plywood_pieces:
            if piece["length"] > sheet_length or piece["width"] > sheet_width:
                print(f"Warning: Piece {piece['length']}\" x {piece['width']}\" is larger than the sheet size!")
                continue

            sheets_needed = 0
            remaining_quantity = piece["quantity"]

            while remaining_quantity > 0:
                pieces_per_sheet = (sheet_length // piece["length"]) * (sheet_width // piece["width"])
                if pieces_per_sheet == 0:
                    sheets_needed += 1
                    remaining_quantity -= 1
                else:
                    sheets_needed += math.ceil(remaining_quantity / pieces_per_sheet)
                    break

            total_sheets += sheets_needed
            print(f"{sheets_needed} sheets needed for {piece['quantity']} pieces of size {piece['length']}\" x {piece['width']}\".")

        return total_sheets

    def save_to_csv(self):
        file_name = f"{self.project_name}.csv"
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Length (in)", "Width (in)", "Quantity"])
            # Write each piece
            for piece in self.plywood_pieces:
                writer.writerow([piece["length"], piece["width"], piece["quantity"]])
        print(f"Project saved to {file_name}.")

    def read_from_csv(self):
        file_name = f"{self.project_name}.csv"
        try:
            with open(file_name, mode="r") as file:
                reader = csv.DictReader(file)
                self.plywood_pieces = []
                for row in reader:
                    piece = {
                        "length": float(row["Length (in)"]),
                        "width": float(row["Width (in)"]),
                        "quantity": int(row["Quantity"])
                    }
                    self.plywood_pieces.append(piece)
            print(f"Project loaded from {file_name}.")
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def calculate_board_feet(self):
        total_board_feet = 0
        for piece in self.plywood_pieces:
            piece_area = (piece["length"] * piece["width"]) / 144  
            total_board_feet += piece_area * piece["quantity"]
        print(f"Total board feet required: {total_board_feet:.2f}")

    def price_calculator(self, sheet_price=0):
        if sheet_price <= 0:
            sheet_price = float(input("Enter the price per sheet of plywood: "))
        total_sheets = self.calculate_plywood_sheets()
        total_cost = total_sheets * sheet_price
        print(f"Estimated total cost: ${total_cost:.2f}")


def main():
    project_name = input("What is the project name: ")
    project = WoodProject(project_name)

    while True:
        print("\nWood Calculator Menu:")
        print("1. Add plywood piece")
        print("2. Calculate total sheets needed")
        print("3. Save to CSV")
        print("4. Load from CSV")
        print("5. Calculate board feet")
        print("6. Price calculator")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            while True:
                try:
                    length = float(input("Enter piece length (inches): "))
                    width = float(input("Enter piece width (inches): "))
                    quantity = int(input("Enter quantity needed: "))
                    project.add_plywood_piece(length, width, quantity)
                except ValueError:
                    print("Invalid input. Please enter numeric values for length, width, and quantity.")
                    continue

                decision = input("Do you want to add another piece? (y/n): ").lower()
                if decision == "y":
                    continue
                elif decision == "n":
                    break
                else:
                    print("Invalid choice. Returning to the main menu.")
                    break

        elif choice == "2":
            sheets = project.calculate_plywood_sheets()
            print(f"\nTotal sheets of plywood needed: {sheets}")

        elif choice == "3":
            project.save_to_csv()

        elif choice == "4":
            project.read_from_csv()

        elif choice == "5":
            project.calculate_board_feet()

        elif choice == "6":
            project.price_calculator()

        elif choice == "7":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
