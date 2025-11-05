import re, ctypes, sys

def to_snake_case(name: str) -> str:
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake

def to_pascal_case(name: str) -> str:
    return ''.join(word.capitalize() for word in name.split('_'))

def table_to_class_name(table_name: str) -> str:
    parts = table_name.split('_')
    parts[-1] = singularize(parts[-1])
    return ''.join(word.capitalize() for word in parts)

def class_to_table_name(class_name: str) -> str:
    snake = to_snake_case(class_name)
    parts = snake.split('_')
    parts[-1] = pluralize(parts[-1])
    return "_".join(parts)

def pluralize(word: str) -> str:
    irregulars = {
        "person": "people",
        "child": "children",
        "man": "men",
        "woman": "women",
        "mouse": "mice",
        "goose": "geese",
    }

    lower = word.lower()
    if lower in irregulars:
        return irregulars[lower]

    if re.search(r'[sxz]$', lower) or re.search(r'(sh|ch)$', lower):
        return lower + "es"
    elif re.search(r'[^aeiou]y$', lower):
        return lower[:-1] + "ies"
    else:
        return lower + "s"

def singularize(word: str) -> str:
    irregulars = {
        "people": "person",
        "children": "child",
        "men": "man",
        "women": "woman",
        "mice": "mouse",
        "geese": "goose",
    }

    lower = word.lower()
    if lower in irregulars:
        return irregulars[lower]

    if lower.endswith("ies") and len(lower) > 3:
        return lower[:-3] + "y"
    elif lower.endswith("es") and (lower[-3:-2] in "sxz" or lower[-4:-2] in ["sh", "ch"]):
        return lower[:-2]
    elif lower.endswith("s") and len(lower) > 1:
        return lower[:-1]
    return lower

def trigger_hosts_file_sync():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable, # main.exe
            f'"{sys.argv[0]}" --sync-hosts', # Tham số
            None,
            1
        )
    except Exception as e:
        print(f"Lỗi khi gọi UAC: {e}")