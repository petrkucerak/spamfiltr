from premade_data_loader import LoadData
from decimal import Decimal


PADDING = 1


def load_known():
    dl = LoadData()
    return dl.load_known('known.json')


def get_propabilities():
    compiled_data = load_known()['compiled_data']
    type_chance = {}
    for type in compiled_data['count_per_type']:
        type_chance[type] = Decimal(compiled_data['count_per_type'][type] /
                                    compiled_data['total_mails'])
    word_chance = {}
    unknown_word_chance = {}
    for type in compiled_data['bow']:
        unknown_word_chance[type] = Decimal(PADDING /
                                            compiled_data['word_count_per_type'][type]*10)
        word_chance[type] = {}
        for word in compiled_data['bow'][type]:
            word_chance[type][word] = Decimal((
                compiled_data['bow'][type][word]+PADDING) / compiled_data['word_count_per_type'][type]*10)
        # print(word_chance[type])
    return type_chance, word_chance, unknown_word_chance
