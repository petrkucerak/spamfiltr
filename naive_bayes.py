from premade_data_loader import LoadData
from decimal import Decimal
from premade_data_loader import LoadData

PADDING = 1


def get_propabilities():
    compiled_data = LoadData().load_known()['compiled_data']
    type_chance = {}
    for type in compiled_data['count_per_type']:
        type_chance[type] = Decimal(compiled_data['count_per_type'][type] /
                                    compiled_data['total_mails'])
    word_chance = {}
    unknown_word_chance = {}
    for type in compiled_data['bow']:
        unknown_word_chance[type] = Decimal(PADDING /
                                            compiled_data['n_of_words_per_type'][type]*10)
        word_chance[type] = {}
        for word in compiled_data['bow'][type]:
            word_chance[type][word] = Decimal((
                compiled_data['bow'][type][word]+PADDING) / compiled_data['n_of_words_per_type'][type]*10)

    return type_chance, word_chance, unknown_word_chance
