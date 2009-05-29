from symbol_generation import generateSymbols, generateIdentifiers

symbols = generateSymbols()
identifiers = generateIdentifiers()

test_frame1_data = [symbols[0],symbols[1]]
test_frame1 = [identifiers[0],symbols[0],symbols[1]]

test_sequence1 = [
    identifiers[0],
    symbols[10],
    symbols[0],
    symbols[8],
    identifiers[0],
    symbols[11],
    symbols[1],
    symbols[27],
    identifiers[0],
    symbols[12],
    symbols[0],
    symbols[15],
    identifiers[0],
    symbols[13],
    symbols[10],
    identifiers[0],
    ]


test_sequence2 = [
    symbols[10],
    symbols[0],
    symbols[8],
    ]


test_sequence3 = [
    symbols[3],
    symbols[0],
    symbols[10],
    symbols[0],
    ]
