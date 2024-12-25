import re


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/([^/]+)/", session_str)
    if match:
        return match.group(1)  # Extract the captured session ID
    return ""  # Return an empty string if no match is found


def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])


if __name__ == "__main__":
    print(get_str_from_food_dict({"samosa": 2, "chhole": 5}))
    # print(extract_session_id("projects/garud-anod/agent/sessions/1234/contexts/ongoing-order"))

