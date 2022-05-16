from re import search

def regex_of_measure(text, value):
    """"RETURN regex of value check with text!"""
    return search(f"\d+\{text}\/\d+[A-zА-я]|\d+\{text}|\d+\s+\{text}|\d+\.*\d+\{text}|\d+\.\d+\s+\{text}|\d+\,\d+\{text}|\d+\,\d+\s+\{text}", value)

def digit_regex(text):
    return search("\d+\,*\d+|\d+\.*\d+|\d+", text)
