#Python
import math

class WoodProject:
    def __init__(self, project_name):
        self.project_name = project_name
        self.plywood_pieces = []
        self.total_cost = 0

    def add_plywood_piece(self, length, width, quantity):
        piece = {
            "length": length,
            "width": width,
            "quantity": quantity
        }
        self.plywood_pieces.append(piece)
        print(f"Added {quantity} pieces: {length}\" x {width}\"")

    def calculate_plywood_sheets(self, sheet_length=96, sheet_width=48):
        total_sheets = 1

        for piece in self.plywood_pieces:
            if piece["length"] > sheet_length or piece["width"] > sheet_width:
                print(f"Warning: Piece {piece['length']}\" x {piece['width']}\" is larger than sheet size!")
                continue

            remaining_length = sheet_length
            remaining_width = sheet_width
            sheets_needed = 0

            while piece["quantity"] > 0:
                # Check if the piece can fit on the remaining space
                if piece["length"] <= remaining_length and piece["width"] <= remaining_width:
                    # Piece can fit, so we use the remaining space
                    remaining_length -= piece["length"]
                    remaining_width -= piece["width"]
                    piece["quantity"] -= 1
                else:
                    # Piece can't fit, so we need a new sheet
                    sheets_needed += 1
                    remaining_length = sheet_length
                    remaining_width = sheet_width

            total_sheets += sheets_needed

            print(f"\nFor pieces {piece['length']}\" x {piece['width']}\":")

        return total_sheets

def main():
    project_name = input("What is the project name: ")
    project = WoodProject(project_name)

    loop = True
    while loop == True:
        print("\nWood Calculator Menu:")
        print("1. Add plywood piece")
        print("2. Calculate total sheets needed")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":

            add_loop = True
            while True:

                length = float(input("Enter piece length (inches): "))
                width = float(input("Enter piece width (inches): "))
                quantity = int(input("Enter quantity needed: "))
                project.add_plywood_piece(length, width, quantity)

                decision = input("Do you want to add another piece (y/n) ")

                if decision.lower() == "y":
                    continue

                elif decision.lower() == "n":
                    add_loop = False
                    break
                
                else:
                    print("Invlaid choice. Please try again.")

        elif choice == "2":
            sheets = project.calculate_plywood_sheets()
            print(f"\nTotal shees of plywood needed: {sheets}")

        elif choice == "3":
            print("Goodbye!")
            loop = False

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()