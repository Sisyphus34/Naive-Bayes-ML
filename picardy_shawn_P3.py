import random
import math


def project_three():

    spam = 0
    ham = 0

    counted = {}

    training_input = input(
        "Please enter the name of the TRAINING set file including extension: \n")
    # print("Training = ", training_input)
    training_file = open(training_input, 'r')
    textline = training_file.readline()
    # print("textline = ", textline)
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
    # print(counted)
    vocab = (make_percent_list(1, counted, spam, ham))
    # print(vocab)

    # ham_sl_prob = 0
    # spam_sl_prob = 0
    
    # for key in vocab:
    #     if key in words:
    #         ham_sl_prob += math.log(vocab[key][1])
    #         spam_sl_prob += math.log(vocab[key][0])
    #     else:
    #         ham_sl_prob += math.log((1 - vocab[key][1]))
    #         spam_sl_prob += math.log((1 - vocab[key][0]))

    # print("words = ", words)
    # total_count += 1
    # subject_line = test_file.readline()
    # print(subject_count)
    ham_prob = ham/ (ham+spam)
    spam_prob = spam / (ham + spam)

    # print("hamProb = ", ham_prob, " spamProb = ", spam_prob, "\nhamSL = ", ham_sl_prob, " spamSL = ", spam_sl_prob)

    training_file.close()

    #################### Stop Word Parsing ####################
    stopwords = input(
        "Please enter the name of the STOPWORDS file including extension: \n")
    # print("Training = ", stopwords)
    stop_file = open(stopwords, 'r')
    stopword = stop_file.readline()
    # print("vocab length = ", len(vocab))
    # count = 0
    while stopword != "":
        if stopword in vocab:
            # print("stopword = ", stopword)
            # print("dict[stopword] = ", vocab[stopword])
            del vocab[stopword]
        stopword = stop_file.readline()
        # count += 1
        # print(count)
    # print("vocab length = ", len(vocab))


    #################### Test Set ####################
    subject_count = {}

    spam_count = 0
    ham_count = 0

    bayes_list = []
    spam_list = []

    test_input = input(
        "Please enter the name of the TEST set file including extension: \n")
    # print("Training = ", test_input)
    test_file = open(test_input, 'r')
    subject_line = test_file.readline()
    # print("subject_line = ", subject_line)
    while subject_line != "":
        # print("while...")
        is_spam = int(subject_line[:1])
        if is_spam == 1:
            # spam += 1
            spam_count += 1
            spam_list.append(1)
        else:
            # ham += 1
            ham_count += 1
            spam_list.append(0)

        subject_line = cleantext(subject_line[1:])

        subject = subject_line.split()
        # print("subject list = ", subject)
        subject = set(subject)
        subject_count = countWords(subject, is_spam, subject_count)

        ####################
        ham_sl_prob = 0
        spam_sl_prob = 0
        
        for key in vocab:
            if key in subject:
                ham_sl_prob += math.log(vocab[key][0])
                spam_sl_prob += math.log(vocab[key][1])
            else:
                ham_sl_prob += math.log((1 - vocab[key][0]))
                spam_sl_prob += math.log((1 - vocab[key][1]))

        ham_sl_prob = math.exp(ham_sl_prob)
        spam_sl_prob = math.exp(spam_sl_prob)
        print("subject line = ", subject)
        print("hamProb = ", ham_prob, " spamProb = ", spam_prob, "\nhamSL = ", ham_sl_prob, " spamSL = ", spam_sl_prob)

        bayes_list.append(naive_bayes(ham_prob, ham_sl_prob, spam_prob, spam_sl_prob))

        subject_line = test_file.readline()
    # print(subject_count)

    

    confusion_matrix(bayes_list, spam_list)

    test_file.close()
    # print(vocab)

def confusion_matrix(bayes_values, spam_values):
    print("bayes = ", len(bayes_values), " spam = ", len(spam_values) )
    confusion_matrix  = [] 
    tp = 0 
    fp = 0
    tn = 0
    fn = 0

    for z in range(len(bayes_values)):
        if bayes_values[z] > 0.5:
            confusion_matrix.append(1)
        else:
            confusion_matrix.append(0)
    
    for el in range(len(confusion_matrix)):
        if confusion_matrix[el] == spam_values[el] and spam_values[el] == 0:
            tn += 1
        elif confusion_matrix[el] == spam_values[el] and spam_values[el] == 1:
            tp += 1
        elif confusion_matrix[el] != spam_values[el] and spam_values[el] == 0:
            fp += 1
        else:
            fn += 1

    accuracy = (tp + tn) / (tp + tn + fp + tn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)  
    f1_score = 2 * (1 / ( (1 / precision) + (1 / recall) )) 

    print("\nFP = ", fp)
    print("TP =", tp)
    print("FN = ", fn)
    print("TN = ", tn)
    print("accuracy = ", accuracy)
    print("precision = ", precision)
    print("recall ", recall)
    print("F1 score = ", f1_score, "\n")
    


def cleantext(text):
    # print("text = ", text)
    text = text.lower()
    text = text.strip()
    for letters in text:
        # print("clean text loop")
        if letters in """[]!.,"-!-@;':#$%^&*()+/?""":
            text = text.replace(letters, " ")
    return text


def countWords(text, is_spam, counted):
    for each_word in text:
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

def naive_bayes(notSpamProb, notSlSpamProb, spamProb, slSpamProb ):
    notValues = notSlSpamProb * notSpamProb
    posValues = slSpamProb * spamProb
    print("notvalues = ", notValues)
    print("posvalues = ", posValues)

    exponent = math.log(notValues) - math.log(posValues)
    bayes_prob = 1 / (1 + math.exp(exponent))
    print("Naive Bayes prediction: ", bayes_prob)

    # return random.uniform(0, 1)
    return bayes_prob
    


project_three()
