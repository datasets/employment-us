import os
import re
import csv
import shutil

import swiss
cache = swiss.Cache('cache')


class Parser(object):
    space = re.compile(r'\s\s+')
    headings = [
        'Year',
        'Civilian noninstitutional population',
        'Civilian labor force (Total)', '% of Population',
        'Employed Total', '% of Population',
        '(of which) Agriculture', '(of which) Non-Agriculture',
        'Unemployed (Number)', '% of labor force', 'Not in labor force',
        'Footnotes',
        ]
    urls = ['ftp://ftp.bls.gov/pub/special.requests/lf/aat1.txt',
            # 'ftp://ftp.bls.gov/pub/special.requests/lf/aat2.txt'
            ]

    def download(self):
        for url in self.urls:
            cache.retrieve(url)

    def get_row(self, line, minimum_number_of_columns=3):
        # need 2 or more spaces!
        row = self.space.split(line)
        if len(row) <= minimum_number_of_columns:
            return None
        # clean up first row (what do we do about footnotes)
        row[0] = row[0].replace('.', '')
        # extract fn
        # either yyyy (fn) or just yyyy
        out = row[0].split()
        if len(out) == 2:
            fn = out[1][1:-1]
        else:
            fn = ''
        row[0] = out[0]
        row.append(fn)
        row[1:-1] = [ xx.replace(',', '') for xx in row[1:-1] ]
        return row

    def parse_file(self, fo, title_line, value_range, footnote_range=[]):
        count = -1
        title = ''
        headings = []
        rows = []
        fns = []
        for line in fo:
            count += 1
            line = line.strip()
            # skip blank lines
            if not line: continue
            # not the same line in every file!!
            if count == title_line:
                title = line
            if count in value_range:
                print line
                row = self.get_row(line)
                # remove blank lines
                if row:
                    rows.append(row)
            if count in footnote_range:
                # More hacking because fns can spill over multiple lines
                # Assume never more than five fns
                # TODO make this more robust ...
                if line and line[0] in ['1', '2', '3', '4', '5' ]:
                    fns.append(line)
                else:
                    fns[-1] += ' ' + line
        return title, rows, fns

    # TODO: col titles (a complete mess ...)
    def parse_1(self, fo):
        comments = 'Persons 14 years of age and over 1940-1947, Persons 16 years of age and over 1948 onwards'
        return self.parse_file(fo, 5, range(22, 103), [103, 104])

    def parse_2(self, fo):
        return self.parse_file(fo, 3, range(20, 103), [103])

    def make_csv(self):
        outfns = []
        for url in Parser.urls:
            fn = cache.retrieve(url)
            fo = file(fn)
            title, rows, fns = self.parse_1(fo)
            csvfn = fn[:-3] + 'csv'
            outfns.append(csvfn)
            csvfo = file(csvfn , 'w')
            writer = csv.writer(csvfo)
            writer.writerow(self.headings)
            for row in rows:
                writer.writerow(row)
            csvfo.close()
            print 'CSV file %s written ok' % csvfn
            print 'Title: ', title
            print 'Footnotes: ', fns
        return outfns

def execute():
    parser = Parser()
    outfns = parser.make_csv()
    src = outfns[0]
    dest = os.path.join(os.path.dirname('__file__'), 'data.csv')
    print 'Copying: %s to %s' % (src, dest)
    shutil.copy(src, dest)

if __name__ == '__main__':
    execute()

    # fn = 'aat1.txt'
    # fo = file(fn)
    # title, rows, fns = parse_1(fo)
    # print title, fns, rows
