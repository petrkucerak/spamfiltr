import re
from utils import read_classification_from_file
from io import StringIO
from html.parser import HTMLParser

# I've used the porter_stemmer method from the nltk library
#   (I've only copied the necessary files to run this method and am not using anything else from nltk)
try:
    from word_stemmer import stem_list_of_words
    stemmer_imported = True
except:
    stemmer_imported = False


class MLStripper(HTMLParser):
    # TODO: check where I got this
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class WordNormalizer:

    def load_stopwords(self):
        try:
            with open('stop_words.txt', 'r') as f:
                self.stopwords = f.read().splitlines()
            self.stopwords_loaded = True
            #print('loaded stopwords: ', self.stopwords)
        except:
            self.stopwords_loaded = False

    def load_patterns(self):
        self.patterns = []

        mail_pat = re.compile(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
        self.patterns.append((mail_pat, 'standardEmailAddress'))

        phone_pat = re.compile(
            r"[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}", re.IGNORECASE)
        self.patterns.append((phone_pat, 'standardPhoneNumber'))

        url_pat = re.compile(
            r'(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)', re.IGNORECASE)
        self.patterns.append((url_pat, 'standardUrlString'))

        ip_pat = re.compile(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        self.patterns.append((ip_pat, 'standardIpAddress'))
        # TODO: price pattern
        # TODO: time pattern
        # TODO: date pattern
        #print('loaded patterns: ', self.patterns)

    def __init__(self):

        self.load_stopwords()
        self.load_patterns()

        self.html_tag_regex = re.compile('<.*?>')

    def remove_html_tags(self, input_text):
        cleantext = re.sub(self.html_tag_regex, '', input_text)
        print("in: ", input_text)
        print("\n\n\n\nout: ", cleantext)
        return cleantext

    def normalize_words(self, words):
        new_words = []
        found = False
        for word in words:
            found = False
            for pattern in self.patterns:
                if pattern[0].match(word):
                    new_words.append(pattern[1])
                    found = True
                    break
            if not found:
                new_words.append(word)
        return new_words

    def normalize(self, text):
        text = text.lower()
        clean_text = strip_tags(text)

        # TODO: decide if we want to keep this since it more than doubles the time of this mehtond
        words = stem_list_of_words.stem_words(clean_text.split())

        if self.stopwords_loaded:
            words = [x for x in words if x not in self.stopwords]
        words = self.normalize_words(words)

        return words


if __name__ == "__main__":
    wn = WordNormalizer()
    str_w_html = """<html>
    <body>
    <center>
    <b><font color = "red" size = "+2.5">COST EFFECTIVE Direct Email Advertising</font><br>
    <font color = "blue" size = "+2">Promote Your Business For As Low As </font><br>
    <font color = "red" size = "+2">$50</font> <font color = "blue" size = "+2">Per 
    <font color = "red" size = "+2">1 Million</font>
    <font color = "blue" size = "+2"> Email Addresses</font></font><p>
    <b><font color = "#44C300" size ="+2">MAXIMIZE YOUR MARKETING DOLLARS!<p></FONT></b>
    <font size = "+2">Complete and fax this information form to 309-407-7378.<Br>
    A Consultant will contact you to discuss your marketing needs.<br>
    </font></font>
    <Table><tr><td>
    <font size = "+1"><b>NAME:___________________________________________________________________<br>
    <font size = "+1"><b>COMPANY:_______________________________________________________________<br>
    <font size = "+1"><b>ADDRESS:________________________________________________________________<br>
    <font size = "+1"><b>CITY:_____________________________________________________________________<br>
    <font size = "+1"><b>STATE:___________________________________________________________________<br>
    <font size = "+1"><b>PHONE:___________________________________________________________________<br>
    <font size = "+1"><b>E-MAIL:__________________________________________________________________<br>
    <font size = "+1"><b>WEBSITE: <font size = "-1" color = "red">(Not Required)</font>_______________________________________________________<br>
    ___________________________________________________________________________<br>
    ___________________________________________________________________________<br>
    <b><font color = "red">*</font>COMMENTS: <font color = "Red" size = "-1">(Provide details, pricing, etc. on the products and services you wish to market)</font><br>
    ___________________________________________________________________________<br>
    ___________________________________________________________________________<br>
    ___________________________________________________________________________<br>
    ___________________________________________________________________________<br>
    </td></tr>
    </table>
    </center>
    </body>
    </html>
    """
    print(wn.remove_html_tags(str_w_html))
