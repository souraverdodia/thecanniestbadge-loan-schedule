# Name: Nicholas Vickery
# Date: 9/25/2023
# Project: This program determines and outputs a payment schedule based on a loan.
# This program also saves the output into a structured file for the user to print and see the output in one selected area.

# Import the necessary modules
import os  # OS module allows for operating system dependent functionality
import json  # JSON module allows for JSON encoding and decoding

# Define a constant for the directory to save loan data files
SAVE_DIR = "loan_data/"

# Section for user input functions

def get_loan_details():
    # This function prompts the user for loan details and returns them

    # Ask the user if they want to save the loan data
    while True:
        save_data = input("Do you want to save the loan data? (yes/no): ").strip().lower()
        if save_data in ["yes", "no"]:
            save_data = save_data == "yes"
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    while True:
        try:
            # Get the loan amount from the user
            loan_amount = float(input("Enter the loan amount: "))
            if loan_amount > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            # Get the loan term in years from the user
            loan_term_years = int(input("Enter the loan term in years (0 if specifying in months): "))
            if loan_term_years >= 0:
                break
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            # Get any additional loan term in months from the user
            loan_term_months = int(input("Enter additional loan term in months: "))
            if loan_term_months >= 0:
                break
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    # Calculate the total loan term in months
    total_months = (loan_term_years * 12) + loan_term_months
    
    while True:
        try:
            # Get the annual interest rate for the loan from the user and convert it to a monthly rate
            loan_rate_annual = float(input("Enter the loan annual interest rate (as a percentage): "))
            if 0 <= loan_rate_annual <= 100:
                monthly_interest_rate = loan_rate_annual / 100 / 12
                break
            else:
                print("Please enter a percentage between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Calculate the monthly payment using the annuity formula, accounting for zero interest cases
    if monthly_interest_rate > 0:
        monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate)**-total_months)
    else:
        monthly_payment = loan_amount / total_months

    monthly_payment = round(monthly_payment, 2)

    # Return the gathered and calculated data
    return save_data, loan_amount, total_months, monthly_interest_rate, monthly_payment, loan_rate_annual

# Section for repayment schedule functions

def generate_repayment_schedule(loan_amount, total_months, monthly_interest_rate, monthly_payment):
    # This function generates a detailed repayment schedule for the loan

    # Initialize an empty list to hold the repayment details
    schedule = []

    # Set the initial remaining balance as the loan amount
    remaining_balance = loan_amount

    # Loop through each month to compute and store repayment details
    for month in range(1, total_months + 1):
        # Calculate the interest amount for the month
        interest_amount = remaining_balance * monthly_interest_rate
        # Calculate the principal portion of the payment for the month
        principal_amount = monthly_payment - interest_amount
        # Update the remaining balance after the payment
        remaining_balance -= principal_amount
        
        # checks to see if the last payment ends with a 0 
        if month == total_months:
            principal_amount += remaining_balance  # Adjust the last principal payment
            remaining_balance = 0  # Force the last balance to be 0


        # Add the details for the month to the schedule list
        schedule.append({
        'Payment #': month,
        'Beg Balance': round(loan_amount, 2),
        'Payment Amt': round(monthly_payment, 2),
        'Amt to Interest': round(interest_amount, 2),
        'Amt to Principle': round(principal_amount, 2),
        'End Balance': round(remaining_balance, 2)
        })
        
        # Update the starting balance for the next month
        loan_amount = remaining_balance

    # Return the generated schedule
    return schedule

def format_repayment_schedule(schedule):
    # This function takes the repayment schedule and formats it for display

    # Initialize an empty list to hold the formatted schedule
    formatted_schedule = []

    # Define a format string for the headers
    headers_format = "{:<10}{:<20}{:<20}{:<20}{:<20}{:<20}"

    # Loop through each entry in the schedule to format it
    for entry in schedule:
        formatted_entry = headers_format.format(entry['Payment #'], "{:.2f}".format(entry['Beg Balance']), "{:.2f}".format(entry['Payment Amt']), "{:.2f}".format(entry['Amt to Interest']), "{:.2f}".format(entry['Amt to Principle']), "{:.2f}".format(entry['End Balance']))
        formatted_schedule.append(formatted_entry)

    # Return the formatted schedule
    return formatted_schedule

