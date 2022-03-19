#!/bin/bash
#$ -S /bin/bash   
#$ -N DiffKS-combine-fus
#$ -cwd    
# merge stdo and stde to one file
#$ -j y

###from __future__ import print_function, unicode_literals, division
echo "job start time: `date`"
#chatbot
/Work18/2019/wangruifang/anaconda3/envs/pytorch_1.1/bin/python main.py
#/Work18/2019/wangruifang/anaconda3/envs/pytorch_1.1/bin/python evaluate.py
echo "job end time `date`"

