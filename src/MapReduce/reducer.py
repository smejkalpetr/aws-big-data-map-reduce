#!/usr/bin/env python3
import sys
def output_recommendations(my_key,friends):
    friends_list=friends.items()
    friends_list=sorted(friends_list,key=lambda x:x[0])
    friends_list=sorted(friends_list,key=lambda x:x[1],reverse=True)
    top10=friends_list[0:10]
    top10_formatted=[]
    for i in top10:
        if i[1]!=0:
            top10_formatted.append(i[0])
    output=",".join([str(x) for x in top10_formatted])
    print("%d\t%s"%(my_key,output))
        
last_key=-1
new_friends={}
for line in sys.stdin:
    line_format=line.split("\t")
    key=int(line_format[0])
    friend_id=int(line_format[1])
    not_friend_yet=int(line_format[2])
    if last_key!=key and last_key!=-1:
        output_recommendations(last_key,new_friends)
        new_friends={}
    last_key=key
    if friend_id not in new_friends:
        new_friends[friend_id]=not_friend_yet
    else:
        new_friends[friend_id]=(new_friends[friend_id]+not_friend_yet) if (new_friends[friend_id] and not_friend_yet) else 0
output_recommendations(last_key,new_friends)

    