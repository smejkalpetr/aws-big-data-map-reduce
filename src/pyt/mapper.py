#!/usr/bin/env python3

import sys

for line in sys.stdin:
    
    line_format=line.split() # contains the index of the person and the list of friends
    person=line_format[0]
    if len(line_format)>1:
        line_format[1]=line_format[1].split(',')#line_format1 is a array of friends now
        for friend1 in line_format[1]:
            for friend2 in line_format[1]:
                if friend1!= friend2:
                    print("%s\t%s\t%d"%(friend1,friend2,1))#here friend 1 is the key and friend 2 is value and the last number shows if the key value pair is 1 than they have at least 1 friend in common , if it is 0 then they are direct friends
            print("%s\t%s\t%d"%(person,friend1,0))#include the friends with the 0 to identify it as a direct friend
    else:
        print("%s\t%s\t%d"%(person,person,0))#include one key-pair in case that the person do not have friends , so they will be included in the output
    
    

    