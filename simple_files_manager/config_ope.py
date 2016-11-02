import pymysql.cursors

class DisposeConfigration():
	def __init__(self):
		self.connection = pymysql.connect(host='127.0.0.1',user='root',password='314159',
			charset='utf8',cursorclass=pymysql.cursors.DictCursor)

	def create_table(self):
		cursor = self.connection.cursor()
		curr_time = time.strftime()

	def handle_data(self, stream):
		data_list = stream.strip().split('\n')

		fout = open('policy.txt', 'w')

		cursor = connection.cursor()

		for index, element in enumerate(data_list):
			if element.startswith('rule id'):  # match a policy
				rule_id = element.strip().split()[-1]
				src_zone = ''
				dst_zone = ''
				src_ip_or_addr = ''
				dst_ip_or_addr = ''
				service = ''
				description = ''

				index += 1  # next element
				while not data_list[index].startswith('exit'):
					element_inside = data_list[index].strip()
					if element_inside.startswith('src-zone'):
						src_zone = element_inside.split()[-1]
					elif element_inside.startswith('dst-zone'):
						dst_zone = element_inside.split()[-1]
					elif element_inside.startswith('src-ip') or element_inside.startswith('src-addr'):
						src_ip_or_addr += element_inside.split()[-1] + ','
					elif element_inside.startswith('dst-ip') or element_inside.startswith('dst-addr'):
						dst_ip_or_addr += element_inside.split()[-1] + ','
					elif element_inside.startswith('service'):
						service += element_inside.split()[-1] + ','
					index += 1

				'''fout.write('rule id ' + rule_id + '\n')
				fout.write('  src-zone ' + src_zone + '\n')
				fout.write('  dst-zone ' + dst_zone + '\n')
				fout.write('  src-ip ' + src_ip_or_addr + '\n')
				fout.write('  dst-ip ' + dst_ip_or_addr + '\n')
				fout.write('  service ' + service + '\n')
				fout.write('exit\n')'''
