#!/usr/bin/env python3

import argparse
import subprocess
import os 
import sys
import reprlib
import logging

#=======================================================#

def main(args):
	logging.info('Starting up.')
	if not os.path.isdir(args.output):
		try:
			os.makedirs(args.output)
		except OSError:
			pass
	logging.info('Running feather.')
	feather_dir = args.output + '/feather_output/'
	if not os.path.isdir(feather_dir):
                try:
                    	os.makedirs(feather_dir)
                except OSError:
                        pass
	res = str(int(args.binsize)/1000)
	resolution = res[0:-2]

	gbuild='hg19'
	chrnum='22'
	resfile='hg19'
	if args.build=='hg38':
		gbuild='hg38'
		chrnum='22'
		resfile='GRCh38'
	if args.build=='mm10':
		gbuild='mm10'
		chrnum='19'
		resfile='mm10'
	if args.build=='mm9':
		gbuild='mm9'
		chrnum='19'
		resfile='mm9'

	genome_feat = args.maps + '../MAPS_data_files/' + gbuild + '/genomic_features/F_GC_M_MboI_' + resolution + 'Kb_el.' + resfile + '.txt'
	feather_log = feather_dir + args.name + '.log'
	feather_path = args.maps + '/feather/feather_pipe'
	feather_cmd = ['python3', feather_path, 'preprocess', 
			'-o', feather_dir,
			'-p', args.name,
			'-f1', args.fastq1,
			'-f2', args.fastq2,
			'-b', args.reference, 
			'-q', args.mapq,
			'-l', args.length,
			'-t', args.threads,
			'-c', 'True',
			'-a', args.peaks,
			'-d', args.optdup ]
	with open(feather_log, 'w') as f:
		subprocess.call(feather_cmd, stderr=f)
	logging.info('Running MAPS 1.')
	maps_dir = args.output + '/MAPS_output/'
	if not os.path.isdir(maps_dir):
		try:
			os.makedirs(maps_dir)
		except OSError:
			pass
	maps_log = maps_dir + args.name + '.log'
	maps_path = args.maps + '/MAPS/make_maps_runfile.py'
	maps_cmd = ['python3', maps_path, args.name, maps_dir, args.peaks, genome_feat, feather_dir, feather_dir, args.binsize, chrnum, maps_dir, 'X', '--BINNING_RANGE', args.binrange ]
	with open(maps_log, 'w') as f:
		subprocess.call(maps_cmd, stderr=f)
	logging.info('Running MAPS 2.')
	maps2_path = args.maps + '/MAPS/MAPS.py'
	maps2_input = maps_dir + 'maps_' + args.name + ".maps"
	maps2_cmd = ['python3', maps2_path, maps2_input ]
	with open(maps_log, 'w') as f:
		subprocess.call(maps2_cmd, stderr=f)
	logging.info('Running MAPS 3.')
	maps3_path = args.maps + '/MAPS/MAPS_regression_and_peak_caller.r'
	maps3_input = args.name + "." + resolution + 'k'
	chrnumx = chrnum + 'X'
	maps3_cmd = ['Rscript', maps3_path, maps_dir, maps3_input, args.binsize, chrnumx, 'None', args.model ]
	with open(maps_log, 'w') as f:
                subprocess.call(maps3_cmd, stderr=f) 
	logging.info('Running MAPS 4.')
	maps4_path = args.maps + '/MAPS/MAPS_peak_formatting.r'
	maps4_input = args.name + '.' + resolution + 'k'
	maps4_cmd = ['Rscript', maps4_path, maps_dir, maps4_input, '2', args.binsize ]
	with open(maps_log, 'w') as f:
		subprocess.call(maps4_cmd, stderr=f)

	logging.info('Finishing up.')
	return

#=======================================================#

def process_args():
	parser = argparse.ArgumentParser(description='Pipeline for analyzing PLAC-seq data using MAPS.')
	
	io_group = parser.add_argument_group('I/O arguments')
	io_group.add_argument('-f1', '--fastq1', required=True, type=str, help='Input fastq read 1')
	io_group.add_argument('-f2', '--fastq2', required=True, type=str, help='Input fastq read 2')
	io_group.add_argument('-p', '--peaks', required=True, type=str, help='Reference peak calls')
	io_group.add_argument('-o', '--output', required=True, type=str, help='Output directory for processed files')
	io_group.add_argument('-n', '--name', required=False, type=str, default='sample', help='Output sample name to prepend')

	proc_group = parser.add_argument_group('Tools')
	proc_group.add_argument('-r', '--reference', required=True, type=str, help='Reference genome')
	proc_group.add_argument('-m', '--maps', required=True, type=str, help='Directory of MAPS installation')
	
	param_group = parser.add_argument_group('Parameters')
	param_group.add_argument('-t', '--threads', required=False, type=str, default="4", help='Number of threads [4]')
	param_group.add_argument('-b', '--build', required=False, type=str, default="hg19", help='Genome build (hg19, hg38, mm9, mm10) [hg19]')
	param_group.add_argument('--binsize', required=False, type=str, default="10000", help='Bin size (5000, 10000, 20000, 40000, 50000, 100000, 200000, 500000, 1000000) [10000]')
	param_group.add_argument('--binrange', required=False, type=str, default="1000000", help='Binning range [1000000]')
	param_group.add_argument('--mapq', required=False, type=str, default="30", help='MAPQ threshold [30]')
	param_group.add_argument('--length', required=False, type=str, default="1000", help='Length cutoff [1000]')
	param_group.add_argument('--model', required=False, type=str, default="pospoisson", help='Model (pospoisson, negbinom) [pospoisson]')
	param_group.add_argument('--optdup', required=False, type=str, default='0', help='Optical duplicate distance [0]')
	
	return parser.parse_args()

#=======================================================#
if __name__ == '__main__':
	logging.basicConfig(format='[%(filename)s] %(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)
	args = process_args()
	main(args)
