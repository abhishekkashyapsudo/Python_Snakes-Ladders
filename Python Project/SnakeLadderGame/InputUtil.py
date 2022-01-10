
def read_string(prompt):
    inp = input(prompt).strip()

    # the length of the string must greater than 0
    if len(inp) > 0:
        return inp
    print("Invalid input...!!! The string must be non-empty")
    return read_string(prompt)
