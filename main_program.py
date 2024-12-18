def login(pos):
    un_list, pw_list, ps_list = [], [], []
    with open("login.txt", "r") as f:
        for line in f:
            un_list.append(line.strip().split(",")[0])
            pw_list.append(line.strip().split(",")[1])
            ps_list.append(line.strip().split(",")[2])
    attempt = 1
    while attempt <= 3:
        print(f"-----------------Attempt {attempt}-----------------")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        for i in range(len(un_list)):
            if username == un_list[i] and password == pw_list[i] and pos == ps_list[i]:
                print("Login Successful")
                print("------------------------------------")
                return True, username, pos
        attempt += 1
        if username in un_list:
            i = un_list.index(username)  # locate index of username to find corresponding password and position
            if password == pw_list[i]:
                print("Permission to access the selected position is DENIED")
                print(f"You only have the permission to access position - {ps_list[i].upper()}")
                dcs = input("Do you wish to continue?\nPress 'ENTER' to continue or type 'n' to login again: ").lower()
                if dcs != "n":
                    print("Login Successful")
                    print("------------------------------------")
                    return True, username, ps_list[i]
            else:
                print("Incorrect password")
        else:
            print("Incorrect username")
    print("No more attempt")
    return False, None, None


def password_validation(password):
    while True:
        flag1, flag2, flag3 = 0, 0, 0
        if len(password) < 6:
            print("Password must be at least 6 characters")
            password = input("Enter Password: ")
            continue
        for i in password:
            if i.islower():
                flag1 += 1
            elif i.isupper():
                flag2 += 1
            elif i.isdigit():
                flag3 += 1
        if flag1 >= 1 and flag2 >= 1 and flag3 >= 1:
            print("Valid Password")
            return password
        else:
            print("Password must be a combination of uppercase letters, lowercase letters and numbers")
            password = input("Enter Password: ")


# -----------------------------------------Receptionist------------------------------------------------------
def receptionist_register():
    login_file = open("login.txt", "a")
    un = input("Enter customer username: ").strip()
    password = input("Enter customer password: ").strip()
    valid_password = password_validation(password)
    login_file.write(f"{un},{valid_password},customer\n")
    login_file.close()
    with open("customer.txt", "a") as f:
        # Username|Password|Email|Home Address|Contact Number
        f.write(f"{un},{password},-,-,-\n")
    print("Record Added")


def assign_services():
    un_list = []
    with open("customer.txt", "r") as f:
        for line in f:
            un_list.append(line.strip().split(",")[0])
    while True:
        cus_username = input("Enter customer username: ")
        if cus_username in un_list:
            break
        else:
            print("Customer not found. Please try again")

    service_type = [0, "Remove virus, malware or spyware", "Troubleshot and fix computer running slow",
                    "Laptop screen replacement", "Laptop battery replacement",
                    "Operating System Format and Installation", "Data backup and recovery"]
    print("-----------service type-----------")
    for i in range(1, len(service_type)):
        print(f"{i},{service_type[i]}")
    print("----------------------------------")
    index = int(input("Enter customer service type: "))
    normal = [0, 50, 60, 380, 180, 100, 80]
    urgent = [0, 80, 90, 430, 210, 150, 130]
    urgency = str(input("normal or urgent: ")).lower().strip()
    if urgency == "normal":
        price = int(normal[index])
    elif urgency == "urgent":
        price = int(urgent[index])
    else:
        price = 0

    with open("service.txt", "a") as f:
        # Username|Type of Service|Urgency|Price|Description|Collection Date|Status|Payment
        f.write(f"{cus_username}|{service_type[index]}|{urgency}|{price}|-|-|Incomplete|Pending\n")
    print("Record Added")


