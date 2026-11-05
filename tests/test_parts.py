from backend.database.parts import get_part, add_part
from backend.database.parts import get_all_parts
from backend.models.part import Part

#def main():
    # Getting part from DB
#    part = get_part(1)

#    if part:
#        print(f"Part ID: {part.part_id}")
#        print(f"Name: {part.name}")
#        print(f"Price: ${part.price}")
#    else:
#        print("Part not found")

    # Adding a part then creating part object
    #new_id = add_part("Air Filter","Engine air filter",19.99,"Filters") Commented out to prevent duplicate inserts everytime it is ran

    #print(f"New Part ID: {new_id}")

    #part = get_part(new_id)
    #print(f"New Part: {part.name}, ${part.price}")


def test_get_all_parts():
    parts = get_all_parts()

    assert len(parts) > 0, "No parts were returned"

    for part in parts:
        assert isinstance(part, Part)
        print(f"ID: {part.part_id}, Name: {part.name}, Price: ${part.price:.2f}")

def test_part_to_dict():
    parts = get_all_parts()

    part_dict = parts[0].to_dict()

    assert isinstance(part_dict, dict)
    assert "part_id" in part_dict
    assert "name" in part_dict
    assert "price" in part_dict

    print(part_dict)

if __name__ == "__main__":
    test_get_all_parts()
    test_part_to_dict()