import string
from unidecode import unidecode

def title_variants(title):
    title = title.strip().lower()
    variants = [title]
    variants += _asciifold(title)
    variants += [x[4:] for x in variants if x.startswith("the ")]
    variants += [x for x in [_ampersander(t) for t in variants] if x is not None]
    return list(set(variants))

def _asciifold(val):
    try:
        asciititle = unidecode(val)
    except:
        asciititle = val

    throwlist = string.punctuation + '\n\t'
    unpunctitle = "".join(c for c in val if c not in throwlist).strip()
    asciiunpunctitle = "".join(c for c in asciititle if c not in throwlist).strip()

    return [unpunctitle, asciititle, asciiunpunctitle]


def _ampersander(val):
    if " & " in val:
        return val.replace(" & ", " and ")
    if " and " in val:
        return val.replace(" and ", " & ")
    return None