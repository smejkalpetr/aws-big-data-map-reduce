sudo apt install dos2unix
dos2unix mapper.py
dos2unix reducer.py
mapred streaming -input input.txt -output output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py