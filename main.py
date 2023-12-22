from googletrans import Translator
import spacy

# abbotts heuristics enum



def translate_text(text, source_lang='el', target_lang='en'):
    translator = Translator()
    translation = translator.translate(text, src=source_lang, dest=target_lang)
    return translation.text

def load_scenario():
    pass



text_el = """O Γιάννης οδηγώντας το περιπολικό του παρατηρεί να βγαίνει καπνός από μία αποθήκη. 
Η συνοδηγός του Μαρία αναφέρει το θέμα από τον ασύρματό της.​
Η Μαρία εισάγει τη διεύθυνση του κτηρίου στον  υπολογιστή παλάμης της, 
μία σύντομη περιγραφή της τοποθεσίας (π.χ. απέναντι από το πάρκο) και ένα επίπεδο συναγερμού.
Επιβεβαιώνει τα στοιχεία και περιμένει την επιβεβαίωση.​
Ο Πέτρος ειδοποιείται για το περιστατικό μέσω ηχητικού σήματος από τον υπολογιστή του. 
Εξετάζει τις πληροφορίες που δόθηκαν από τη Μαρία και επιβεβαιώνει τη λήψη της αναφοράς. 
Στέλνει ένα πυροσβεστικό όχημα και αποστέλλει τον εκτιμώμενο χρόνο άφιξης (ΕΧΑ) στη Μαρία.​
Η Μαρία λαμβάνει την επιβεβαίωση και τον ΕΧΑ.​"""

text_en = translate_text(text_el)

nlp = spacy.load("en_core_web_sm")

doc = nlp(text_en)
for token in doc:
    if token.pos_ == 'PROPN':
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)