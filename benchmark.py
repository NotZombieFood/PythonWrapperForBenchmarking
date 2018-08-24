import subprocess, sys, getopt, csv


def runCMD(command):
	result = 0
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		line_string = line.strip().decode("utf-8")
		print(line_string)
		if 'Milliseconds ' in line_string:
			result = int(line_string.split(':')[1])
			break
	return result

def benchmark(file, isUnix):
	unix_command = 'ts=$(date +%s%N) ; ./$file ; tt=$((($(date +%s%N) - $ts)/1000000)) ; echo "Miliseconds:$tt"'.replace('$file', file)
	windows_command = 'powershell Measure-Command {.\$file}'.replace('$file', file)
	command = unix_command if isUnix else windows_command
	results = []
	for i in range(0,99):
		results.append(runCMD(command))
	avg = float(sum(results))/len(results)
	return avg

def append2CSV(file,data):
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(data)

def main(argv):
	#here we should parse all the inputs
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ofile=","ifile="])
	except getopt.GetoptError:
		print ('benchmark.py -o <inputfile> -i <outputfiles, divided by commas>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('benchmark.py -i <inputfile> -o <outputfiles, divided by commas>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	tests = inputfile.split(',')
	isUnix = True if "win" not in sys.platform else False
	for test in tests:
		result = benchmark(test, isUnix)
		print("%s has result an average of %.5f miliseconds"%(test,result))
		append2CSV(outputfile,[test,result])
	

if __name__ == "__main__":
   main(sys.argv[1:])
