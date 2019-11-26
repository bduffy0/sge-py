#!/usr/bin/env python3

import subprocess
import argparse
import pandas as pd
import re

def remove_colon(s):
    return re.sub(':\d','',s)

def split_range(s):
    # given a range e.g. 5-8, splits into 5,6,7,8
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)

    r = [str(x) for x in r]
    return r

def split_task_list(task_list):
    # split id list e.g. from 166-168:1 to 166,167,168
    task_list = task_list.split(',')
    task_list = [remove_colon(x) for x in task_list]
    task_list = [split_range(x) for x in task_list]
    task_list = [x for y in task_list for x in y] # flatten
    return task_list


def make_command_list(task_number):
    # makes qsub command from a given task id
    command_list = ['qsub','-cwd','-t',task_number,command] + args_to_command
    return command_list

parser = argparse.ArgumentParser()
parser.add_argument('-c',help='command (normally shell script)')
parser.add_argument('-a',nargs='*',help='input arguments',default=[])
parser.add_argument('-t',help='task id list as csv e.g. -t "1,2,3,4,5"')
parser.add_argument('-i',default=None,help='input file list(instead of task id list')
parser.add_argument('-f',default=None,help='filelist to read input from - only used with -i ')
args = parser.parse_args()

if args.c is None:
    raise(ValueError('requires -c command argument'))

if args.t is None:
    raise(ValueError('requires -t command argument'))


# if input file list instead of task id then find task id
if args.i is not None:
    print(args.f[0])
    filelist = pd.read_csv(args.f, sep = ' ',names=['id','path'],dtype={'id':str})
    id_list = args.i.split(',')
    id_list = [x.replace(' ','') for x in id_list]
    print(id_list)
    task_list = filelist[filelist['id'].isin(id_list)].index.astype('str').values
    print(task_list)
else:
    input_task_list = args.t
    task_list = split_task_list(input_task_list)

command = args.c
args_to_command = args.a

if __name__=='__main__':

    print('task list',task_list)
    for task in task_list:
        cmd = make_command_list(task)
        print(' '.join(cmd))
        out = subprocess.Popen(cmd)




