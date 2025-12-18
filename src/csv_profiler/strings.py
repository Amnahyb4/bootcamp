def slugify(text: str) -> str: ##slugify turns a normal text string into a URL / filename friendly format.
    t=text.strip().casefold()
    p=t.split()
    return"-".join(p)