---
layout: post
title: "Second problem" #Anything else xD
date: 2018-12-01
feature: /newAssets/Anuj/featureImage.jpg
excerpt: "Solution to the second problem"
comments: false
---

# **Question:**

Write a shell script to simulate a stack and queue using only shell commands. It should
support the following operations, displayed to the user:

• Check if stack/queue is empty: isEmpty

• Insert data from terminal (make proper checks): insert

• Delete data only if not empty: delete

• Read the top record of the stack and first record of the queue: top, first 

# **Solution code for the same:**

```
#!/bin/bash
echo "Press Ctrl+C to Exit"
count=0
LIN=""
while :
do
        read LIN
        LINE=$(echo $LIN | tr "," " ")
        IFS=' ' read -ra parts <<< "$LINE"
        if [ "${parts[0]}" == "insert" ]
        then
                arr[$count]=$(echo ${LINE#* })
                count=$(($count+1))
        elif [ "${parts[0]}" == "delete" ]
        then
                if [ "$count" -eq 0 ]
                then
                        echo "List Already Empty"
                else
                        count=$(($count-1))
                fi
        elif [ "${parts[0]}" == "isEmpty" ]
        then
                echo "$count Entries Present"
        elif [ "${parts[0]}" == "top" ]
        then
                if  [ "$count" -eq 0 ]
                then
                        echo Stack is Empty
                else
                        echo "${arr[$(($count-1))]}"
                fi
        fi
done
```
---