def payment_receipt():
    un_list = []
    with open("service.txt", "r") as f:
        for line in f:
            un_list.append(line.strip().split("|")[0])
    while True:
        customer_username = input("Enter customer username: ")
        if customer_username in un_list:
            break
        else:
            print("Customer not found. Please try again")
    with open("service.txt", "r") as f:
        for line in f:
            if line.startswith(customer_username):
                services = line.strip().split("|")[1]
                price = int(line.strip().split("|")[3])
    print("Total Amount: RM", price)
    payment = float(input("Enter amount paid by customer: RM "))
    change = payment - price
    print("----------Receipt----------")
    print(f"-------Service type-------")
    print(f"1. {services}")
    print("---------------------------")
    print(f"Total: RM{price:.2f}\nAmount paid: RM{payment:.2f}\nChange: RM{change:.2f}")
    print("---------------------------\n")

    # add payment status 'Done' into text file
    with open("service.txt", "r") as f:
        updated_lines = []
        lines = f.readlines()
        for line in lines:
            if line.startswith(customer_username):
                new_line = line.replace("Pending", "Paid")
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)
    with open("service.txt", "w") as f:
        f.writelines(updated_lines)


def receptionist_update_profile(un):
    username_list, password_list, ps_list = [], [], []
    un_list, pw_list, name_list, contact_list, email_list = [], [], [], [], []
    with open("receptionist.txt", "r") as f:
        for line in f:
            un_list.append(line.strip().split(",")[0])
            pw_list.append(line.strip().split(",")[1])
            name_list.append(line.strip().split(",")[2])
            contact_list.append(line.strip().split(",")[3])
            email_list.append(line.strip().split(",")[4])
    with open("login.txt", "r") as g:
        for line in g:
            username_list.append(line.strip().split(",")[0])
            password_list.append(line.strip().split(",")[1])
            ps_list.append(line.strip().split(",")[2])

    i = un_list.index(un)
    i2 = username_list.index(un)
    choices = int(input("Please choose which personal information that want to change\n1.Password\n"
                        "2.Full Name\n3.Contact number\n4.Email address\nEnter your choice: "))

    match choices:
        case 1:
            pw = input("Please enter new password: ")
            new = password_validation(pw)
            pw_list[i] = new
            password_list[i2] = new
            with open("login.txt", "r") as f:
                lines = f.readlines()
            lines[i2] = f"{username_list[i2]},{password_list[i2]},{ps_list[i2]}\n"
            with open("login.txt", "w") as f:
                f.writelines(lines)
        case 2:
            new = input("Please enter new full name: ")
            name_list[i] = new
        case 3:
            new = int(input("Please enter new contact number: "))
            contact_list[i] = new
        case 4:
            new = input("Please enter new email address: ")
            email_list[i] = new

    with open("receptionist.txt", "r") as F:
        lines = F.readlines()
    lines[i] = f"{un_list[i]},{pw_list[i]},{name_list[i]},{contact_list[i]},{email_list[i]}\n"
    with open("receptionist.txt", "w") as F:
        F.writelines(lines)
    print("Profile updated successfully")


# -----------------------------------------Technician--------------------------------------------------------
def view_services():
    username, services, urgency, price, status = [], [], [], [], []
    f = open("service.txt", "r")
    for line in f:
        username.append(line.strip().split("|")[0])
        services.append(line.strip().split("|")[1])
        urgency.append(line.strip().split("|")[2])
        price.append(line.strip().split("|")[3])
        status.append(line.strip().split("|")[6])
    print("-" * 130)
    print("{:^20}{:^50}{:^20}{:^20}{:^20}".format("username", "services", "urgency", "price", "status"))
    print("-" * 130)
    for i in range(len(username)):
        print("{:^20}{:^50}{:^20}{:^20}{:^20}".format
              (f"{username[i]}", f"{services[i]}", f"{urgency[i]}", f"{price[i]}", f"{status[i]}"))
    print(("-" * 130) + "\n")


def add_des_date():
    username_list = []
    f = open("service.txt", "r")
    for line in f:
        username_list.append(line.strip().split("|")[0])
    f.close()
    while True:
        cus_name = str(input("please enter customer username: "))
        if cus_name in username_list:
            break
        else:
            print("User not found!")
    updated_lines, record = [], []
    f = open("service.txt", "r")
    for line in f:
        if line.startswith(cus_name):
            record = (line.strip().split("|"))
            continue
        updated_lines.append(line)
    print(f"Username: {cus_name} ")
    print(f"Service: {record[1]}")
    print(f"Description: {record[4]}")
    print(f"Collection Date: {record[5]}")
    print("----------------------------------------")
    des = str(input("Enter Description: "))
    date = input("Enter Date (DD/MM/YY): ")
    new_line = "|".join(record[:4]) + "|" + des + "|" + date + "|" + "Completed" + "|" + record[7] + "\n"
    updated_lines.append(new_line)
    with open("service.txt", "w") as f:
        f.writelines(updated_lines)
    print("Update Completed")


