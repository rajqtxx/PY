import re

book_inventory = [
    ["001", "Python Programming", "G. Van Rossum", "IT", 4, 4],
    ["002", "Data Structures", "A. Aho", "CS", 3, 3]
]
borrow_records = []  # Stores: [user_id, user_name, user_role, acc_no, title, is_returned]

def is_valid_user_id(uid):
    """Validates User ID format: XX-XXXX-XXXXXX (e.g., 02-2425-003422)"""
    pattern = r"^\d{2}-\d{4}-\d{6}$"
    return bool(re.match(pattern, uid))

def is_acc_no_exists(acc_no):
    """Checks if Accession Number already exists in the inventory."""
    return any(book[0] == acc_no for book in book_inventory)

def get_yes_or_no(prompt_text):
    """Helper function to strictly require 'y' or 'n' input."""
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in ['y', 'n']:
            return choice
        print("[ERROR] Invalid input. Please enter 'y' for Yes or 'n' for No.")

def add_book(acc_no, title, author, category, qty):
    qty_num = int(qty)
    book_inventory.append([acc_no, title, author, category, qty_num, qty_num])
    print(f"[SUCCESS] Added to inventory: {title}\n")

def display_inventory():
    divider = "=" * 95
    sub_divider = "-" * 95
    
    print("\n" + divider)
    print(f"{'ACC NO':<10} | {'TITLE':<25} | {'AUTHOR':<20} | {'CATEGORY':<12} | {'QTY':<7} | {'AVAIL':<7}")
    print(sub_divider)
    for acc_no, title, author, cat, total_qty, avail_qty in book_inventory:
        print(f"{acc_no:<10} | {title:<25} | {author:<20} | {cat:<12} | {total_qty:<7} | {avail_qty:<7}")
    print(divider)

def display_user_active_borrows(user_id):
    """Displays books currently borrowed by a specific user that haven't been returned yet."""
    active_borrows = [rec for rec in borrow_records if rec[0] == user_id and not rec[5]]
    
    if not active_borrows:
        return []

    divider = "=" * 65
    sub_divider = "-" * 65
    print("\n" + divider)
    print(f"ACTIVE BORROWS FOR USER: {user_id}")
    print(sub_divider)
    print(f"{'ACC NO':<10} | {'TITLE':<30} | {'STATUS':<10}")
    print(sub_divider)
    for rec in active_borrows:
        print(f"{rec[3]:<10} | {rec[4]:<30} | Active")
    print(divider)
    
    return active_borrows

def borrow_single_book(user_id, user_name, user_role, acc_no):
    active_borrows = sum(1 for rec in borrow_records if rec[0] == user_id and not rec[5])
    max_allowed = 2 if user_role.lower() == "student" else 5

    if active_borrows >= max_allowed:
        print(f"[DENIED] Borrow limit ({max_allowed}) reached for {user_role}. Cannot borrow more items.")
        return False, True

    for book in book_inventory:
        if book[0] == acc_no:
            if book[5] > 0:
                book[5] -= 1
                borrow_records.append([user_id, user_name, user_role, acc_no, book[1], False])
                print(f"[SUCCESS] Borrowed: {book[1]}")
                return True, False
            else:
                print("[UNAVAILABLE] No copies remaining on shelf.")
                return False, False

    print("[ERROR] Book Accession Number not found in inventory.")
    return False, False

def return_single_book(user_id, acc_no):
    for record in borrow_records:
        rec_user, rec_name, rec_role, rec_acc, title, is_returned = record
        
        if rec_user == user_id and rec_acc == acc_no and not is_returned:
            for book in book_inventory:
                if book[0] == acc_no:
                    book[5] += 1
                    break

            record[5] = True
            print(f"[SUCCESS] Returned: {title}")
            return True

    print("[ERROR] No active borrow record found for this Accession Number under your User ID.")
    return False

def display_borrow_history():
    if not borrow_records:
        print("\n[INFO] No borrowing history available.")
        return

    divider = "=" * 105
    sub_divider = "-" * 105

    print("\n" + divider)
    print(f"{'USER ID':<16} | {'NAME':<18} | {'ROLE':<10} | {'ACC NO':<8} | {'TITLE':<25} | {'STATUS':<10}")
    print(sub_divider)
    for user_id, name, role, acc_no, title, is_returned in borrow_records:
        status = "Returned" if is_returned else "Active"
        print(f"{user_id:<16} | {name:<18} | {role:<10} | {acc_no:<8} | {title:<25} | {status:<10}")
    print(divider)

