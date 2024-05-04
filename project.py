data_file = "disk_usage_data.txt"

def load_disk_usage():
    data = {}
    try:
        with open(data_file, 'r') as file:
            for line in file:
                server_name, disk_path, total_space, used_space, free_space = line.strip().split(',')
                data[(server_name, disk_path)] = {
                    'total_space': int(total_space),
                    'used_space': int(used_space),
                    'free_space': int(free_space)
                }
    except FileNotFoundError:
        pass
    return data

def save_disk_usage(data):
    with open(data_file, 'w') as file:
        for (server_name, disk_path), usage_data in data.items():
            file.write(f"{server_name},{disk_path},{usage_data['total_space']},{usage_data['used_space']},{usage_data['free_space']}\n")

def insert_disk_usage(server_name, disk_path, total_space, used_space, free_space):
    data = load_disk_usage()
    data[(server_name, disk_path)] = {
        'total_space': total_space,
        'used_space': used_space,
        'free_space': free_space
    }
    save_disk_usage(data)

def get_disk_usage(server_name):
    data = load_disk_usage()
    return [value for key, value in data.items() if key[0] == server_name]

def update_disk_usage(server_name, disk_path, total_space, used_space):
    data = load_disk_usage()
    if (server_name, disk_path) in data:
        data[(server_name, disk_path)] = {
            'total_space': total_space,
            'used_space': used_space,
            'free_space': total_space-used_space
        }
        save_disk_usage(data)

def delete_disk_usage(server_name, disk_path):
    data = load_disk_usage()
    if (server_name, disk_path) in data:
        del data[(server_name, disk_path)]
        save_disk_usage(data)

def fetch_disk_usage(server_name, disk_path):
    total_space = int(input('Enter Total Space (in MB): '))
    used_space = int(input('Enter Used Space (in MB): '))
    free_space = total_space - used_space
    insert_disk_usage(server_name, disk_path, total_space, used_space, free_space)

def analyze_disk_space():
    data = load_disk_usage()
    print("Disk Space Usage Analysis:")
    print("{:<20} {:<20} {:<15} {:<15} {:<15}".format("Server Name", "Disk Path", "Total Space(MB)", "Used Space(MB)", "Free Space(MB)"))
    for (server_name, disk_path), usage_data in data.items():
        print("{:<20} {:<20} {:<15} {:<15} {:<15}".format(server_name, disk_path, usage_data['total_space'], usage_data['used_space'], usage_data['free_space']))


def suggest_cleanup_actions():
    data = load_disk_usage()
    print("Suggested Cleanup Actions:")
    for (server_name, disk_path), usage_data in data.items():
        if usage_data['used_space'] > usage_data['total_space'] * 0.8:
            print(f"Server: {server_name}, Disk Path: {disk_path} - Clean up unnecessary files.")


def menu():
    print("Disk Space Management Tool")

    while True:
        print("\n1. Add Disk Usage Data")
        print("2. View Disk Usage Data")
        print("3. Update Disk Usage Data")
        print("4. Delete Disk Usage Data")
        print("5. Analyze Disk Space Usage")
        print("6. Suggest Cleanup Actions")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            server_name = input("Enter server name: ")
            disk_path = input("Enter disk path: ")
            fetch_disk_usage(server_name, disk_path)
            print("Disk usage data added successfully!")

        elif choice == '2':
            server_name = input("Enter server name: ")
            print(get_disk_usage(server_name))

        elif choice == '3':
            server_name = input("Enter server name: ")
            disk_path = input("Enter disk path: ")
            total_space = int(input("Enter total space (in MB): "))
            used_space = int(input("Enter used space (in MB): "))
            update_disk_usage(server_name, disk_path, total_space, used_space)
            print("Disk usage data updated successfully!")

        elif choice == '4':
            server_name = input("Enter server name: ")
            disk_path = input("Enter disk path: ")
            delete_disk_usage(server_name, disk_path)
            print("Disk usage data deleted successfully!")

        elif choice == '5':
            analyze_disk_space()

        elif choice == '6':
            suggest_cleanup_actions()

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    menu()