def technician_update_profile(tech_name):
    updated_lines, record = [], []
    f = open("technician.txt", "r")
    for line in f:
        if line.startswith(tech_name):
            record = (line.strip().split(","))
            continue
        updated_lines.append(line)
    while True:
        print("----------MENU------------")
        print("1.Add Contact Number.\n2.Add Email.\n3.Change Password.")
        choices = int(input("Enter Your Choice: "))
        match choices:
            case 1:
                cnum = input("Enter Contact Number: ")
                new_line = ",".join(record[:2]) + "," + cnum + "," + record[3] + "\n"
                break
            case 2:
                email = input("Enter Email: ")
                new_line = ",".join(record[:3]) + "," + email + "\n"
                break
            case 3:
                pw = input("Enter New Password: ")
                new_pw = password_validation(pw)
                new_line = record[0] + "," + new_pw + "," + ",".join(record[2:]) + "\n"
                updated_login_file = []
                with open("login.txt", "r") as f:
                    for line in f:
                        if line.startswith(tech_name):
                            credentials = line.strip().split(",")
                            continue
                        updated_login_file.append(line)
                new_credentials = f"{credentials[0]},{new_pw},{credentials[2]}\n"
                updated_login_file.append(new_credentials)
                with open("login.txt", "w") as f:
                    f.writelines(updated_login_file)
                break
            case _:
                print("Invalid input.")
    updated_lines.append(new_line)
    with open("technician.txt", "w") as f:
        f.writelines(updated_lines)
    print("Update Completed")


# --------------------------------------------Customer----------------------------------------------------
def change_requested_service(cus_name):
    username_list = []
    f = open("service.txt", "r")
    for line in f:
        username_list.append(line.strip().split("|")[0])
    f.close()
    if cus_name not in username_list:
        print("Record not found. You haven't requested a service")
        return

    updated_lines, record = [], []
    f = open("service.txt", "r")
    for line in f:
        if line.startswith(cus_name):
            record = (line.strip().split("|"))
            continue
        updated_lines.append(line)
    f.close()
    print("----------------------------------------")
    print(f"Username: {cus_name} ")
    print(f"Service: {record[1]}")
    print(f"Urgency: {record[2]}")
    print(f"Service fee: RM{record[3]}")
    print(f"Status: {record[6]}")
    if record[6] == "Incomplete":
        print("--------------------------------------------------------------------------------------------------------"
              "-----------")
        print("{:^10}{:^50}{:^60}".format("No", "Service type", "Service fee"))
        print("--------------------------------------------------------------------------------------------------------"
              "-----------")
        print("{:^60}{:^30}{:^30}".format("", "Normal", "Urgent"))
        print("--------------------------------------------------------------------------------------------------------"
              "-----------")
        print("{:^10}{:^50}{:^30}{:^30}".format("1", "Remove virus, malware or spyware", "RM 50", "RM 80"))
        print("{:^10}{:^50}{:^30}{:^30}".format("2", "Troubleshot and fix computer running slow", "RM 60", "RM 90"))
        print("{:^10}{:^50}{:^30}{:^30}".format("3", "Laptop screen replacement", "RM 380", "RM 430"))
        print("{:^10}{:^50}{:^30}{:^30}".format("4", "Laptop battery replacement", "RM 180", "RM 210"))
        print("{:^10}{:^50}{:^30}{:^30}".format("5", "Operating System Format and Installation", "RM 100", "RM 150"))
        print("{:^10}{:^50}{:^30}{:^30}".format("6", "Data backup and recovery", "RM 80", "RM 130"))

        choices = int(input("Please enter the service to be changed: "))
        match choices:
            case 1:
                service_change = "Remove virus, malware or spyware"
            case 2:
                service_change = "Troubleshoot and fix computer running slow"
            case 3:
                service_change = "Laptop screen replacement"
            case 4:
                service_change = "Laptop battery replacement"
            case 5:
                service_change = "Operating System Format and Installation"
            case 6:
                service_change = "Data backup and recovery"
            case _:
                service_change = ""
                print("Invalid input")

        service_fee = 0
        urgency = str(input("urgent or normal: "))
        if choices == 1 and urgency == "normal":
            service_fee = 50
        elif choices == 1 and urgency == "urgent":
            service_fee = 80
        elif choices == 2 and urgency == "normal":
            service_fee = 60
        elif choices == 2 and urgency == "urgent":
            service_fee = 90
        elif choices == 3 and urgency == "normal":
            service_fee = 380
        elif choices == 3 and urgency == "urgent":
            service_fee = 430
        elif choices == 4 and urgency == "normal":
            service_fee = 180
        elif choices == 4 and urgency == "urgent":
            service_fee = 210
        elif choices == 5 and urgency == "normal":
            service_fee = 100
        elif choices == 5 and urgency == "urgent":
            service_fee = 150
        elif choices == 6 and urgency == "normal":
            service_fee = 80
        elif choices == 6 and urgency == "urgent":
            service_fee = 130

        new_line = (record[0] + "|" + service_change + "|" + urgency + "|"
                    + str(service_fee) + "|" + "|".join(record[4:])) + "\n"
        updated_lines.append(new_line)
        with open("service.txt", "w") as f:
            f.writelines(updated_lines)
        print("Update Completed")

    else:
        print("Your requested service has been done. You are not allowed to change service anymore.")


