# -*- coding: utf-8 -*-
import re
import sys

LATIN_TO_CYRILLIC = {
    'a': 'а',
    'b': 'б',
    'd': 'д',
    'e': 'е',
    'f': 'ф',
    'g': 'г',
    'sh':'ш',
    'ch': 'ч',
    'h': 'ҳ',
    'i': 'и',
    'j': 'ж',
    'k': 'к',
    'l': 'л', 
    'm': 'м', 
    'n': 'н',
    'o': 'о', 
    'p': 'п', 
    'q': 'қ', 
    'r': 'р', 
    's': 'с', 
    't': 'т', 
    'u': 'у', 
    'v': 'в', 
    'x': 'х', 
    'y': 'й', 
    'z': 'з', 
    'ʼ': 'ъ',
    # TODO: case?
}
LATIN_VOWELS = (
    'a', 'a'
)

# These words cannot be reliably converted to cyrillic because of the lossy
# nature of the to_latin converter.
TS_WORDS = {
    'aberra(ts)ion': 'аберрацион'
}

# These words cannot be reliably transliterated into cyrillic
E_WORDS = {
    'bel(e)taj': 'бельэтаж',
}
# Not to confuse with ш
SH_WORDS = {
    'a(sh)ob': 'асҳоб',
    'mu(sh)af': 'мусҳаф'
}
# Not to confuse with ё
YO_WORDS = {
    'general-ma(yo)r': 'генерал-майор',
    
}
YU_WORDS = {
    'mo(yu)pa': 'мойупа',

}
YA_WORDS = {
    'po(ya)bzal': 'пойабзал',
 
}
YE_WORDS = {
    'i(ye)': 'ийе',

}
SOFT_SIGN_WORDS = {
    'aviamodel': 'авиамодель',
}

CYRILLIC_TO_LATIN = {
    'а': 'a', 
    'б': 'b',
    'в': 'v', 
    'г': 'g', 
    'д': 'd',
    'е': 'e', 
    'ё': 'yo',
    'ж': 'j', 
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o', 
    'п': 'p', 
    'р': 'r', 
    'с': 's', 
    'т': 't', 
    'у': 'u', 
    'ф': 'f', 
    'х': 'x',
    'ц': 's', 
    'ч': 'ch',
    'ш': 'sh', 
    'ъ': 'ʼ', 
    'ь': '',
    'э': 'e', 
    'ю': 'yu', 
    'я': 'ya', 
    'ў': 'oʻ', 
    'қ': 'q', 
    'ғ': 'gʻ',
    'ҳ': 'h', 
    'ы':'i'
}
CYRILLIC_VOWELS = (
    '',
)


def to_cyrillic(text):
    """Transliterate latin text to cyrillic  using the following rules:
    1. ye = е in the beginning of a word or after a vowel
    2. e = э in the beginning of a word or after a vowel
    3. ц exception words
    4. э exception words
    """
    # These compounds must be converted before other letters
    compounds_first = {
        "nothing":"nothing"
    }
    compounds_second = {
        # different kinds of apostrophes
        'o‘': 'ў', 'O‘': 'Ў', 'oʻ': 'ў', 'Oʻ': 'Ў',
        'g‘': 'ғ', 'G‘': 'Ғ', 'gʻ': 'ғ', 'Gʻ': 'Ғ',
    }
    beginning_rules = {
        'e': 'е'
    }
    after_vowel_rules = {
        'e': 'е',
    }
    exception_words_rules = {
        's': 'с'
    }

    # standardize some characters
    # the first one is the windows string, the second one is the mac string
    text = text.replace('ʻ', '‘')

    def replace_soft_sign_words(m):
        word = m.group(1)
        if word.isupper():
            result = SOFT_SIGN_WORDS[word.lower()].upper()
        elif word[0].isupper():
            result = SOFT_SIGN_WORDS[word.lower()]
            result = result[0].upper() + result[1:]
        else:
            result = SOFT_SIGN_WORDS[word.lower()]
        return result

    for word in SOFT_SIGN_WORDS:
        text = re.sub(
            r'\b(%s)' % word,
            replace_soft_sign_words,
            text,
            flags=re.U
        )

    def replace_exception_words(m):
        """Replace ц (or э) only leaving other characters unchanged"""
        return '%s%s%s' % (
            m.group(1)[:m.start(2)],
            exception_words_rules[m.group(2)],
            m.group(1)[m.end(2):]
        )
    # loop because of python's limit of 100 named groups
    for word in list(TS_WORDS.keys()) + list(E_WORDS.keys()):
        text = re.sub(
            r'\b(%s)' % word,
            replace_exception_words,
            text,
            flags=re.U
        )

    # compounds
    text = re.sub(
        r'(%s)' % '|'.join(compounds_first.keys()),
        lambda x: compounds_first[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(compounds_second.keys()),
        lambda x: compounds_second[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(LATIN_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(LATIN_TO_CYRILLIC.keys()),
        lambda x: LATIN_TO_CYRILLIC[x.group(1)],
        text,
        flags=re.U
    )

    return text


def to_latin(text):
    """Transliterate cyrillic text to latin using the following rules:
    1. ц = s at the beginning of a word.
    ц = ts in the middle of a word after a vowel.
    ц = s in the middle of a word after consonant (DEFAULT in CYRILLIC_TO_LATIN)
        цирк = sirk
        цех = sex
        федерация = federatsiya
        функция = funksiya
    2. е = ye at the beginning of a word or after a vowel.
    е = e in the middle of a word after a consonant (DEFAULT).
    3. Сентябр = Sentabr, Октябр = Oktabr
    """
    beginning_rules = {
        'ц': 's', 'Ц': 'S',
        'е': 'e', 'Е': 'e'
    }
    after_vowel_rules = {
        'ц': 'ts', 'Ц': 'Ts',
        'е': 'e', 'е': 'e'
    }

    text = re.sub(
        r'(сент|окт)([яЯ])(бр)',
        lambda x: '%s%s%s' % (x.group(1),
                              'a' if x.group(2) == 'я' else 'A', x.group(3)),
        text,
        flags=re.IGNORECASE | re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(CYRILLIC_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(CYRILLIC_TO_LATIN.keys()),
        lambda x: CYRILLIC_TO_LATIN[x.group(1)],
        text,
        flags=re.U
    )

    return text


def transliterate(text, to_variant):
    if to_variant == 'cyrillic':
        text = to_cyrillic(text)
    elif to_variant == 'latin':
        text = to_latin(text)

    return text

if __name__ == "__main__":
    """cat input_in_lat.txt | python transliterate.py > output_in_cyr.txt"""
    for line in sys.stdin:
        sys.stdout.write(transliterate(line, 'cyrillic'))