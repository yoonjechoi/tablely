#!/usr/bin/env python
# -*-coding:utf-8 -*-

import sys
import argparse
from collections import defaultdict

import Table
from PayStubTableFactory import *


# def profileRows(filePath) :
#     book = xlrd.open_workbook(filePath)
#     sh = book.sheet_by_index(0)
#
#     counter = defaultdict(int)
#
#     for rx in range(sh.nrows) :
#         row = sh.row(rx)
#         key = u"".join([ unicode(cell.value) for cell in row])
#         counter[key] += 1
#
#     for key, value in counter.items() :
#         if key.strip() != "" and value > 1 :
#             print key, value


def main() :
    parser = argparse.ArgumentParser(description="converting normal paystubs into table form.")
    parser.add_argument("--input")
    parser.add_argument("--encoding")
    parser.add_argument("--output", type=argparse.FileType("w"))
    parser.add_argument("--separator", default="\t")

    tableList = []
    args = parser.parse_args()
    for inputFilePath in args.input.split(",") :

        table = PayStubTableFactory.parse(inputFilePath, args.encoding, args.separator)

        # header = table.header
        # for field in header :
        #     print field
        #
        # tableList.append(table)
        PayStubTableFactory.save(table, args.output)
    #merged = PayStubTableFactory.mergeTables(tableList)

    #PayStubTableFactory.save(merged, args.database)
        

if __name__ == "__main__" :
    main()
