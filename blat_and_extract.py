#!/usr/bin/env python

# A tool for searching one set of sequences against another and extracting all that hit.
#
#

import argparse
import os
from Bio import SeqIO

parser = argparse.ArgumentParser(description="A tool for BLATing one set of sequences against another and extracting all that hit.")
parser.add_argument("-d", dest='database', action='store', required=True, help='fasta formatted reference sequence(s)')
parser.add_argument("-q", dest='query', action='store', required=True, help='query sequences in fasta format (sequences to extract)')
parser.add_argument("-o", dest='output', action='store', required=True, help='fasta format output file for hits')
parser.add_argument("-p", dest='psl', action='store', required=False, default='tmp.psl', help='temporary psl file for blat output')
parser.add_argument("-s", dest='sample', action='store', required=True, help='sample name')

#args = parser.parse_args("-d Limonius_californicus.fasta -q contigs.fasta -o hits.fasta -p tmp.psl -s Zymo3".split())

args = parser.parse_args()

print ("----------" + args.sample + "----------")

# Set up index into the query file:
idx = SeqIO.index(args.query, 'fasta')

#Set up command and run it:
cmd = 'blat -minScore=200 -minIdentity=75 ' + args.database + ' ' + args.query + ' ' + args.psl
os.system(cmd)

out = open(args.output, 'w')
written = {}

i=0
recs_written=0
for l in open(args.psl, 'r'):
    i += 1
    if i <=5:
        continue
    l2 = l.strip().split("\t")
    score = l2[0]
    query = l2[9]
    target = l2[13]
    print ("query =", query, "score =", score, "target =", target)
    if query not in written:
        written[query] = True
        recs_written += 1
        rec = idx[query]
        rec.id = args.sample + "-contig" + str(recs_written) + "_:_" + rec.id
        SeqIO.write( rec, out, 'fasta')

out.close()