def view_service_description(cus_name):
    username_list = []
    f = open("service.txt", "r")
    for line in f:
        username_list.append(line.strip().split("|")[0])
    f.close()
    if cus_name not in username_list:
        print("Record not found. You haven't requested a service")
        return

    record = []
    f = open("service.txt", "r")
    for line in f:
        if line.startswith(cus_name):
            record = (line.strip().split("|"))
    f.close()
    if record[6] == "Completed":
        print("------------------------------------")
        print(f"Username: {cus_name} ")
        print(f"Service: {record[1]}")
        print(f"Description: {record[4]}")
        print(f"Collection Date: {record[5]}")
        print(f"Total amount to be paid: RM{record[3]}")
    else:
        print("Your requested service is still in progress.")


def customer_update_profile(cust_name):
    print("Please update your profile\n 1.Email\n 2.Home address\n 3.Contact number\n 4.Password")
    updated_lines, record = [], []
    f = open("customer.txt", "r")
    for line in f:
        if line.startswith(cust_name):
            record = (line.strip().split(","))
            continue
        updated_lines.append(line)
    f.close()
    choices = int(input("Please choose which profile to update: "))
    if choices == 1:
        e_mail = str(input("Please enter your Email:"))
        new_line = record[0] + "," + record[1] + "," + e_mail + "," + record[3] + "," + record[4] + "\n"
    elif choices == 2:
        home_address = str(input("Please enter your Home address:"))
        new_line = record[0] + "," + record[1] + "," + record[2] + "," + home_address + "," + record[4] + "\n"
    elif choices == 3:
        contact_number = str(input("Please enter your Contact number:"))
        new_line = record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "," + contact_number + "\n"
    elif choices == 4:
        password = str(input("Please enter your new Password:"))
        new_password = password_validation(password)
        new_line = record[0] + "," + new_password + "," + record[2] + "," + record[3] + "," + record[4] + "\n"
        updated_login_file = []
        with open("login.txt", "r") as f:
            for line in f:
                if line.startswith(cust_name):
                    credentials = line.strip().split(",")
                    continue
                updated_login_file.append(line)
        new_credentials = f"{credentials[0]},{new_password},{credentials[2]}\n"
        updated_login_file.append(new_credentials)
        with open("login.txt", "w") as f:
            f.writelines(updated_login_file)
    else:
        print("Invalid Input.")
        return
    updated_lines.append(new_line)
    with open("customer.txt", "w") as f:
        f.writelines(updated_lines)
    print("Update Completed")