# Section for file handling functions

def save_schedule_to_file(schedule, loan_details):
    # This function saves the repayment schedule and loan details to files

    # Define the paths for the files to save the schedule and details
    schedule_file_path = os.path.join(SAVE_DIR, "repayment_schedule.txt")
    details_file_path = os.path.join(SAVE_DIR, "loan_details.json")

    # Check if the save directory exists, and create it if not
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Save the formatted repayment schedule to a text file
    with open(schedule_file_path, "w") as file:
        # Write loan details to the file
        file.write("Loan Details:\n")
        file.write("Loan Amount: ${:.2f}\n".format(loan_details["Loan Amount"]))
        file.write("Total Months: {}\n".format(loan_details["Total Months"]))
        file.write("Annual Interest Rate: {:.2f}%\n".format(loan_details["Annual Interest Rate"]))
        file.write("Monthly Payment: ${:.2f}\n".format(loan_details["Monthly Payment"]))
        file.write("\n")

        # Write headers and a divider line
        headers_format = "{:<10}{:<20}{:<20}{:<20}{:<20}{:<20}"
        file.write(headers_format.format("Month", "Beginning Balance", "Payment Amount", "Amount to Interest", "Amount to Principle", "Ending Balance") + "\n")
        file.write("-" * 140 + "\n")

        # Write each entry of the schedule to the file
        for entry in schedule:
            file.write(entry + "\n")

    # Save the loan details to a JSON file
    with open(details_file_path, "w") as file:
        json.dump(loan_details, file)

    # Return the paths to the saved files
    return schedule_file_path, details_file_path

def retrieve_loan_details():
    # This function retrieves the saved loan details from a JSON file

    # Define the path to the file containing the loan details
    details_file_path = os.path.join(SAVE_DIR, "loan_details.json")

    # Check if the file exists, and if not, return None
    if not os.path.exists(details_file_path):
        return None

    # If the file exists, read the loan details from it and return them
    with open(details_file_path, "r") as file:
        loan_details = json.load(file)

    return loan_details

def print_repayment_schedule(formatted_schedule):
    # This function prints the formatted repayment schedule to the console

    # Print a header for the schedule and a divider line
    print("\nRepayment Schedule:")
    print("-" * 140)

    # Define and print the headers for each column
    headers_format = "{:<10}{:<20}{:<20}{:<20}{:<20}{:<20}"
    print(headers_format.format("Month", "Beginning Balance", "Payment Amount", "Amount to Interest", "Amount to Principle", "Ending Balance"))
    print("-" * 140)

    # Print each entry in the formatted schedule
    for line in formatted_schedule:
        print(line)

# Section for main execution

if __name__ == "__main__":
    # Ask the user if they want to retrieve saved loan details or input new ones
    retrieve_saved = input("Do you want to retrieve saved loan details? (yes/no): ").strip().lower() == "yes"
    
    if retrieve_saved:
        loan_details = retrieve_loan_details()
        if loan_details:
            loan_amount = loan_details["Loan Amount"]
            total_months = loan_details["Total Months"]
            loan_rate_annual = loan_details["Annual Interest Rate"]
            monthly_payment = loan_details["Monthly Payment"]
            monthly_interest_rate = loan_rate_annual / 100 / 12
            save_data = False
        else:
            print("No saved loan details found.")
            # You might want to either exit or ask for new details here
    else:
        # Get the loan details from the user
        save_data, loan_amount, total_months, monthly_interest_rate, monthly_payment, loan_rate_annual = get_loan_details()

    # Generate the repayment schedule based on the loan details
    repayment_schedule = generate_repayment_schedule(loan_amount, total_months, monthly_interest_rate, monthly_payment)

    # Format the schedule for display
    formatted_schedule = format_repayment_schedule(repayment_schedule)

    # Print the formatted schedule to the console
    print_repayment_schedule(formatted_schedule)

    # If the user chose to save the data, save the formatted schedule and loan details to files
    if save_data:
        loan_details = {
        "Loan Amount": loan_amount,
        "Total Months": total_months,
        "Annual Interest Rate": loan_rate_annual,
        "Monthly Payment": round(monthly_payment, 2)
        }   
        save_schedule_to_file(formatted_schedule, loan_details)


