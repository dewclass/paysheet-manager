import argparse

# Example usage
employee_file_path = 'employee_details.txt'
salary_file_path = 'salary_details.txt'
allowance_file_path = 'allowance_details.txt'


epf_percentage_employee = 8
epf_percentage_employer = 12
etf_percentage = 3


def check_duplicate_nic(file_path, nic):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    _, line_nic = line.split(',')
                    if line_nic == nic:
                        return True
    except FileNotFoundError:
        return False
    return False


def save_employee_details(file_path):
    while True:
        employee_name = input("Enter employee name (or 'q' to quit): ")
        if employee_name.lower() == 'q':
            break
        employee_nic = input("Enter employee NIC: ")
        if check_duplicate_nic(file_path, employee_nic):
            print("NIC already exists. Employee details not saved.")
            continue
        employee_details = {'Name': employee_name, 'NIC': employee_nic}
        with open(file_path, 'a') as file:
            file.write(
                f"{employee_details['Name']},{employee_details['NIC']}\n")



def get_employee_details(file_path):
    employee_details_list = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces and newline characters
            if line:  # Skip empty lines
                name, nic = line.split(',')
                employee_details = {'Name': name, 'NIC': nic}
                employee_details_list.append(employee_details)
    return employee_details_list


def get_employee_details_by_nic(file_path, nic):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                name, line_nic = line.split(',')
                if line_nic == nic:
                    return name, line_nic
    return None, None

