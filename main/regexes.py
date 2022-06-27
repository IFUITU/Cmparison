from re import findall, sub

def regex_of_measure(value):
    """"RETURN regex of value check with text!"""
    # return search(f"\d+\{text}\/*\d+[A-zА-я]|\d+\.*\d+\{text}|\d+\s+\{text}|\d+\{text}|\d+\.\d+\s+\{text}|\d+\,\d+\{text}|\d+\,\d+\s+\{text}", value)
    return findall(f"\d+[A-zА-я]|\d+%|\№*\s+\d+|\№*\d+|\d+\s+[A-zА-я]|\d+\.*\d+[A-zА-я]|\d+\.\d+\s+[A-zА-я]|\d+\,\d+[A-zА-я]|\d+\,\d+\s+[A-zА-я]|\d+[A-zА-я]", value)

def digit_regex(text):
    return findall("\d+\,*\d+|\d+\.*\d+|\d+", sub(r"(?<=\d)\s+",'',text))
