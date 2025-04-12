#!/bin/python

# Copyright (c) 2024 Technicfan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#  _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
# |_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#   | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#   | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#   |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

# credits to https://github.com/Geremia/RichTextUnicode
# for idea and most of the convert function

import subprocess
from re import match, sub


def convert(string="placeholder", style=0, strike=False, underline=False):
    umlaut = "\u0308"

    font_styles = {
        # sans bold/italic/bold italic
        1: {"A": 0x1D5D4, "a": 0x1D5EE, "zero": 0x1D7EC},
        2: {"A": 0x1D608, "a": 0x1D622, "zero": "0"},
        3: {"A": 0x1D63C, "a": 0x1D656, "zero": "0"},
        # monospace
        4: {"A": 0x1D670, "a": 0x1D68A, "zero": "0"},
    }

    umlauts = {"Ä": "A", "Ö": "O", "Ü": "U", "ä": "a", "ö": "o", "ü": "u"}

    raw = style == 0
    if style in font_styles:
        A = font_styles[style]["A"]
        a = font_styles[style]["a"]
        zero = font_styles[style]["zero"]
    elif not raw:
        return string
    strike = strike and style in range(4)

    result = ""
    for c in string:
        if not raw:
            if c in umlauts:
                isumlaut = True
                c = umlauts[c]
            else:
                isumlaut = False
            if c >= "A" and c <= "Z":
                result += chr(A + ord(c) - ord("A"))
            elif c >= "a" and c <= "z":
                result += chr(a + ord(c) - ord("a"))
            elif c >= "0" and c <= "9":
                result += chr(zero + ord(c) - ord("0"))
            else:
                result += c
            if isumlaut:
                result += umlaut
        else:
            result += c
        if strike:
            result += "\u0336"
        if underline:
            result += "\u0332"

    return result


def main(string: str):
    results = []
    symbols = []
    skip = 0
    for i, c in enumerate(string):
        if skip == 0:
            if (
                i != 0
                and results[-1][0] == c
                and c in ["*", "_", "~", "`"]
                and len(results[-1]) < 3
            ):
                results[-1] += c
            elif c == "<" and (
                string[i : i + 3] == "<u>" or string[i : i + 4] == "</u>"
            ):
                if string[i + 1] == "/":
                    results.append("</u>")
                    skip = 3
                else:
                    results.append("<u>")
                    skip = 2
            else:
                results.append(c)
        else:
            skip -= 1
    for i, s in enumerate(results):
        if s[0] in ["*", "_", "~", "`"]:
            if s != "~":
                found = False
                for x, r in enumerate(reversed(symbols)):
                    if len(r) == 2 and r[0] == s:
                        found = True
                        symbols[-x - 1].append(i)
                        break
                if not found:
                    symbols.append([s, i])
        elif s == "<u>":
            symbols.append(["u", i])
        elif s == "</u>":
            for x, r in enumerate(reversed(symbols)):
                if len(r) == 2 and r[0] == "u":
                    symbols[-x - 1].append(i)

    for symbol in reversed(symbols):
        if len(symbol) == 3 or symbol[0] == "u":
            results[symbol[1]] = ""
            if len(symbol) == 3:
                results[symbol[2]] = ""

            if match("([*]|_)+", symbol[0]):
                if len(symbol[0]) == 3:
                    style = 3
                else:
                    if len(symbol[0]) == 2:
                        style = 1
                    else:
                        style = 2
                    for x in symbols:
                        if (
                            len(x) == 3
                            and x[0] in ["*" * style, "_" * style]
                            and x[1] < symbol[1]
                            and x[2] > symbol[2]
                        ):
                            style = 3
                            break
                for i in range(symbol[1] + 1, symbol[2]):
                    results[i] = convert(results[i], style)
            else:
                match symbol[0]:
                    case "~~":
                        for i in range(symbol[1] + 1, symbol[2]):
                            results[i] = convert(results[i], 0, True)
                    case "u":
                        if len(symbol) == 2:
                            end = len(results)
                        else:
                            end = symbol[2]
                        for i in range(symbol[1] + 1, end):
                            results[i] = convert(results[i], 0, False, True)
                    case "`" | "``" | "```":
                        for i in range(symbol[1] + 1, symbol[2]):
                            results[i] = convert(results[i], 4)

    result = "".join(results).splitlines()
    for i, s in enumerate(result):
        result[i] = sub("^- ", " •  ", s)

    return "\n".join(result)


text = subprocess.getoutput("xclip -o")

subprocess.call(f"clipcatctl insert -- '{main(text)}'", shell=True)
