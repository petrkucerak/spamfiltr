class KnownMail:
    name = None
    subject = None
    subject_length = None
    n_of_repeat_char_words = None
    word_count = None
    sender = None
    reply_chain = None
    word_counter = None
    n_of_other_recipients = None
    n_of_mentioned_mails = None
    n_of_urls = None
    bow_score = None
    n_of_normal_number = None

    def __init__(self, name):
        self.name = name

    def get_training_data(self, params):
        training_data = []
        self_dict = self.__dict__
        for param in params:
            if param in self_dict and self_dict[param] != None:
                training_data.append(self_dict[param])
            else:
                raise ValueError(
                    f"Couldn't find valid param {param} in {self_dict}")
        return training_data


if __name__ == "__main__":
    km = KnownMail("Test_mail", subject="test subject",
                   n_of_repeat_char_words=12, word_count=156, sender="sender@sender.com", reply_chain=0, word_counter={'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6}, n_of_recipients=2)
    import json
    with open('new_data.json', 'w',  encoding='utf-8') as fp:
        json.dump(km.__dict__, fp, sort_keys=True, indent='\t')
