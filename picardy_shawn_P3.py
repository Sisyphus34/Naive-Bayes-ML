

def read_files():

    spam = 0
    ham = 0

    counted = {}

    training_input = input(
        "Please enter the name of the training set file including extension: \n")
    print("Training = ", training_input)
    training_file = open(training_input, 'r')
    textline = training_file.readline()
    while textline != "":
        is_spam = int(textline[:1])
        if is_spam == 1:
            spam += 1
        else:
            ham += 1
        textline = cleantext(textline[1:])
        words = textline.split()
        words = set(words)
        counted = countWords(words, is_spam, counted)
        textline = training_file.readline()
    print(counted)
    vocab = (make_percent_list(1, counted, spam, ham))
    print(vocab)
    training_file.close()

    stop_word_bank = input(
        "Please enter the name of the Stop Word list file including extensions: \n")
    print("Stop Words = ", stop_word_bank)


def cleantext(text):
    text = text.lower()
    text = text.strip()
    for letters in text:
        if letters in """[]!.,"-!-@;':#$%^&*()+/?""":
            text = text.replace(letters, " ")


def countWords(text, is_spam, counted):
    for each_word in counted:
        if each_word in counted:
            if is_spam == 1:
                counted[each_word][1] = counted[each_word][1] + 1
            else:
                counted[each_word][0] = counted[each_word][0] + 1
        else:
            if is_spam == 1:
                counted[each_word] = [0, 1]
            else:
                counted[each_word] = [1, 0]
    return counted


def make_percent_list(k, theCount, spams, hams):
    for each_key in theCount:
        theCount[each_key][0] = (theCount[each_key][0] + k)/(2*k+hams)
        theCount[each_key][1] = (theCount[each_key][1] + k)/(2*k+spams)
    return theCount

read_files()
