

class BinaryConfusionMatrix():

    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def as_dict(self):
        """Return the conf. mat. as a dictionary."""
        return {'tp': self.tp, 'tn': self.tn, 'fp': self.fp, 'fn': self.fn}

    def check_value_of(self, value):
        """Raise ValueError if var does not contain either positive or negative tag."""
        if value not in (self.pos_tag, self.neg_tag):
            print(value, self.pos_tag, self.neg_tag)
            raise ValueError('The arguments may be either %s or %s.'
                             % (self.pos_tag, self.neg_tag))

    def update(self, truth, prediction):
        """Compare the truth with the prediction and increment the related counter."""
        self.check_value_of(truth)
        self.check_value_of(prediction)
        if prediction == self.pos_tag:
            if truth == prediction:
                self.tp += 1
            else:
                self.fp += 1
        elif prediction == self.neg_tag:
            if truth == prediction:
                self.tn += 1
            else:
                self.fn += 1

    def compute_from_dicts(self, truth_dict, pred_dict):
        """Update the matrix using the corresponding values from both dictionaries.
        It is assumed that both dicts have the same keys.
        """
        for key in truth_dict:
            self.update(truth_dict[key], pred_dict[key])
