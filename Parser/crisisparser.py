import re
import csv
import io
from collections import defaultdict
import pkgutil


class CrisisParser:
    def __init__(self, data=pkgutil.get_data(__package__, "data/pattern_data")):
        self.category = defaultdict(list)
        self.code_category = {}
        csvio = io.StringIO(data.decode("utf-8"))
        csvreader = csv.reader(csvio)
        next(csvio) # skip first line
        for l in csvreader:
            term, code, category, ex = l
            self.category[code].append(term)
            if not self.code_category.get(code):
                self.code_category[code] = category
    
    def findall(self, s):
        res = []
        for code in self.category.keys():
            for term in self.category[code]:
                result = self.match_one(term, s)
                if result:
                    res.append(code)
                    break
        return res

    def find_pattern(self, s):
        res = []
        for code in self.category.keys():
            for term in self.category[code]:
                result = self.match_one(term, s)
                if result:
                    res.append((code, term,))
        return res

    def match_one(self, t, s):
        # TODO
        
        res = False
        
        # 0. Preprocessing

        # Preprocessing sentence
        s = " ".join(s.split())

        # Preprocessing term
        t = re.sub("\(", "\(", t)
        t = re.sub("\)", "\)", t)
        t = re.sub("\+", "\)", t)        
        t = re.sub("\?", "\?", t)

        if re.findall("{Number}", t):
            # {Number} 
            number = "\d+"
            written_number = "(zero|one|two|three|four|five|six|seven|eight|nine)"
            number_pattern = "(?<!\S)(?=.)(0|([1-9](\d*|\d{0,2}(,\d{3})*)))?(\.\d*[1-9])?(?!\S)"
            t1 = re.sub("{Number}", number, t)
            t2 = re.sub("{Number}", number_pattern, t)
            t3 = re.sub("{Number}", written_number, t)
            res = res or re.findall(t1, s, re.I) or re.findall(t2, s, re.I) or re.findall(t3, s, re.I) 
        else:
            res = re.findall(t, s, re.I)
        return res


def load_parser():
    return CrisisParser()



