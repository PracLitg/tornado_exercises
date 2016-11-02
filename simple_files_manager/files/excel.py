# -*- encoding:utf-8 -*-
import xlrd

data = xlrd.open_workbook('test.xlsx')
table = data.sheets()[0]

# get the values of the second column
col_num = len(table.col_values(1))
sec_col_values = []
for x in xrange(2, col_num):
	ele = table.col_values(1)[x]
	if ele:
		sec_col_values.append(ele.strip())

# get the values of the forth column
for_col_values = []
for x in xrange(2, col_num):
	ele = table.col_values(3)[x]
	if ele:
		for_col_values.append(ele.strip())

# handle data of the forth column
for_col_meta_values = []
route_node = {}
for tmp in xrange(0, len(for_col_values)):
	ele = for_col_values[tmp]
	#for ele in for_col_values:
	# get the content after the colon(if exists)
	route_content = ele.split(':')
	if len(route_content) == 2:
		route_content = ele.split(':')[1]
	else:
		route_content = ele.split(':')[0]
	meta = ''
	meta_values = []
	# get the value of each route node
	#for index in xrange(0,len(route_content)):
	index = 0
	while index < len(route_content):
		if route_content[index] != '-':
			meta += route_content[index]
		else:
			count = 0
			while route_content[index] == '-':
				count += 1
				index += 1
			index -= 1
			if count > 2:
				meta_values.append(meta)
				meta = ''
			elif count == 1:
				meta += '-'
		index += 1
	meta_values.append(meta)
	for item in meta_values:
		if item not in route_node.keys():
			route_node[item] = []
		route_node[item].append(tmp)
	#for_col_meta_values.append(meta_values)

with open('result.txt', 'w') as fout:
	for key,value in route_node.iteritems():
		if len(value) > 1:
			fout.write(key.encode('utf-8') + ':\r\n        ')
			for ele in value:
				fout.write(sec_col_values[int(ele)].encode('utf-8') + '    ')
			fout.write('\r\n')


'''
with open('route_node.txt', 'w') as fout:
	for ele in for_col_meta_values:
		for ele1 in ele:
			fout.write(ele1.encode('utf-8'))
			fout.write(' ')
		fout.write('\n')
'''
