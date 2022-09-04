import itertools
import re
from typing import Sequence, Iterable

END = 3


def morse_or_text_to_bytes(text: str) -> Sequence[int]:
    if is_morse_code(text):
        text = text.strip()
    else:
        text = _from_text_to_morse(text)

    result = bytearray()

    bits_values = itertools.chain((_char_to_bits_map[c] for c in text), [0, END])
    iterator = iter(bits_values)
    byte = 0
    try:
        while True:
            a = next(iterator)
            byte |= a
            b = next(iterator)
            byte |= b << 2
            c = next(iterator)
            byte |= c << 4
            d = next(iterator)
            byte |= d << 6
            result.append(byte)
            byte = 0
    except StopIteration:
        if byte != 0:
            result.append(byte)

    return result


def bytes_to_morse_or_text(morse_bytes: Iterable[int], morse: bool = False) -> str:
    morse_values = ""
    for byte in morse_bytes:
        a = byte & 0b00000011
        if a == END:
            break
        morse_values += _bits_to_char_map[a]
        b = (byte & 0b00001100) >> 2
        if b == END:
            break
        morse_values += _bits_to_char_map[b]
        c = (byte & 0b00110000) >> 4
        if c == END:
            break
        morse_values += _bits_to_char_map[c]
        d = (byte & 0b11000000) >> 6
        if d == END:
            break
        morse_values += _bits_to_char_map[d]

    if morse:
        return morse_values

    result = ""
    # Because spaces can either be a split between morse values, it's easier to use a regex
    split_values = re.split(r'([.-]+)', morse_values)
    for value in split_values:
        if value == "":
            continue
        if value[0] == " ":
            assert value.isspace()
            result += " " * int(len(value) / 3)
        else:
            result += _morse_to_char_map[value]

    return result.strip()


def is_morse_code(text: str) -> bool:
    for char in text.strip():
        if char not in _char_to_morse_map.values():
            return False
    return True


def is_valid_morse_text(text: str) -> bool:
    distinct = set((c for c in text.strip().upper()))
    return any((c for c in distinct if c not in _char_to_morse_map.keys()))


def invalid_morse_chars(text: str) -> str:
    distinct = set((c for c in text.strip().upper()))
    return "".join((c for c in distinct if c not in _char_to_morse_map.keys()))


def _from_text_to_morse(text: str) -> str:
    return " ".join(_char_to_morse_map[c] for c in text.strip().upper())


_bits_to_char_map = [' ', '.', '-']
_char_to_bits_map = {v: i for i, v in enumerate(_bits_to_char_map)}
_char_to_morse_map = {
    'A': ".-", 'B': "-...", 'C': "-.-.", 'D': "-..", 'E': ".", 'F': "..-.", 'G': "--.", 'H': "....",
    'I': "..", 'J': ".---", 'K': "-.-", 'L': ".-..", 'M': "--", 'N': "-.", 'O': "---", 'P': ".--.",
    'Q': "--.-", 'R': ".-.", 'S': "...", 'T': "-", 'U': "..-", 'V': "...-", 'W': ".--", 'X': "-..-",
    'Y': "-.--", 'Z': "--..",

    '0': "-----", '1': ".----", '2': "..---", '3': "...--", '4': "....-",
    '5': ".....", '6': "-....", '7': "--...", '8': "---..", '9': "----.",

    'ä': ".-.-", 'á': ".--.-", 'å': ".--.-", 'é': "..-..", 'ñ': "--.--", 'ö': "---.", 'ü': "..--",

    '&': ".-...", '\'': ".----.", '@': ".--.-.", ')': "-.--.-", '(': "-.--.", ':': "---...",
    ',': "--..--", '=': "-...-", '!': "-.-.--", '.': ".-.-.-", '-': "-....-", '+': ".-.-.",
    '\"': ".-..-.", '?': "..--..", '/': "-..-.", ' ': ' '
}
_morse_to_char_map = {v: k for k, v in _char_to_morse_map.items()}
