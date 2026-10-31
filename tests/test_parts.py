from backend.database.parts import get_part

def main():
    part = get_part(1)

    if part:
        print(f"Part ID: {part.part_id}")
        print(f"Name: {part.name}")
        print(f"Price: ${part.price}")
    else:
        print("Part not found")


if __name__ == "__main__":
    main()
