#!/usr/bin/env python3
import sys
def output_recommendations(my_key,friends): 
    '''receives the id of the user and list of possible recommendations, it will sort by number of friends in common (descendent order) and by id(ascendent order) and writes in the output'''
    friends_list=friends.items()
    friends_list=sorted(friends_list,key=lambda x:x[0]) #sort by id first(ascendent order)
    friends_list=sorted(friends_list,key=lambda x:x[1],reverse=True) #sort by number of friends in common(descendent order)
    top10=friends_list[0:10]
    top10_formatted=[]
    for i in top10:
        if i[1]!=0:
            top10_formatted.append(i[0]) #select top10 valid friends
    output=",".join([str(x) for x in top10_formatted])
    print("%d\t%s"%(my_key,output)) #output the result
        
last_key=-1
new_friends={} #dictionary of possible friends
for line in sys.stdin:
    line_format=line.split("\t")
    key=int(line_format[0]) #id of the user
    friend_id=int(line_format[1]) #id of the friend
    not_friend_yet=int(line_format[2]) # identifies if is not a direct friend
    if last_key!=key and last_key!=-1: # when the user change , generate the output
        output_recommendations(last_key,new_friends)
        new_friends={}
    last_key=key
    if friend_id not in new_friends: #create key-value pair in the dictionary
        new_friends[friend_id]=not_friend_yet
    else: #if value that was in the dictionary is 0 or the new value is 0 , the new value will be 0 too (showing that it is a direct friend) , or the sum of them otherwise.
        new_friends[friend_id]=(new_friends[friend_id]+not_friend_yet) if (new_friends[friend_id] and not_friend_yet) else 0
output_recommendations(last_key,new_friends)

    