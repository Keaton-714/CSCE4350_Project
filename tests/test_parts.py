from backend.database.parts import get_part, add_part

def main():
    # Getting part from DB
    part = get_part(1)

    if part:
        print(f"Part ID: {part.part_id}")
        print(f"Name: {part.name}")
        print(f"Price: ${part.price}")
    else:
        print("Part not found")

    # Adding a part then creating part object
    new_id = add_part("Air Filter","Engine air filter",19.99,"Filters")

    print(f"New Part ID: {new_id}")

    part = get_part(new_id)
    print(f"New Part: {part.name}, ${part.price}")

if __name__ == "__main__":
    main()
