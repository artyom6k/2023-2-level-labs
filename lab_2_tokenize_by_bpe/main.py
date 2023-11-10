"""
Lab 2
BPE and machine translation evaluation
"""


def prepare_word(
        raw_word: str, start_of_word: str | None, end_of_word: str | None
) -> tuple[str, ...] | None:
    """
    Tokenizes word into unigrams and appends end-of-word token
    :param raw_word: original word
    :param start_of_word: a token that signifies the start of word
    :param end_of_word: a token that signifies the end of word
    :return: preprocessed word
    """
    if (not isinstance(raw_word, str)
            or (start_of_word is not None
                and not isinstance(start_of_word, str))
            or (end_of_word is not None
                and not isinstance(end_of_word, str))
    ):
        return None

    word_list = list(raw_word)

    if end_of_word:
        word_list.append(end_of_word)
    if start_of_word:
        word_list.insert(0, start_of_word)
    return tuple(word_list)


def collect_frequencies(
        text: str, start_of_word: str | None, end_of_word: str
) -> dict[tuple[str, ...], int] | None:
    """
    Counts number of occurrences of each word
    :param text: original text with no preprocessing
    :param start_of_word: a token that signifies the start of word
    :param end_of_word: a token that signifies the end of word
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if not (isinstance(text, str)
            and isinstance(end_of_word, str)) or not (
            isinstance(start_of_word, str) or start_of_word is None
    ):
        return None

    frequencies = {}
    words = text.split()

    for word in words:
        prepared_word = prepare_word(word, start_of_word, end_of_word)
        if prepared_word is None:
            return None
        if prepared_word not in frequencies:
            frequencies[prepared_word] = 0
        frequencies[prepared_word] += 1
    return frequencies


def count_tokens_pairs(
        word_frequencies: dict[tuple[str, ...], int]
) -> dict[tuple[str, str], int] | None:
    """
    Counts number of occurrences of each pair of subsequent tokens
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :return: dictionary in the form of <token pair: number of occurrences>
    """
    if not isinstance(word_frequencies, dict):
        return None

    token_pairs = {}
    for word, count in word_frequencies.items():
        tokens = list(word)
        for i in range(len(tokens) - 1):
            token_pair = (tokens[i], tokens[i + 1])
            if token_pair not in token_pairs:
                token_pairs[token_pair] = count
            else:
                token_pairs[token_pair] += count
    return token_pairs


def merge_tokens(
        word_frequencies: dict[tuple[str, ...], int], pair: tuple[str, str]
) -> dict[tuple[str, ...], int] | None:
    """
    Updates word frequency dictionary by replacing a pair of token with a merged one
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :param pair: a pair of tokens to be merged
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if not isinstance(word_frequencies, dict) or not isinstance(pair, tuple):
        return None

    new_word_frequencies = {}

    for key, value in word_frequencies.items():
        new_key = tuple(new_word_frequencies.replace(pair[0], pair[1]))
        for word in key:
            value = new_word_frequencies[new_key]

    return new_word_frequencies


