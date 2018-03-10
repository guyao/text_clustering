import os
import argparse
import json
import logging
import sys
import Parser


class TextClustering:
    def __init__(self, input_folder, output_folder):
        self.categories = {
            "needs": {"C02", "C05"},
            "resources": {"C06", "T04", "T05", "T06", "T07", },
            "issues": {"C01", "C03", "C04", "C07", "C08", "O01", "O02", "O03", "O04", "T01", "T02", "T03", "T08", "T09", "T10", "T11", },
        }
        self.parser = Parser.load_parser()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.__init_storage()

    def __init_storage(self):
        from collections import defaultdict
        self.result_category_id = defaultdict(list)

    def process(self):
        for filename in os.listdir(self.input_folder):
            self.process_file(os.path.join(self.input_folder, filename))
        for category in self.categories.keys():
            self.output(category, json.dumps(self.result_category_id[category]))

    def output(self, category, s):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        with open(os.path.join(self.output_folder, category + ".json"), "a") as f:
            f.write(s)
            f.write("\n")

    def process_result(self, r):
        if r["category"] in self.categories.keys():
            self.result_category_id[r["category"]].append(r["DocumentID"])

    def process_file(self, fn):
        with open(fn) as f:
            s = f.read()
            r = self.process_json(json.loads(s))
            logger.info("Category: " + str(r["category"]))
            logger.info("")
        self.process_result(r)

    def process_json(self, j_obj):
        r = {}
        logger.info("Text: " + str(j_obj["originalText"]))

        # result
        r["category"] = self.process_text(j_obj["originalText"])
        r["DocumentID"] = self.process_id(j_obj)
        return r

    def process_text(self, s):
        labels = self.parser.findall(s)
        logger.info("Parser Labels: " + str(labels))
        return self.classify(labels)

    def process_id(self, json_obj):
        """
        Format 1. json object ["llAnnotation"]["DocumentID"] (str)
        Format 2. json object ["id"] (int)
        """
        document_id = None
        if json_obj.get("llAnnotation"):
            if json_obj.get("llAnnotation").get("DocumentID"):
                document_id = json_obj.get("llAnnotation").get("DocumentID")
        elif json_obj.get("id"):
            document_id = json_obj.get("id")
        if type(document_id) != str:
            document_id = str(document_id)
        return document_id

    def classify(self, labels):
        classified_label = None
        if not labels:
            classified_label = None
        if any((label in self.categories["needs"] for label in labels)):
            classified_label = "needs"
        elif any((label in self.categories["resources"] for label in labels)):
            classified_label = "resources"
        else:
            classified_label = "issues"
        return classified_label


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Clustering text to needs, resources, issues categories."
        )
    )

    parser.add_argument(
        "input",
        help="Input folder name",
    )

    parser.add_argument(
        "output",
        help="Output folder name",
    )

    parser.add_argument(
        "-v",
        help="Verbose output",
        action='store_true',
        default=False,
    )
    args = parser.parse_args()
    logger = logging.getLogger()

    if args.v:
        console_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)

    TextClustering(args.input, args.output).process()