# ----------------------------------------------Admin-----------------------------------------------------
def admin_register():
    # Select position to register
    while True:
        choices = int(input("Register for\n1. Receptionist\n2. Technician\n3. Admin\nPlease enter number: "))
        if 1 <= choices <= 3:
            break
        else:
            print("Position not found. Please select number 1-3")

    # Avoid duplicate username
    f = open("login.txt", "r")
    username_list = []
    for line in f:
        username_list.append(line.strip().split(",")[0])
    while True:
        username = input("Enter username: ").strip()
        if username in username_list:
            print("Username already exists. Please try again")
        else:
            break

    # Check if the password is valid
    password = password_validation(input("Enter password: ")).strip()

    # Add record
    f = open("login.txt", "a")
    match choices:
        case 1:
            f.write(f"{username},{password},receptionist\n")
            with open("receptionist.txt", "a") as f2:
                # Username|Password|Full Name|Contact Number|Email
                f2.write(f"{username},{password},-,-,-\n")
        case 2:
            f.write(f"{username},{password},technician\n")
            with open("technician.txt", "a") as f2:
                # Username|Password|Contact Number|Email
                f2.write(f"{username},{password},-,-\n")
        case 3:
            f.write(f"{username},{password},admin\n")
            with open("admin.txt", "a") as f2:
                # Username|Password|Full Name|Contact Number|Email
                f2.write(f"{username},{password},-,-,-\n")
        case _:
            print("Invalid input")
    print("Record Added")
    f.close()


def service_report():
    services, prices, date, status, payment = [], [], [], [], []
    total_income, unpaid = 0, 0
    with open("service.txt", "r") as f:
        for line in f:
            services.append(line.strip().split("|")[1])
            prices.append(line.strip().split("|")[3])
            date.append(line.strip().split("|")[5])
            status.append(line.strip().split("|")[6])
            payment.append(line.strip().split("|")[7])
    print("{:^130}".format("October Service Record"))
    print("-" * 130)
    print("{:^20}{:^50}{:^20}{:^20}{:^20}".format("No", "Services", "Prices (RM)", "Status", "Date"))
    print("-" * 130)
    for i in range(len(services)):
        print("{:^20}{:^50}{:^20}{:^20}{:^20}".format(i+1, services[i], prices[i], status[i], date[i]))
        if payment[i] == "Paid":
            total_income += int(prices[i])
        else:
            unpaid += int(prices[i])
    print("-" * 130)
    print()
    print("{:^130}".format("Analysis"))
    print("-" * 130)
    print("{:^80}{:^50}".format("Service Type", "Total"))
    print("-" * 130)

    service_map = {}
    for service in services:
        if service not in service_map:
            service_map[service] = 0
        service_map[service] += 1
    for service, count in service_map.items():
        print("{:^80}{:^50}".format(service, count))

    print("-" * 130)
    print("Total Services:", len(services))
    print(f"Total Income: RM {total_income} + RM {unpaid} (unpaid)")
    print()


def admin_update_profile(admin_name):
    updated_lines, admin_profile = [], []
    with open("admin.txt", "r") as f:
        for line in f:
            if line.startswith(admin_name):
                admin_profile = line.strip().split(",")
                continue
            updated_lines.append(line)

    print("Admin Profile\n-------------------")
    print(f"Username: {admin_profile[0]}\nFull Name: {admin_profile[2]}")
    print(f"Contact Number: {admin_profile[3]}\nEmail Address: {admin_profile[4]}")
    print("-------------------")

    choices = int(input("Update Password [1]| Personal Information [2]\nEnter the number of choice: "))
    match choices:
        case 1:
            password = input("Please enter your current password: ")
            if password == admin_profile[1]:
                while True:
                    pw = input("Enter New Password: ")
                    if pw == password:
                        print("New password cannot be same as old password")
                    else:
                        new_pw = password_validation(pw)
                        if new_pw == password:
                            print("New password cannot be same as old password")
                            continue
                        else:
                            break
                # add updated record in admin.txt
                new_line = f"{admin_profile[0]},{new_pw},{admin_profile[2]},{admin_profile[3]},{admin_profile[4]}\n"
                updated_lines.append(new_line)
                with open("admin.txt", "w") as f:
                    f.writelines(updated_lines)

                # add updated record in login,txt
                updated_login_file = []
                with open("login.txt", "r") as f:
                    for line in f:
                        if line.startswith(admin_name):
                            credentials = line.strip().split(",")
                            continue
                        updated_login_file.append(line)
                new_credentials = f"{credentials[0]},{new_pw},{credentials[2]}\n"
                updated_login_file.append(new_credentials)
                with open("login.txt", "w") as f:
                    f.writelines(updated_login_file)
                print("Password Updated Successfully")
            else:
                print("Incorrect Password")

        case 2:
            print("Please put '-' if you would like to leave the column empty")
            name = input("Enter your name: ")
            contact_num = input("Enter your contact number: ")
            email = input("Enter your email address: ")
            new_line = f"{admin_profile[0]},{admin_profile[1]},{name},{contact_num},{email}\n"
            updated_lines.append(new_line)
            with open("admin.txt", "w") as f:
                f.writelines(updated_lines)
            print("Profile Updated Successfully")

        case _:
            print("Invalid input. Please select number 1 or 2")


