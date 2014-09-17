import string

def preprocess(text):
    #text can be a big or small string
    st = ''
    for letter in text:
        if letter in string.whitespace[:-1]:
            st += ' '
        elif letter in '.,?!/\\()[]{}':
            st += ' '+letter+' '
        elif letter in '~`-*()[]{}<>)""\':; ':
            st += ' '
        else:
            st += letter
    return st + ' \n'
