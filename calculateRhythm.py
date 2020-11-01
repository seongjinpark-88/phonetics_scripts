#!/usr/bin/python

import sys

def sum_list(my_list): 
	sum_list = 0
	for i in my_list:
		sum_list = sum_list + i
	return(sum_list)

def mean_list(my_list):
	num_item = len(my_list)
	sum_item = sum_list(my_list)
	mean_value = sum_item / num_item
	return mean_value

def stdv_list(my_list):
	num_value = len(my_list)
	average_value = mean_list(my_list)
	sum_diff = 0
	for i in my_list:
		diff = (i - average_value) ** 2
		sum_diff = sum_diff + diff
	stdv = (sum_diff / num_value) ** 0.5
	return stdv

def nPVI(my_list):
	num_value = len(my_list)
	sum_value = 0
	for i in range(0, num_value-1):
		diff = my_list[i] - my_list[i+1]
		mean = (my_list[i] + my_list[i+1]) / 2
		result = abs(diff / mean)
		sum_value = sum_value + result
		# print(diff, mean, result)

	nPVI = (100 * sum_value) / (num_value - 1)
	return(nPVI)

def rPVI(my_list):
	num_value = len(my_list)
	sum_value = 0
	for i in range(0,num_value-1):
		diff = abs(my_list[i] - my_list[i + 1])
		sum_value = sum_value + diff

	rPVI = sum_value / (num_value - 1)
	return(rPVI)

import os
path = sys.argv[1]
files = os.listdir(path)

my_dict = {}

out = open(os.path.join(sys.argv[2], "rhythm_v3.csv"), "w")
out.write("fileName,%V,deltaV,deltaC,VarcoV,VarcoC,nPVI-V,rPVI-C,SyllPerSec,%Pause\n")

vowel = ["A", "E", "I", "O", "U"]

for file in files:
	tmp_dict = {}
	if (file[-4:] == ".txt"):
		print(file)
		fileName = path + "/" + file
		my_lab = open(fileName, "r")
		data = my_lab.readlines()

		vowlList = []
		consList = []

		total_dur = 0
		pause_dur = 0	

		npvi_v = []
		rpvi = []

		tmp_v = 0
		tmp_c = 0
		# for line in data:
		for i in range(0, len(data)):
			line = data[i]
			line = line.replace("\n","")
			# line = line.lower()
			items = line.split()
			print(line)
			phone = items[5].split("_")[0]

			duration = (float(items[3]) - float(items[2]))
			# duration = duration * 1000

			total_dur += duration

			if (any(i in phone for i in vowel) and phone != "SIL"):
				vowlList.append(duration)
				if i == 0:
					tmp_dict[i] = "V"
					tmp_v += duration
				else:
					tmp_dict[i] = "V"
					if tmp_dict[i-1] != "C":
						tmp_v += duration
					elif tmp_dict[i-1] == "C":
						rpvi.append(tmp_c)
						tmp_c = 0
						tmp_v += duration

			elif(phone != "SIL"):
				consList.append(duration)
				if i == 0:
					tmp_dict[i] = "C"
					tmp_c += duration
				else:
					tmp_dict[i] = "C"
					if tmp_dict[i-1] != "V":
						tmp_c += duration
					elif tmp_dict[i-1] == "V":
						npvi_v.append(tmp_v)
						tmp_v = 0
						tmp_c += duration
			else:
				tmp_dict[i] = "SIL"
				pause_dur += duration
				if tmp_v != 0:
					npvi_v.append(tmp_v)
					tmp_v = 0
				if tmp_c != 0:
					rpvi.append(tmp_c)
					tmp_c = 0
					
			print(tmp_dict)
			print(tmp_v, tmp_c)
			print(duration)
			print(npvi_v, rpvi)

		print("npvi ", npvi_v)

		sylpersec = total_dur / len(vowlList)
		perc_v = (sum_list(vowlList) / total_dur) * 100
		delta_v = stdv_list(npvi_v)
		delta_c = stdv_list(rpvi)
		varco_v = 100 * delta_v / mean_list(npvi_v)
		varco_c = 100 * delta_c / mean_list(rpvi)
		nPVI_v = nPVI(npvi_v)
		rPVI_c = rPVI(rpvi)
		sylpersec = len(vowlList) / total_dur
		perc_pause = (pause_dur / total_dur) * 100

		out.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (file,perc_v,delta_v,delta_c,varco_v,varco_c,nPVI_v,rPVI_c,sylpersec,perc_pause))
		# out.close()
		# exit()		
out.close()
