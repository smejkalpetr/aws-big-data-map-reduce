import glob
import shutil

for input_file in glob.iglob("/user/hadoop/input/input_file*.txt"):
	words = sc.textFile(input_file).flatMap(lambda line: line.split(" "))
	cnt = words.map(lambda word: (word, 1))
	cnt_aggregated = cnt.reduceByKey(lambda a,b:a +b)
	cnt_aggregated.saveAsTextFile(f'{input_file}_output_wordcount_spark.txt')