'''
StackOverflow: https://stackoverflow.com/questions/2288953/separate-word-lists-for-nouns-verbs-adjectives-etc

Wordnet Dictionary: https://wordnet.princeton.edu/download/current-version

egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adj | cut -d ' ' -f 5 > conv.data.adj
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adv | cut -d ' ' -f 5 > conv.data.adv
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.noun | cut -d ' ' -f 5 > conv.data.noun
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.verb | cut -d ' ' -f 5 > conv.data.verb
'''