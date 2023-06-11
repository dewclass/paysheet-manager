import argparse

# Example usage
employee_file_path = 'employee_details.txt'
salary_file_path = 'salary_details.txt'

def check_duplicate_nic(file_path, nic):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                _, line_nic = line.split(',')
                if line_nic == nic:
                    return True
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

def add_salary_details(file_path, salary_file_path):
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

                    # Append salary details to the salary file
                    with open(salary_file_path, 'a') as salary_file:
                        salary_file.write(f"{name},{nic_number},{salary},{bonus}\n")

                    print("Salary details added successfully.")

    if not employee_found:
        print("Employee not found.")


def view_salary_details_by_nic(salary_file_path, nic):
    with open(salary_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                name, line_nic, salary, bonus = line.split(',')
                if line_nic == nic:
                    print(f"Name: {name}, NIC: {line_nic}, Salary: {salary}, Bonus: {bonus}")
                    return

    print("Salary details not found for the provided NIC.")



# Create the command-line argument parser
parser = argparse.ArgumentParser(description='Select function to run')
parser.add_argument('action', choices=['view-all', 'add-new','view-by-nic','add-salary'],
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
    add_salary_details(employee_file_path, salary_file_path)