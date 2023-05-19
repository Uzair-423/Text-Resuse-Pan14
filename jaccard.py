import string

def bow(a,b):
    a = a.split()
    b = b.split()

    a = set(a)
    b = set(b)

    intersection = a.intersection(b)
    union = a.union(b)

    score = len(intersection)/len(union)

    if score > 0.3:
        return True
    else:
        return False

def wrapper(a,lst):
    final = False
    for j,i in enumerate(lst):
        final = bow(a,i)
        if final:
            return lst.index(i)
    
    return -1
    

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
                words.append((current.lower(),current_offset,len(current)))
                current = ''

    return words

def ngrams(words):
    n = 30
    ngrams = []
    
    for i in range(0,len(words)-n+1,10):
        ngram = words[i:i+n]
        offset = ngram[0][1]

        ngram = [i[0] for i in ngram]
        ngram = " ".join(ngram)
        ngram = (ngram,offset,len(ngram))

        ngrams.append(ngram)

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
    suspicious_ngrams = ngrams(suspicious_sentences)
    source_ngrams = ngrams(source_sentences)

    # suspicious_ngrams = ngrams(suspicious_sentences)
    # source_ngrams = ngrams(source_sentences)
    # print(len(source_ngrams))
    src_plain_ngrams = [i[0] for i in source_ngrams]
    cases = []
    current = ""
    offset_sus = 0
    offset_src = 0
    len_src = 0
    len_sus = 0
    prev_sus = None
    prev_src = None

    # for i,a in enumerate(suspicious_ngrams):
    #     phrase = a[0]
    #     x = wrapper(phrase,src_plain_ngrams)
    #     if x !=-1:
    #         src_data = source_ngrams[x]
    #         if current=="":
    #             current = phrase
    #             offset_sus = a[1]
    #             offset_src = src_data[1]
    #             len_src = src_data[2]-offset_src
    #             len_sus = a[2] - offset_sus
    #         else:
    #             if current.split()[-1] == phrase.split()[-2]:
    #                 current+=" "+ phrase.split()[-1]
    #                 len_src = src_data[2]-offset_src
    #                 len_sus = a[2] - offset_sus
    #             else:
    #                 cases.append((current,offset_sus,len_sus,offset_src,len_src))
    #                 current=phrase
    #                 offset_sus = 0
    #                 offset_src = 0
    #                 len_src = 0
    #                 len_sus = 0

    #     else:
    #         if current != "":
    #             cases.append((current,offset_sus,len_sus,offset_src,len_src))
    #             current = ""
    #             offset_sus = 0
    #             offset_src = 0
    #             len_src = 0
    #             len_sus = 0
    #     prev = a
    # if (current,offset_sus,len_sus,offset_src,len_src) not in cases:
    #     cases.append((current,offset_sus,len_sus,offset_src,len_src))

    # return cases


    for ngram in suspicious_ngrams:
        src_data = None
        phrase = ngram[0]
        x = wrapper(phrase,src_plain_ngrams)
        if x !=-1:
            src_data = source_ngrams[x]
            if current=="":
                current = phrase
                offset_sus = ngram[1]
                offset_src = src_data[1]
                
            else:
                current+=" "+ " ".join(phrase.split()[-10:])
        else:
            if current != "":
                len_sus = (prev_sus[1]+prev_sus[2])-offset_sus
                len_src = (prev_src[1]+prev_src[2])-offset_src
                cases.append((current,offset_sus,len_sus,offset_src,len_src))
                current = ""
        prev_sus = ngram
        prev_src = src_data



    return cases



    
    


if __name__ == '__main__':
    # input folders for the pairs
    f= open("./dataset/02-no-obfuscation/pairs",'r')
    pairs = f.readlines()
    f.close()
    f = open("./dataset/01-no-plagiarism/pairs",'r')
    pairs += f.readlines()
    # f.close()
    # f = open("./dataset/03-random-obfuscation/pairs",'r')
    # pairs += f.readlines()
    f.close()
    # pairs = ['suspicious-document00001.txt source-document01256.txt']
    # pairs = ['testsus.txt testsrc.txt']
    # pairs = ['suspicious-document00006.txt source-document00860.txt']
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
        # Output folder for the detections
        f = open('./copy-paste-detections/'+filename,'w')
        str = f'<document reference="{a}" >'
        f.write(str)
        f.write("\n")
        
            
        for instance in case:
            if instance not in all_cases and instance[2]>=50:
                sus = pair.split()[0]
                src = pair.split()[1]
                all_cases.append((sus,src,instance[2],instance[1],instance[3]))
                sus_name = sus
                sus_offset = instance[1]
                sus_length = instance[2]
                src_name = src
                src_offset = instance[3]
                src_length = instance[2]

                xml_str = """ <feature name="detected-plagiarism" source_length="{source_length}" source_offset="{source_offset}" source_reference="{source_name}" this_length="{sus_length}" this_offset="{sus_offset}" />\n""".format(suspicious_name=sus_name,source_length=src_length,source_offset=src_offset,source_name = src_name, sus_length=sus_length,sus_offset=sus_offset)
                # print(xml_str)
                f.write(xml_str)
            
        f.write("</document>\n")
        f.close()
    


