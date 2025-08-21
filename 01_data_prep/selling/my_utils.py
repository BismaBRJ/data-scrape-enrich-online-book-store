import re

match_digit_re = re.compile(r"[0-9]")
match_digits_re = re.compile(r"[0-9]*") # just in case?

def get_digits_int_from_str(old_str):
    new_list = [
        ch
        for ch in old_str
        if re.match(match_digit_re, ch)
    ]
    new_str = "".join(new_list)
    new_int = int(new_str)
    return new_int

price_int_from_str = get_digits_int_from_str
