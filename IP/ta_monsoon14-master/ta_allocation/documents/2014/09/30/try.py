import xlrd
import csv

def csv_from_excel():

    wb = xlrd.open_workbook('Book1.xls')
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('Book1.csv', 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
    	print sh.row_values(rownum)
        wr.writerow(sh.row_values(rownum))

    


csv_from_excel()
with open('Book1.csv','rb') as file:
	print "hello"
	contents = csv.reader(file, delimiter='\n')
	for row in contents:
		print row