def main_menu():
    while True:
        print("\n=== CITE RESOURCE CENTER TRACKING SYSTEM ===")
        print("1. Display Inventory Catalog")
        print("2. Add Books/Resources (Bulk/Single)")
        print("3. Borrow Books/Resources (Bulk/Single)")
        print("4. Return Books/Resources (Bulk/Single)")
        print("5. Display Borrowing History")
        print("6. Exit System")
        
        while True:
            choice = input("\nSelect Option (1-6): ").strip()
            if choice in ["1", "2", "3", "4", "5", "6"]:
                break
            print("[ERROR] Invalid choice option. Please enter a valid number from 1 to 6.")

        if choice == "1":
            display_inventory()
            
        elif choice == "2":
            print("\n--- BATCH ADD MODE ---")
            books_added_count = 0
            
            while True:
                display_inventory()
                
                while True:
                    acc = input("\nEnter New Accession No: ").strip()
                    if not acc.isdigit():
                        print("[ERROR] Accession Number must contain digits only. Please try again.")
                        continue
                    if is_acc_no_exists(acc):
                        print("[ERROR] Accession Number already exists! Please enter a unique number.")
                        continue
                    break
                    
                title = input("Enter Title: ").strip()
                author = input("Enter Author/Publisher: ").strip()
                cat = input("Enter Category: ").strip()
                
                while True:
                    qty = input("Enter Quantity: ").strip()
                    if not qty.isdigit() or int(qty) <= 0:
                        print("[ERROR] Quantity must be a valid positive integer. Please try again.")
                        continue
                    break

                add_book(acc, title, author, cat, qty)
                books_added_count += 1
                
                again = get_yes_or_no("Do you want to add another item? (y/n): ")
                if again == 'n':
                    print(f"\n[SUMMARY] Batch import complete. Total items added: {books_added_count}")
                    break
                
        elif choice == "3":
            print("\n--- BORROW MODE ---")
            
            while True:
                uid = input("Enter User ID (e.g., 02-2425-003422): ").strip()
                if not is_valid_user_id(uid):
                    print("[ERROR] Invalid User ID format! Format must be XX-XXXX-XXXXXX. Try again.\n")
                    continue
                break

            uname = input("Enter User Name: ").strip()
            
            while True:
                role = input("Enter Role (Student/Faculty): ").strip()
                if role.lower() not in ["student", "faculty"]:
                    print("[ERROR] Invalid Role. Must be 'Student' or 'Faculty'. Try again.\n")
                    continue
                break

            max_allowed = 2 if role.lower() == "student" else 5
            active_borrows = sum(1 for rec in borrow_records if rec[0] == uid and not rec[5])
            remaining_limit = max_allowed - active_borrows

            print("\n" + "="*50)
            print(f" BORROWING LIMITATIONS & STATUS")
            print(f" Role: {role.capitalize()}")
            print(f" Max Allowed: {max_allowed} item(s)")
            print(f" Currently Borrowed: {active_borrows} item(s)")
            print(f" Available Allowance: {remaining_limit} item(s)")
            print("="*50)

            if remaining_limit <= 0:
                print(f"[DENIED] You have reached the maximum borrow limit ({max_allowed} items).")
                continue

            while True:
                num_to_borrow_input = input(f"\nHow many books would you like to borrow? (1-{remaining_limit}): ").strip()
                if not num_to_borrow_input.isdigit():
                    print("[ERROR] Please enter a valid number.")
                    continue
                
                num_to_borrow = int(num_to_borrow_input)
                if num_to_borrow <= 0:
                    print("[ERROR] Quantity must be at least 1.")
                    continue
                elif num_to_borrow > remaining_limit:
                    print(f"[ERROR] You cannot borrow {num_to_borrow} items. Your remaining limit is {remaining_limit}.")
                    continue
                break

            borrowed_count = 0
            for i in range(1, num_to_borrow + 1):
                while True:
                    display_inventory()
                    
                    acc = input(f"\nEnter Accession No. to borrow (Item {i} of {num_to_borrow}): ").strip()
                    if not acc.isdigit():
                        print("[ERROR] Accession Number must contain digits only. Try again.")
                        continue

                    success, limit_reached = borrow_single_book(uid, uname, role, acc)
                    if limit_reached:
                        break
                    if success:
                        borrowed_count += 1
                        break
                    else:
                        print("Please try entering a valid/available Accession Number again.")

            print(f"\n[SUMMARY] Borrow session ended. Total items borrowed: {borrowed_count}")

        elif choice == "4":
            print("\n--- RETURN MODE ---")
            while True:
                uid = input("Enter User ID (e.g., 02-2425-003422): ").strip()
                if not is_valid_user_id(uid):
                    print("[ERROR] Invalid User ID format! Format must be XX-XXXX-XXXXXX. Try again.\n")
                    continue
                break
            
            returned_count = 0
            while True:
                active_borrows = display_user_active_borrows(uid)
                
                if not active_borrows:
                    if returned_count == 0:
                        print("\n[INFO] You have no active borrowed items to return.")
                    else:
                        print("\n[INFO] All active borrowed items have been successfully returned.")
                    break

                while True:
                    acc = input("\nEnter Accession No to return: ").strip()
                    if not acc.isdigit():
                        print("[ERROR] Accession Number must contain digits only. Try again.")
                        continue

                    if return_single_book(uid, acc):
                        returned_count += 1
                        break
                    else:
                        print("Please enter a valid Accession Number from your active borrows above.")

                remaining_active = [rec for rec in borrow_records if rec[0] == uid and not rec[5]]
                if not remaining_active:
                    print("\n[INFO] All borrowed items for this user have been returned.")
                    break

                again = get_yes_or_no("\nDo you want to return another item? (y/n): ")
                if again == 'n':
                    break

            print(f"\n[SUMMARY] Return session ended. Total items returned: {returned_count}")

        elif choice == "5":
            display_borrow_history()
                
        elif choice == "6":
            print("\nExiting system. Program terminated.")
            break

if __name__ == "__main__":
    main_menu()