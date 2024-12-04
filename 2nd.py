#Next features
#1. Detailed PDF reports of project materials and costs
#2. Support for different woods
#4. Multiple projects
#5. Conversion between metric and standard
#6. Customizable default sheet sizes
#7. Include Tax
#8. GUI

import math
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class WoodProject:
    def __init__(self, project_name):
        self.project_name = project_name
        self.plywood_pieces = []
        self.waste_tracking = []  # New attribute to track waste
        self.additional_materials = []

    def add_plywood_piece(self, length, width, quantity):
        piece = {
            "length": length,
            "width": width,
            "quantity": quantity
        }
        self.plywood_pieces.append(piece)
        print(f"Added {quantity} pieces: {length}\" x {width}\"")
    
    def new_plywood_piece(self):
        while True:
            try:
                length = float(input("Enter piece length (inches): "))
                width = float(input("Enter piece width (inches): "))
                quantity = int(input("Enter quantity needed: "))
                self.add_plywood_piece(length, width, quantity)
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

    def save_to_csv(self):
        save_file = input("Enter file name to save project to: ")
        file_name = f"{save_file}.csv"
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Length (in)", "Width (in)", "Quantity"])
            # Write each piece
            for piece in self.plywood_pieces:
                writer.writerow([piece["length"], piece["width"], piece["quantity"]])
        print(f"Project saved to {file_name}.")

    def read_from_csv(self):
        open_file = input("What is the name of the file")
        file_name = f"{open_file}.csv"
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
        print(f"\nTotal board feet required: {total_board_feet:.2f}")

    def add_additional_materials(self, name, price):
        material = {
            "name": name,
            "price": price
        }
        self.additional_materials.append(material)
        print(f"Added: {name} at ${price:.2f}")

    def new_additional_materials(self):
        while True:
            try:
                material_name = input("Enter the name of the material: ")
                material_price = float(input("Enter the price of the material: $"))
                self.add_additional_materials(material_name, material_price)
            except ValueError:
                print("Invalid input. Please enter numeric values for length, width, and quantity.")
                continue

            decision = input("Do you want to add another material? (y/n): ").lower()
            if decision == "y":
                continue
            elif decision == "n":
                break
            else:
                print("Invalid input.")
                break

    def price_calculator(self, sheet_price=0):
        """
        Calculate the total cost of plywood sheets and additional materials.
        """
        tax = float(input("What is the tax rate (%): "))

        if sheet_price <= 0:
            sheet_price = float(input("Enter the price per sheet of plywood: $"))
        total_sheets = self.calculate_plywood_sheets()
        plywood_cost = total_sheets * sheet_price
        
        # Calculate total cost of additional materials
        additional_materials_cost = sum(material['price'] for material in self.additional_materials)
        
        # Calculate overall cost
        total_cost = plywood_cost + additional_materials_cost
        total_cost_after_tax = total_cost + (total_cost* (tax / 100))
        total_tax = total_cost * tax
        # Display detailed cost breakdown
        print("\nCost Breakdown:")
        print(f"Total Sheets of Plywood: {total_sheets}")
        print(f"Plywood Cost: ${plywood_cost:.2f}")
        print(f"Additional Materials Cost: ${additional_materials_cost:.2f}")
        print(f"Subtotal: ${total_cost:.2f}")
        print(f"Total tax: ${total_tax:.2f}")
        print(f"Total Estimated Cost: ${total_cost_after_tax:.2f}")

    def calculate_plywood_sheets(self, sheet_length=96, sheet_width=48):
        total_sheets = 0
        self.waste_tracking = []  # Reset waste tracking

        for piece in self.plywood_pieces:
            if piece["length"] > sheet_length or piece["width"] > sheet_width:
                print(f"Warning: Piece {piece['length']}\" x {piece['width']}\" is larger than the sheet size!")
                continue

            sheets_needed = 0
            remaining_quantity = piece["quantity"]
            
            # Total usable area of a standard sheet
            sheet_total_area = sheet_length * sheet_width
            piece_area = piece["length"] * piece["width"]

            while remaining_quantity > 0:
                # Calculate how many pieces can fit on a sheet
                pieces_per_sheet_x = sheet_length // piece["length"]
                pieces_per_sheet_y = sheet_width // piece["width"]
                pieces_per_sheet = pieces_per_sheet_x * pieces_per_sheet_y

                if pieces_per_sheet == 0:
                    # If piece is too large, count as full sheet waste
                    sheets_needed += 1
                    remaining_quantity -= 1
                    waste_percentage = 100.0
                else:
                    # Determine pieces that can fit on this sheet
                    pieces_on_this_sheet = min(remaining_quantity, pieces_per_sheet)
                    
                    # Calculate area used and wasted
                    used_area = pieces_on_this_sheet * piece_area
                    waste_area = sheet_total_area - used_area
                    waste_percentage = (waste_area / sheet_total_area) * 100

                    sheets_needed += 1
                    remaining_quantity -= pieces_on_this_sheet

                # Track waste for this sheet
                self.waste_tracking.append({
                    "sheet_number": sheets_needed,
                    "piece_size": f"{piece['length']}x{piece['width']}",
                    "waste_percentage": waste_percentage
                })

            total_sheets += sheets_needed
            print(f"\n{sheets_needed} sheets needed for {piece['quantity']} pieces of size {piece['length']}\" x {piece['width']}\".")
        
        print(f"\nTotal sheets of plywood needed: {total_sheets}")
        return total_sheets

    def calculate_waste(self):
        """Calculate and display waste percentages"""
        if not self.waste_tracking:
            print("No waste data available. Run sheet calculation first.")
            return 0

        # Calculate average waste percentage
        total_waste_percentage = sum(waste['waste_percentage'] for waste in self.waste_tracking)
        average_waste_percentage = total_waste_percentage / len(self.waste_tracking)

        print("\nWaste Tracking Report:")
        for waste in self.waste_tracking:
            print(f"Sheet for {waste['piece_size']}: {waste['waste_percentage']:.2f}% waste")
        
        print(f"\nOverall Average Waste: {average_waste_percentage:.2f}%")
        return average_waste_percentage

    def generate_pdf_report(self, sheet_price=0):
        """
        Generate a comprehensive PDF report for the wood project, including additional materials.
        """
        # Ensure the 'reports' directory exists
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        # Prepare file path
        file_path = os.path.join('reports', f"{self.project_name}_report.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        
        # Prepare story (content) for the PDF
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Project: {self.project_name} - Material Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Materials List
        materials_title = Paragraph("Materials List", styles['Heading2'])
        story.append(materials_title)
        
        # Prepare table data
        table_data = [
            ['Length (in)', 'Width (in)', 'Quantity', 'Piece Area (sq in)', 'Total Area (sq in)']
        ]
        
        total_pieces = 0
        total_area = 0
        
        for piece in self.plywood_pieces:
            piece_area = piece['length'] * piece['width']
            total_area_for_piece = piece_area * piece['quantity']
            
            table_data.append([
                f"{piece['length']:.2f}",
                f"{piece['width']:.2f}",
                str(piece['quantity']),
                f"{piece_area:.2f}",
                f"{total_area_for_piece:.2f}"
            ])
            
            total_pieces += piece['quantity']
            total_area += total_area_for_piece
        
        # Create the table
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(t)
        
        # Cost Calculation
        if sheet_price <= 0:
            sheet_price = float(input("Enter the price per sheet of plywood: $"))
        tax = float(input("What is the tax rate (%): "))        
        total_sheets = self.calculate_plywood_sheets()
        plywood_cost = total_sheets * sheet_price

        # Additional Materials Cost
        additional_materials_cost = sum(material['price'] for material in self.additional_materials)
        
        # Total Cost
        total_cost = plywood_cost + additional_materials_cost
        total_cost_after_tax = total_cost + (total_cost * (tax / 100))
        total_tax = total_cost * tax
        # Cost Summary
        cost_summary = Paragraph("Cost Summary", styles['Heading2'])
        story.append(Spacer(1, 12))
        story.append(cost_summary)
        
        cost_data = [
            ['Total Pieces', str(total_pieces)],
            ['Total Area (sq in)', f"{total_area:.2f}"],
            ['Sheets Required', str(total_sheets)],
            ['Price per Sheet', f"${sheet_price:.2f}"],
            ['Plywood Cost', f"${plywood_cost:.2f}"],
            ['Additional Materials Cost', f"${additional_materials_cost:.2f}"],
            ['Subtotal', f"${total_cost:.2f}"],
            ['Tax rate', f"%{tax:.2f}"],
            ['Total tax', f"${total_tax:.2f}"]
            ['Total Estimated Cost', f"${total_cost_after_tax:.2f}"]
        ]
        
        cost_table = Table(cost_data)
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(cost_table)
        
        # List of Additional Materials
        if self.additional_materials:
            materials_summary = Paragraph("Additional Materials", styles['Heading2'])
            story.append(Spacer(1, 12))
            story.append(materials_summary)
            
            materials_data = [['Name', 'Price']]
            for material in self.additional_materials:
                materials_data.append([material['name'], f"${material['price']:.2f}"])
            
            materials_table = Table(materials_data)
            materials_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            story.append(materials_table)

# Waste Tracking Section
        waste_summary = Paragraph("Waste Tracking", styles['Heading2'])
        story.append(Spacer(1, 12))
        story.append(waste_summary)
        
        # Calculate waste if not already done
        if not self.waste_tracking:
            self.calculate_plywood_sheets()
        
        # Waste data table
        waste_data = [
            ['Sheet Number', 'Piece Size', 'Waste Percentage']
        ]
        
        total_waste_percentage = 0
        for waste in self.waste_tracking:
            waste_data.append([
                str(waste['sheet_number']),
                waste['piece_size'],
                f"{waste['waste_percentage']:.2f}%"
            ])
            total_waste_percentage += waste['waste_percentage']
        
        # Calculate average waste
        average_waste = total_waste_percentage / len(self.waste_tracking) if self.waste_tracking else 0
        
        # Add average waste to the table
        waste_data.append([
            'Average', 'Total Waste', f"{average_waste:.2f}%"
        ])
        
        # Create waste table
        waste_table = Table(waste_data)
        waste_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(waste_table)
        
        # Build PDF
        doc.build(story)
        
        print(f"PDF report generated: {file_path}")
        return file_path

def main():


    while True:
        print("\nWood Calculator Menu:")
        print("1. New Project")
        print("2. Add plywood piece")
        print("3. Calculate total sheets needed")
        print("4. Save to CSV")
        print("5. Load from CSV")
        print("6. Calculate board feet")
        print("7. Add additional materials")
        print("8. Price calculator")
        print("9. Generate PDF Report")
        print("10. Calculate Waste Percentage")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ")

        if choice == "1":
            project_name = input("Enter project name: ")
            project = WoodProject(project_name)

        elif choice == "2":
            project.new_plywood_piece()

        elif choice == "3":
            project.calculate_plywood_sheets()

        elif choice == "4":
            project.save_to_csv()

        elif choice == "5":
            project.read_from_csv()

        elif choice == "6":
            project.calculate_board_feet()

        elif choice == "7":
            project.new_additional_materials()

        elif choice == "8":
            project.price_calculator()

        elif choice == "9":
            project.generate_pdf_report()

        elif choice == "10":
            project.calculate_waste()

        elif choice == "11":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()