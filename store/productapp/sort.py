def sort_index():
	rows = []
	with open("index.txt","r") as file:
		for line in file:
			row = line.split(" ")
			rows.append(row)
	rows = sorted(rows, key = lambda x: x[1])
	new_row = []
	for row in rows:
		row = " ".join(row)
		new_row.append(row)
	with open("index.txt" ,"w") as file:
		file.writelines(new_row)


def sort_secindex():
	rows = []
	with open("secindex.txt","r") as file:
		for line in file:
			row = line.split(" ")
			rows.append(row)
	rows = sorted(rows, key = lambda x: x[1])
	new_row = []
	for row in rows:
		row = " ".join(row)
		new_row.append(row)
	with open("secindex.txt" ,"w") as file:
		file.writelines(new_row)