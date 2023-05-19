import string

def parse(fname):
    f = open(fname,'r')
    txt = f.read()
    txt = txt.split()

    f.close()
    lst = []
    count = 0
    for line in txt:
        if 'SPAN' not in line and '>' not in line:
            text = line
            # t = str.maketrans("","")
            # text = line.translate((t,string.punctuation))
            # text = "".join([i if i.isalnum() or i.isspace() else "" for i in line])
            lst.append((text.lower(),count,len(line)))
            count+= len(line)+1
    return lst

def parse_new(fname):
    f = open(fname,'r')
    raw = f.read()
    f.close()
    new = ""
    for i in range(len(raw)):
        if raw[i] in ['\n','\xa0']:
            new+=" "
        else:
            new+=raw[i]
    raw = new
    # print(raw)
    words = []
    current = ""
    current_offset = 0
    offset = -1
    for character in raw:
        offset+=1
        if character not in [' ']:
            current+= character
            if len(current) == 1:
                current_offset = offset
        else:
            if current != '':
                words.append((current.lower(),current_offset))
                current = ''

    return words

def ngrams(words):
    n = 5
    ngrams = []
    
    for i in range(len(words)-n+1):
        ngram = words[i:i+n]
        offset = ngram[0][1]

        ngram = [i[0] for i in ngram]
        ngram = " ".join(ngram)
        ngram = (ngram,offset,len(ngram))

        ngrams.append(ngram)

def ngram_stopwords(words):
    n = 5
    ngrams = []
    words_revised = []
    # stop_words = ['is','and','or','in','a','her','his','their','which','for','but','the','of','to','it','was','for','but','has','have','not','this',]
    stop_words = 'the of and a in to is was it for with he be on i that by at you are not his this from but had which she they or an were we their been has have will would her there can all as if what who said'
    stop_words = stop_words.split()
    for word in words:
        if word[0] in stop_words:
            words_revised.append(word)

    for i in range(len(words_revised)-n+1):
        ngram = words_revised[i:i+n]
        offset = ngram[0][1]

        ngram_word_only = [i[0] for i in ngram]
        ngram_word_only = " ".join(ngram_word_only)

        # length = (ngram[-1][1] + len(ngram[-1][0]))-offset
        end_index = ngram[-1][1] + len(ngram[-1][0])

        ngram = (ngram_word_only,offset,end_index)

        ngrams.append(ngram)

        
    # a sdf fsd in
    # 0123456789

    return ngrams

def check(case_instance):
    case_instance = case_instance.split()
    suspicious_name = case_instance[0]
    source_name = case_instance[1]

    # suspicious_sentences = parse('./dataset/susp/'+suspicious_name)
    # source_sentences = parse('./dataset/src/'+source_name)

    suspicious_sentences = parse_new('./dataset/susp/'+suspicious_name)
    source_sentences = parse_new('./dataset/src/'+source_name)

    # print(suspicious_sentences)

    suspicious_ngrams = ngram_stopwords(suspicious_sentences)
    source_ngrams = ngram_stopwords(source_sentences)
    # print(suspicious_ngrams[0:3])
    src_plain_ngrams = [i[0] for i in source_ngrams]
    cases = []
    current = ""
    offset_sus = 0
    offset_src = 0
    len_src = 0
    len_sus = 0
    prev = None
    flag = False

    for i,a in enumerate(suspicious_ngrams):
        phrase = a[0]
        if phrase in src_plain_ngrams:
            src_data = source_ngrams[src_plain_ngrams.index(phrase)]
            if current=="":
                current = phrase
                offset_sus = a[1]
                offset_src = src_data[1]
                len_src = src_data[2]-offset_src
                len_sus = a[2] - offset_sus
            else:
                if current.split()[-1] == phrase.split()[-2]:
                    current+=" "+ phrase.split()[-1]
                    len_src = src_data[2]-offset_src
                    len_sus = a[2] - offset_sus
                else:
                    cases.append((current,offset_sus,len_sus,offset_src,len_src))
                    current=phrase
                    offset_sus = 0
                    offset_src = 0
                    len_src = 0
                    len_sus = 0

        else:
            if current != "":
                cases.append((current,offset_sus,len_sus,offset_src,len_src))
                current = ""
                offset_sus = 0
                offset_src = 0
                len_src = 0
                len_sus = 0
        prev = a
    if (current,offset_sus,len_sus,offset_src,len_src) not in cases:
        cases.append((current,offset_sus,len_sus,offset_src,len_src))



    # for ngram in suspicious_ngrams:
    #     phrase = ngram[0]
    #     if phrase in src_plain_ngrams:
    #         src_data = source_ngrams[src_plain_ngrams.index(phrase)]
    #         if current=="":
    #             current = phrase
    #             offset = ngram[1]
    #             offset_src = src_data[1]
    #         else:
    #             if current.split()[-1] == phrase.split()[-2]:
    #                 current+=" "+ phrase.split()[-1]
    #             elif current.split()[-1] == prev[0].split()[-1]:
    #                 current+=phrase
    #             else:
    #                 cases.append((current,offset,len(current),offset_src))
    #                 current=phrase
                    
    #     else:
    #         if current != "":
    #             cases.append((current,offset,len(current),offset_src))
    #             current = ""
    #     prev = ngram



    return cases



    
    


if __name__ == '__main__':
    pairs = ""
    f= open("./dataset/02-no-obfuscation/pairs",'r')
    pairs = f.readlines()
    f.close()
    f = open("./dataset/01-no-plagiarism/pairs",'r')
    pairs += f.readlines()
    f.close()
    f = open("./dataset/03-random-obfuscation/pairs",'r')
    pairs += f.readlines()
    f.close()
    # pairs = ['suspicious-document00006.txt source-document00860.txt']
    # pairs = ['testsus.txt testsrc.txt']
    count = -1
    all_cases = []
    for pair in pairs:
        count+=1
        case = check(pair)
        # sus, src, len, sus offset, src offset
        a = pair.split()[0]
        b = pair.split()[1]
        # print(case)

        filename = filename = a[:-4]+"-"+b[:-4]+".xml"

        # if len(case) > 0:
        f = open('./all-detections/'+filename,'w')
        str = f'<document reference="{a}" >'
        f.write(str)
        f.write("\n")
        
            
        for instance in case:
            if instance not in all_cases and instance[2]>0 and instance[4]>0:
                sus = pair.split()[0]
                src = pair.split()[1]
                all_cases.append((sus,src,instance[2],instance[1],instance[3]))
                sus_name = sus
                sus_offset = instance[1]
                sus_length = instance[2]
                src_name = src
                src_offset = instance[3]
                src_length = instance[4]

                xml_str = """ <feature name="detected-plagiarism" source_length="{source_length}" source_offset="{source_offset}" source_reference="{source_name}" this_length="{sus_length}" this_offset="{sus_offset}" />\n""".format(suspicious_name=sus_name,source_length=src_length,source_offset=src_offset,source_name = src_name, sus_length=sus_length,sus_offset=sus_offset)
                if src_length < 0 or sus_length < 0:
                    print(xml_str)
                f.write(xml_str)
            
        f.write("</document>\n")
        f.close()
    


