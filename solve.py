import logging


def clean(input_str):
    return input_str.strip(" \n")


BOARD = clean("""
XDOFZBNTBEMKJYUDFXLTBQGCACZGCB
OFJFMNHJLJJOYZDMPIRYTNHIWNUBCS
ZMALHIGZZWIMUZONCBXUITGSDYYVBN
NKOIRLDFHACJXHJUALPCWIVUNXBOBO
KSZTQUULLETOHTHZXCNNTLGMIYKGAC
NDEZWSLNZCGNXBPBZAXYRNKFOQWZIM
EERPXLJFDPPQUIPIDDJNSQWGITEFXW
NKMGOPIPTFDPVSWVWMFICR8OHVMRWO
IPFMBEABFRDYEAMBXCYWWBOUAANMLO
TMMKPRCFCOQYJKEJMLKBPVGNIPJFGT
FCVWTOZIIXGVGBCNMYGCJIKUWCLENW
CMXYYIMDVCUUMNNRUFIBJYBSHRKAOU
NLDTDPWEGRITLWIOIEGUNEZSPHOVKF
DMIGQCBKNWEVDJGCIHKTWOEDKQHXLW
RVIQLTGNUFXSCWVPSTPXKMHTXWSMCL
XNITWRIWMCKVOLWOGZCGAEDBMKZJEQ
OBQCZODAEEZPIJXPUHCGXGQDXFIVXI
TGRETVZQONBBHIXENNBOZMCXWLXUKF
MOTIRWALJFJVWTXEFYXPICTUREQXDB
IOARASZHLAFVVDEINRWQWEZRTNGJLO
IULDVZUYJIWGWTHOQKFYBUORWUPRUN
EHHBEWMHUTTPOGZIPXZLCDSQXOKDUD
ILRHLSCMPTHIASZVESOICXWOYYRPEJ
FUJSMDAVFJYADHTRIBPSDXIGZSEJYZ
CUMLWMUNWSNFEAJTUUKUPZMFQJXYZW
SRRQPCPKOJJNMJOUDVUKWIMPJBWYRG
ERPGCLDQEPTNNVNICJGEXFIBDWUEGL
SXDZYWIAYRWZPKUZOYFAWZNLKSTOHP
OYTOAMQXGKGVGEWSXUOFUAGLCPLBYM
ZYBBPNFDFKTFXOUYLBCUXAMDQQIPNR
""")

WORDS = clean("""
BIRTHDAY
GAMES
MUSIC
POPCORN
THIRTEEN
CANDY
HOTEL
PARTY
SERVICE
TRAVEL
DANCING
MITZVAH
PICTURE
SWIMMING
""")

DIRECTIONS = [
    (0, 1, 'down'),
    (0, -1, 'up'),
    (1, 0 , 'right'),
    (-1, 0, 'left'),
    (1, 1, 'down and right'),
    (1, -1, 'up and right'),
    (-1, 1, 'down and left'),
    (-1, -1, 'up and left'),
]


class SearchException(Exception):
    pass


def word_exists_at(word, x, y, direction, rows, all_indexes):
    x_delta, y_delta, label = direction
    if len(word) == 0:
        return True

    if x >= len(rows[0]) or x < 0:
        return False

    if y >= len(rows) or y < 0:
        return False

    current_char = rows[y][x]
    if current_char != word[0]:
        return False

    next_x = x + x_delta
    next_y = y + y_delta
    word = word[1:]  # Trim first letter.
    all_indexes.append((x, y))

    return word_exists_at(word, next_x, next_y, direction, rows, all_indexes)


def find_word(word, rows):
    for y in range(0, len(rows)):
        for x in range(0, len(rows[0])):
            for direction in DIRECTIONS:
                all_indexes = []
                if word_exists_at(word, x, y, direction, rows, all_indexes):
                    return x, y, direction, all_indexes

    raise SearchException('Word {} could not be found!'.format(word))


def cell_key(cell):
    return '{}x{}'.format(cell[0], cell[1])


def format_html(rows, results):
    html_rows = ''
    cells_to_bold = {}
    for word, metadata in results.iteritems():
        indexes = metadata[3]  # all_indexes
        for index in indexes:
            cells_to_bold[cell_key(index)] = True

    for y in range(0, len(rows)):
        html_rows += '<tr>'
        for x in range(0, len(rows[0])):
            html_rows += '<td>'
            if cell_key((x, y)) in cells_to_bold:
                html_rows += '<strong>{}</strong>'.format(rows[y][x])
            else:
                html_rows += rows[y][x]
            html_rows += '</td>'

        html_rows += '</tr>'
            
    return """
    <html>
        <head>
        <style>
        strong {
            color: red;
        }
        th, td {
            width: 18px;
            height: 18px;
            text-align: center;
        }
        </style>
        </head>
        <body>
            <table>
    """ + html_rows + """
            </table>
        </body>
    </html>

    """

def main():
    rows = BOARD.split("\n")
    words = WORDS.split("\n")
    results = {}

    # Find all words.
    for word in words:
        try:
            x, y, direction, all_indexes = find_word(word=word, rows=rows)
            results[word] = (x, y, direction[2], all_indexes)
        except SearchException as e:
            logging.warn(e)

    # Make pretty results
    print format_html(rows, results)


if __name__ == '__main__':
    main()
