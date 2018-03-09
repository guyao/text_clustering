import os
import argparse
import json
import logging
import sys
import Parser


class TextClustering:
    def __init__(self, input_filename, output_filename):
        self.categories = {
            "needs": {"C02", "C05"},
            "resources": {"C06", "T04", "T05", "T06", "T07", },
            "issues": {"C01", "C03", "C04", "C07", "C08", "O01", "O02", "O03", "O04", "T01", "T02", "T03", "T08", "T09", "T10", "T11", },
        }
        self.parser = Parser.load_parser()
        self.input_filename = input_filename
        self.output_filename = output_filename

    def process(self):
        for filename in os.listdir(self.input_filename):
            self.process_file(os.path.join(self.input_filename, filename))

    def output(self, category, s):
        if not os.path.exists(self.output_filename):
            os.makedirs(self.output_filename)

        with open(os.path.join(self.output_filename, category + ".json"), "a") as f:
            f.write(s)
            f.write("\n")

    def process_file(self, fn):
        with open(fn) as f:
            s = f.read()
            category = self.process_json(json.loads(s))
            logger.info("Category: " + str(category))
            logger.info("")

            if category in self.categories.keys():
                self.output(category, s)

    def process_json(self, j_obj):
        logger.info("Text: " + str(j_obj["originalText"]))
        return self.process_text(j_obj["originalText"])

    def process_text(self, s):
        labels = self.parser.findall(s)
        logger.info("Parser Labels: " + str(labels))
        return self.calssify(labels)

    def calssify(self, labels):
        if not labels:
            return None
        if any((label in self.categories["needs"] for label in labels)):
            return "needs"
        elif any((label in self.categories["resources"] for label in labels)):
            return "resources"
        else:
            return "issues"


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
