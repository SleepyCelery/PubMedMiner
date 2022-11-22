def string_search(target_string, seq):
    if isinstance(seq, list):
        for i in seq:
            try:
                if target_string in i:
                    return True
            except:
                continue
        return False
    elif isinstance(seq, str):
        if target_string in seq:
            return True
        else:
            return False


def strings_search(target_strings, seq):
    if isinstance(seq, list):
        for i in seq:
            for target_string in target_strings:
                try:
                    if target_string in i:
                        return True
                except:
                    continue
        return False
    if isinstance(seq, str):
        for target_string in target_strings:
            if target_string in seq:
                return True
        return False