# ------------------------------------------Main Program----------------------------------------------------
while True:
    print("\n----------------------------------------")
    print("{:^40}".format("Welcome to Laptop Repair Service"))
    print("----------------------------------------\nPlease select your Position\n1. Receptionist\n2. Technician\n"
          "3. Customer\n4. Admin\n5. Exit Program")
    try:
        while True:
            position = int(input("Enter your position: "))
            match position:
                case 1:
                    position = "receptionist"
                case 2:
                    position = "technician"
                case 3:
                    position = "customer"
                case 4:
                    position = "admin"
                case 5:
                    print("Thank you.")
                    exit()
                case _:
                    print("Invalid input. Please select number 1-5")
                    continue
            break
    except ValueError:
        print("Integer input required.")
        continue
    print()

    login_successful, user_name, position = login(position)
    if login_successful:
        try:
            match position:

                case "receptionist":
                    print("{:^36}".format("RECEPTIONIST PAGE"))
                    while True:
                        print("-----------------------------------\nMENU\n1. Register new customer\n"
                              "2. Assign services to customer\n3. Accept payment from customer\n4. Update own profile\n"
                              "5. Log out")
                        choice = int(input("Enter your choice (number): "))
                        match choice:
                            case 1:
                                receptionist_register()
                            case 2:
                                assign_services()
                            case 3:
                                payment_receipt()
                            case 4:
                                receptionist_update_profile(user_name)
                            case 5:
                                break
                            case _:
                                print("Invalid input. Please select number 1-5")
                                continue

                case "technician":
                    print("{:^36}".format("TECHNICIAN PAGE"))
                    while True:
                        print("------------------------------------\nMENU\n1. View service requested by customers\n"
                              "2. Add description and laptop collection date\n3. Update own profile\n4. Log out")
                        choice = int(input("Enter your choice (number): "))
                        match choice:
                            case 1:
                                view_services()
                            case 2:
                                add_des_date()
                            case 3:
                                technician_update_profile(user_name)
                            case 4:
                                break
                            case _:
                                print("Invalid input. Please select number 1-4")
                                continue

                case "customer":
                    print("{:^36}".format("CUSTOMER PAGE"))
                    while True:
                        print("------------------------------------\nMENU\n1. Change requested service.\n"
                              "2. View service description, collection date and total amount\n"
                              "3. Update own profile\n4. Log out")
                        choice = int(input("Enter your choice (number): "))
                        match choice:
                            case 1:
                                change_requested_service(user_name)
                            case 2:
                                view_service_description(user_name)
                            case 3:
                                customer_update_profile(user_name)
                            case 4:
                                break
                            case _:
                                print("Invalid input. Please select number 1-4")
                                continue

                case "admin":
                    print("{:^36}".format("ADMIN PAGE"))
                    while True:
                        print("------------------------------------\nMENU\n"
                              "1. Register a new Receptionist / Technician / Admin.\n"
                              "2. View service report (monthly).\n3. Update own profile.\n4. Log out")
                        choice = int(input("Enter your choice (number): "))
                        match choice:
                            case 1:
                                admin_register()
                            case 2:
                                service_report()
                            case 3:
                                admin_update_profile(user_name)
                            case 4:
                                break
                            case _:
                                print("Invalid input. Please select number 1-4")
                                continue

        except ValueError:
            print("Integer input required.")