def view_salary_details_by_nic(salary_file_path, nic):
    try:
        with open(salary_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    name, line_nic, salary, bonus = line.split(',')
                    if line_nic == nic:
                        print(f"Name: {name}, NIC: {line_nic}, Salary: {salary}, Bonus: {bonus}")
                        return
    except FileNotFoundError:
        print("Salary file not found.")

    print("Salary details not found for the provided")



def check_duplicate_allowance(file_path, allowance_name):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    existing_name, _ = line.split(',')
                    if existing_name == allowance_name:
                        return True
    except FileNotFoundError:
        return False
    return False


def add_allowance(file_path):
    allowance_name = input("Enter allowance name: ")

    if check_duplicate_allowance(file_path, allowance_name):
        print("Allowance already exists.")
        return

    allowance_amount = input("Enter allowance amount: ")

    with open(file_path, 'a') as file:
        file.write(f"{allowance_name},{allowance_amount}\n")

    print("Allowance added successfully.")


def add_salary_details(file_path, allowance_file_path, salary_file_path):
    nic_number = input("Enter NIC number: ")
    employee_found = False

    # Search for the employee based on NIC
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                name, line_nic = line.split(',')
                if line_nic == nic_number:
                    employee_found = True

                    # Prompt for salary details
                    salary = input("Enter salary: ")
                    bonus = input("Enter bonus: ")

                    # Select allowances from the allowance file
                    allowances = select_allowances(allowance_file_path)

                    # Append salary details to the salary file
                    with open(salary_file_path, 'a') as salary_file:
                        salary_file.write(f"{name},{nic_number},{salary},{bonus}")
                        for allowance_name, allowance_amount in allowances.items():
                            salary_file.write(f",{allowance_name},{allowance_amount}")
                        salary_file.write("\n")

                    print("Salary details added successfully.")

    if not employee_found:
        print("Employee not found.")

def select_allowances(allowance_file_path):
    allowances = {}

    # Read and display the available allowances
    with open(allowance_file_path, 'r') as allowance_file:
        lines = allowance_file.readlines()
        for i, line in enumerate(lines):
            allowance_name, allowance_amount = line.strip().split(',')
            allowances[i + 1] = (allowance_name, allowance_amount)
            print(f"{i + 1}. {allowance_name} ({allowance_amount})")

    selected_allowances = []

    # Prompt for selection of allowances
    while True:
        selection = input("Enter the number of the allowance (or 'q' to quit): ")
        if selection.lower() == 'q':
            break
        try:
            selection_index = int(selection)
            if 1 <= selection_index <= len(allowances):
                selected_allowances.append(allowances[selection_index])
                print(f"Selected: {allowances[selection_index][0]} ({allowances[selection_index][1]})")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

    return dict(selected_allowances)
def calculate_epf_employee_basic_salary(basic_salary, epf_percentage_employee):
    return (basic_salary * epf_percentage_employee) / 100

def calculate_epf_employer_basic_salary(basic_salary, epf_percentage_employer):
    return (basic_salary * epf_percentage_employer) / 100

def calculate_etf_basic_salary(basic_salary, etf_percentage):
    return (basic_salary * etf_percentage) / 100

def print_salary_slip_by_nic(file_path, salary_file_path, epf_percentage_employee, epf_percentage_employer, etf_percentage):
    nic = input("Enter NIC number: ")
    name, _ = get_employee_details_by_nic(file_path, nic)
    
    if name is None:
        print("Employee not found")
        return
    
    basic_salary, bonus = None, None
    
    with open(salary_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                fields = line.split(',')
                line_nic = fields[1]
                if line_nic == nic:
                    basic_salary = int(fields[2])
                    bonus = int(fields[3])
                    allowances = fields[4:]  # Fetch all allowances from the line
                    break
    
    if basic_salary is None or bonus is None:
        print("Salary details not found for the provided NIC")
        return
    
    month = input("Enter month: ")
    
    print("********** Salary Slip **********")
    print(f"Month: {month}")
    print(f"Employee Name: {name}")
    print(f"NIC: {nic}")
    print(f"Basic Salary: {basic_salary}")
    print(f"Bonus: {bonus}")
    
    total_allowances = 0
    
    # Display the individual allowances and calculate the total allowance amount
    for i in range(0, len(allowances), 2):
        allowance_name = allowances[i]
        allowance_amount = int(allowances[i + 1])
        print(f"{allowance_name}: {allowance_amount}")
        total_allowances += allowance_amount
    
    print("--------")
    print(f"Total Allowances: {total_allowances}")
    
    epf_employee = calculate_epf_employee_basic_salary(basic_salary, epf_percentage_employee)
    epf_employer = calculate_epf_employer_basic_salary(basic_salary, epf_percentage_employer)
    etf_basic = calculate_etf_basic_salary(basic_salary, etf_percentage)
    
    print(f"EPF (Employer): {epf_employer}")
    print(f"EPF (Employee): {epf_employee}")
    print(f"ETF: {etf_basic}")
    
    total_salary = basic_salary + bonus + total_allowances
    total_deductions = epf_employee + etf_basic
    net_salary = total_salary - total_deductions
    
    print("--------")
    print(f"Total Salary: {total_salary}")
    print(f"Total Deductions: {total_deductions}")
    print(f"Net Salary: {net_salary}")
    print("*********************************")


# Create the command-line argument parser
parser = argparse.ArgumentParser(description='Select function to run')
parser.add_argument('action', choices=['view-all', 'add-new','view-by-nic',
                                       'add-salary',"add-allowance","print-salary"],
                    help='The action to run')

# Parse the command-line arguments
args = parser.parse_args()

# Call the selected function
if args.action == 'view-all':
    # Example usage
    employees = get_employee_details(employee_file_path)
    for employee in employees:
        print(f"Name: {employee['Name']}, NIC: {employee['NIC']}")
elif args.action == 'add-new':
    save_employee_details(employee_file_path)
elif args.action == 'view-by-nic':
    nic_number = input("Enter NIC number: ")
    name, nic = get_employee_details_by_nic(employee_file_path, nic_number)
    if name and nic:
        print(f"Name: {name}, NIC: {nic}")
    else:
        print("Employee not found")    

    view_salary_details_by_nic(salary_file_path,nic)
    
elif args.action == "add-salary":
    add_salary_details(employee_file_path, allowance_file_path, salary_file_path)

elif args.action == "add-allowance":
    add_allowance(allowance_file_path)

elif args.action == "print-salary":
    print_salary_slip_by_nic(employee_file_path,salary_file_path,epf_percentage_employee,
                             epf_percentage_employer,etf_percentage)