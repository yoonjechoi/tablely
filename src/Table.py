#!/usr/bin/env python
# -*-coding:utf-8 -*-

import re
from collections import *
import pdb

class Validator :
    def __init__(self) :
        pass

    def validate(self, record) :
        return True

    def setHeader(self, h) :
        self.header = h


class TableFactory :
    @staticmethod
    def parse(file) :
        raise NotImplementedError()


    @staticmethod
    def merge(tables) :
        raise NotImplementedError()
        
    @staticmethod
    def save(header, f) :
        raise NotImplementedError()



class Field :
    def __init__(self, name, rowIndex, colIndex) :
        self.name = name.encode("utf-8")
        self.rowIndex = rowIndex
        self.colIndex = colIndex

    def __str__(self) :
        return "(" + ",".join([self.name, str(self.rowIndex), str(self.colIndex)]) + ")"


class TableHeaderIterator() :
    def __init__(self, header):
        self.header = header
        self.nextRow = 0
        self.nextCol = 0

    def next(self) :
        header_table = self.header.headerTable

        if self.nextRow >= len(header_table) :
            raise StopIteration("nextRow = %d, number Of rows in headerTable = %d" \
                                % (self.nextRow, len(header_table)) )

        row = header_table[self.nextRow]

        if self.nextCol < len(row) :
            self.nextCol += 1
            return row[self.nextCol - 1 ]

        if self.nextRow >= (len(header_table) - 1) :
            raise StopIteration()

        self.nextRow += 1
        row = header_table[self.nextRow]
        self.nextCol = 1

        return row[0]




class TableHeader :
    def __init__(self) :
        self.headerTable = [] #2d array
        self.indexToFieldDict = dict() # < tuple, Field >
        self.properties = dict()

    def __iter__(self):
        return TableHeaderIterator(self)

    NAME_PATTERN = re.compile("\d+\. \D+")
    EMPTY_FIELD = "EMPTY_FIELD"

    def setProperty(self, key, value) :
        self.properties[key] = value

    def getProperty(self, key) :
        return self.properties[key]

    def addRow(self) :
        self.headerTable.append([])


    def addField(self, name) :
        rowIndex = len(self.headerTable) - 1
        row = self.headerTable[rowIndex]

        colIndex = len(row)
        field = Field(name, rowIndex, colIndex)
        self.indexToFieldDict[(rowIndex, colIndex)] = field
        row.append(field)

    def row(self, rowIndex) :
        return self.headerTable[rowIndex]

    def rowSize(self) :
        return len(self.headerTable)

    def indexOf(self, columnName) :
        return self.indexToFieldDict[(rowIndex, colIndex)] 

    def size(self) :
        count = 0
        for row in self.headerTable :
            for col in row :
                count += 1

        return count



class Table :
    def __init__(self, header ) :
        self.header = header
        self.columnDict = OrderedDict() #<Columna, [] >


    def setValidator(self, v) :
        v.setHeader(self.header)
        self.validator = v

    # def insert(self, record) :
    #     numberOfFields = self.header.size()

    #     if record == None or len(record) != numberOfFields :
    #         raise ValueError("Number of columns in the record is not same to number of columns in the header.\n \
    #                             number of columns in the header = [%d]\n\
    #                             number of columns in the record = [%d]"\
    #                             % (numberOfFields, (len(record), -1)[ record == None ] ))

    #     if self.validator != None and self.validator.validate(record) :
    #         self.rowArray.append(record)

    def insert(self, column, value) :
        if column not in self.columnDict.keys() :
            self.columnDict[column] = []

        data = self.columnDict[column]
        data.append(value)

    def header(self ) :
        return self.header

    def row(self, index) :

        record = []
        for field, colData in self.columnDict.iteritems() :
            record.append(colData[index])
        return record

    def size(self):
        if len(self.columnDict) == 0 :
            return 0
        return len(self.columnDict[self.columnDict.keys()[0]])


    def merge(self, table) :
        merged_header = TableHeader()


        field_dict = OrderedDict()  # <string, [ Field, ...] >
        column_index_dict = dict()  # <Field, int(columnIndex)>

        column_index = 0
        for field in self.header:
            field_name = field.name

            if field_name == TableHeader.EMPTY_FIELD:
                continue

            if field_name in field_dict:
                representative_field = field_dict[field_name][0]
                column_index_dict[field] = column_index_dict[representative_field]

            else:
                column_index_dict[field] = column_index
                field_dict[field_name] = [field]
                column_index += 1

        for field in table.header:
            field_name = field.name

            if field_name == TableHeader.EMPTY_FIELD:
                continue

            if field_name in field_dict:
                representative_field = field_dict[field_name][0]
                column_index_dict[field] = column_index_dict[representative_field]

            else:
                column_index_dict[field] = column_index
                field_dict[field_name] = [field]
                column_index += 1




        column_index = 0
        for t in tables :
            header = t.header

            #Iterate over headerTable row
            for row in header.headerTable :
                #Iterate over headerTable column
                for field in row :

                    if field.name in fieldDict :
                        bucket = fieldDict[field.name]
                        representativeField = bucket[0]
                        column_index_dict[field] = column_index_dict[representativeField]
                        bucket.append(field)

                    else :
                        column_index_dict[field] = column_index
                        fieldDict[field.name] = [ field ]
                        column_index += 1

        sorted(column_index_dict)




        return merged

