import csv
import logging


class LoadData:

    logging.basicConfig(level=logging.INFO)

    MIN_CHARS = 60

    def __init__(self, filenames):
        self.filenames = filenames

    def load(self, grp_key=2, grp_value=4):
        c_oc = 0
        c_voc = 0
        data = {}
        for filename in self.filenames:
            f = open(filename, "rb")
            lines = csv.reader(f)

            for l in lines:
                c_oc += 1
                if len(l[grp_value]) >= self.MIN_CHARS:
                    c_voc += 1
                    if l[grp_key] in data:
                        data[l[grp_key]] = data[l[grp_key]] + "\n" + l[grp_value]
                    else:
                        data[l[grp_key]] = l[grp_value]

        logging.info("total occurences: %s", c_oc)
        logging.info("total of unique clients: %s", len(data))
        logging.info("average - clients x occurrences: %s", (c_voc / len(data)))

        return data
