#!/usr/bin/env python
# -*-coding:utf-8 -*-

import codecs
from Table import *

class PayStubTableFactory :

    @staticmethod
    def __parse_page_header(f, header, separator="\t"):
        # After skipping 3 lines
        # There are company and date on the fourth line
        for i in range(0, 4) :
            s = f.readline()

        record = s.rstrip("\n").strip(separator).split(separator)
        company = record[0]
        date = record[4].strip() + record[7]

        header.setProperty("company", company)
        header.setProperty("date", date)

        # Skip 5th and put the 6th line in the s
        for i in range(0, 2) :
            s = f.readline()

    @staticmethod
    def __skip_table_header(f, separator = "\t"):
        while True :
            lastPos = f.tell()
            line = f.readline()
            record = line.rstrip("\n").strip(separator).split(separator)

            if TableHeader.NAME_PATTERN.match(record[0]) :
                f.seek(lastPos)
                break

    @staticmethod
    def __parse_table_header(f, header, separator="\t"):
        # header starts
        # for i in range(0, 7) :
        #    s = f.readline()
        #    print s,
        
        while True :
            lastPos = f.tell()
            line = f.readline()
            record = line.rstrip("\n").split(separator)

            if TableHeader.NAME_PATTERN.match(record[0]) :
                f.seek(lastPos)
                break

            header.addRow()
            for col in record :
                col_name = col.strip()
                if len(col_name) == 0 :
                    col_name = TableHeader.EMPTY_FIELD
                header.addField(col_name)

            #for col in (header.row(header.rowSize()-1)) :
            #    print col,
            #print


    EMPTY_DATA = object()


    @staticmethod
    def __parse_record(f, table, separator="\t") :
        #for i in range(0, 7) :
        #    s = f.readline()
        #    print s,
        headerTable = table.header
        spreadOut = []
        
        for hRow in headerTable.headerTable :
            record = f.readline().strip("\n").split(separator)

            i = 0
            for hCol in hRow :
                if hCol.name == TableHeader.EMPTY_FIELD :
                    spreadOut.append(PayStubTableFactory.EMPTY_DATA)

                else:

                    if hCol.rowIndex == 0 and hCol.colIndex == 0 :
                        if TableHeader.NAME_PATTERN.match(record[i]) :
                            record[i] = record[i].split(".")[1].strip()
                       
                    table.insert(hCol, record[i])
                    #spreadOut.append(record[i])

                i += 1

        #table.rowArray.append(spreadOut)

        #line = "\t".join([ x for x in spreadOut if x != PayStubTableFactory.EMPTY_DATA])
        #print line




        #extract date from the second lint
        #date = s.rstrip("\n").strip("\t")
        #dateObject = datetime.datetime.strptime(date, "%Y.%m.%d")
        #s = f.readline() 
        #date = dateObject.strftime("%Y-%m-%d")
        #
        #for i in range(3, 7) :
        #    s = f.readline()


    @staticmethod
    def __parseRecords(f, table, separator) :
        while True :
            lastPos = f.tell()
            line = f.readline().strip()
            f.seek(lastPos)

            if len(line) == 0 :
                break;
            
            PayStubTableFactory.__parse_record(f, table, separator)

    @staticmethod
    def parse(filePath, enc, separator="\t") :

        f = open(filePath, "r")

        # if enc != "utf8" or enc != "utf-8" :
        clazz = codecs.getreader(enc)
        reader = clazz(f)
        f = reader

        # while True :
        #     line = reader.readline()
        #     if line is None or line == "":
        #         break
        #
        #     print line
        #
        # import sys
        # sys.exit(0)

        header = TableHeader()
        table = Table(header)

        page = 1
        while True :

            if page == 1 :
                PayStubTableFactory.__parse_page_header(f, header, separator)
                PayStubTableFactory.__parse_table_header(f, header, separator)
            else :
                PayStubTableFactory.__skip_table_header(f, separator)

            PayStubTableFactory.__parseRecords(f, table, separator)

            page += 1

            lastPos = f.tell()
            line = f.readline()

            if line == '' :
                break
            else :
                f.seek(lastPos)

        return table



    @staticmethod
    def save(table, f) :
        headerTable = table.header

        headerArray = []
        for hRow in headerTable.headerTable :
            for hCol in hRow :
                if hCol.name != TableHeader.EMPTY_FIELD :
                    headerArray.append(hCol.name)

        headerArray.append("\n")
        f.write("\t".join(headerArray))

        size = table.size()
        for i in xrange(1, size) :
            record = table.row(i)
            record.append(u"\n")
            s = "\t".join(record)

            f.write(s.encode("utf-8"))