def train(
        word_frequencies: dict[tuple[str, ...], int] | None, num_merges: int
) -> dict[tuple[str, ...], int] | None:
    """
    Creates required number of new tokens by merging existing ones
    :param word_frequencies: dictionary of a kind <preprocessed word: number of occurrences>
    :param num_merges: required number of new tokens
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if not isinstance(word_frequencies, dict) or not isinstance(num_merges, int):
        return None

    if word_frequencies is None:
        return None

    merge_token = 0
    while merge_token < num_merges:
        max_frequency = -1
        max_token_pair = None
        for token_pair, frequency in word_frequencies.items():
            if frequency > max_frequency or (frequency == max_frequency
                                             and len(token_pair) > len(max_token_pair)):
                max_frequency = frequency
                max_token_pair = token_pair

        if max_token_pair is None:
            break

        new_token = merge_tokens(max_token_pair[0], max_token_pair[1])
        word_frequencies[new_token] = max_frequency

        del word_frequencies[max_token_pair[0]]
        del word_frequencies[max_token_pair[1]]

        merge_token += 1

    return word_frequencies
def get_vocabulary(
        word_frequencies: dict[tuple[str, ...], int], unknown_token: str
) -> dict[str, int] | None:
    """
    Establishes correspondence between tokens and its integer identifier
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :param unknown_token: a token to signify an unknown token
    :return: dictionary in the form of <token: identifier>
    """
    if not isinstance(word_frequencies, dict) or not isinstance(unknown_token, str):
        return None

    tokens = []
    for word in word_frequencies.keys():
        tokens.extend(word)
    tokens = list(set(tokens))

    tokens.sort(key=lambda x: (-len(x), x))

    if len(tokens)>1:
        tokens.append('<START>')
        tokens.append('<END>')

    vocabulary = {token: i for i, token in enumerate(tokens)}


    return vocabulary
def decode(
        encoded_text: list[int] | None, vocabulary: dict[str, int] | None,
        end_of_word_token: str | None
) -> str | None:
    """
    Translates encoded sequence into decoded one
    :param encoded_text: a sequence of token identifiers
    :param vocabulary: dictionary in the form of <token: identifier>
    :param end_of_word_token: an end-of-word token
    :return: decoded sequence
    """
    if not isinstance(encoded_text, list) or not isinstance(vocabulary, dict) or not(
    isinstance(end_of_word_token, (str, type(None)))):
        return None

    decoded_text = ''
    for token_id in encoded_text:
        if token_id in vocabulary:
            token = vocabulary[token_id]
            if token == end_of_word_token:
                break
            decoded_text += token + ' '
        else:
            decoded_text += '<unk>'

        decoded_text = decoded_text.strip()

        return decoded_text
def tokenize_word(
        word: tuple[str, ...], vocabulary: dict[str, int], end_of_word: str | None,
        unknown_token: str
) -> list[int] | None:
    """
    Splits word into tokens
    :param word: preprocessed word
    :param vocabulary: dictionary in the form of <token: identifier>
    :param end_of_word: an end-of-word token
    :param unknown_token: token that signifies unknown sequence
    :return: list of token identifiers
    """


def load_vocabulary(vocab_path: str) -> dict[str, int] | None:
    """
    Reads and retrieves dictionary of type <token: identifier>
    :param vocab_path: path to the saved vocabulary
    :return: dictionary in the form of <token: identifier>
    """


def encode(
        original_text: str,
        vocabulary: dict[str, int] | None,
        start_of_word_token: str | None,
        end_of_word_token: str | None,
        unknown_token: str,
) -> list[int] | None:
    """
    Translates decoded sequence into encoded one
    :param original_text: original text
    :param vocabulary: dictionary in the form of <token: identifier>
    :param start_of_word_token: a start-of-word token
    :param end_of_word_token: an end-of-word token
    :param unknown_token: token that signifies unknown sequence
    :return: list of token identifiers
    """


def collect_ngrams(text: str, order: int) -> list[tuple[str, ...]] | None:
    """
    Extracts n-grams from the given sequence
    :param text: original text
    :param order: required number of elements in a single n-gram
    :return: sequence of n-grams
    """


def calculate_precision(
        actual: list[tuple[str, ...]], reference: list[tuple[str, ...]]
) -> float | None:
    """
    Compares two sequences by virtue of Precision metric
    :param actual: predicted sequence of n-grams
    :param reference: expected sequence of n-grams
    :return: value of Precision metric
    """


def geo_mean(precisions: list[float], max_order: int) -> float | None:
    """
    Computes geometric mean of sequence of values
    :param precisions: sequence of Precision values
    :param max_order: maximum length of n-gram considered
    :return: value of geometric mean of Precision metric
    """


def calculate_bleu(actual: str | None, reference: str, max_order: int = 3) -> float | None:
    """
    Compares two sequences by virtue of BLEU metric
    :param actual: predicted sequence
    :param reference: expected sequence
    :param max_order: max length of n-gram to consider for comparison
    :return: value of BLEU metric
    """
