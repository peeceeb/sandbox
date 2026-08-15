def isValid(s):
    # Maps every closing bracket
    # to its matching opening bracket.
    bracket_map = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    # Stack stores opening brackets.
    stack = []

    # Read one character at a time.
    for char in s:
        # Opening bracket?
        if char in "([{":
            # Remember it for later.
            stack.append(char)
        else:
            # Closing bracket without an opening bracket.
            if not stack:
                return False

            # Most recent opening bracket.
            top = stack.pop()

            # Does it match?
            if top != bracket_map[char]:
                return False

    # If anything remains,
    # some brackets weren't closed.
    return len(stack) == 0

print(isValid("({]})")) 