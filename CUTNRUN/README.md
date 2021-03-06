# CUT N RUN pipeline

Required tools that need to be installed in order to run pipeline:  
> **BWA**:  http://bio-bwa.sourceforge.net/  
> **samtools**:  http://www.htslib.org/  
> **MACS**:  https://github.com/taoliu/MACS  
  
Primary output files from the pipeline:
> Peak calls: output_peaks.narrowPeak  
> Filtered, sorted alignment: output.sort.filt.rmdup.bam  
> Read depth track: output_treat_pileup.bdg  
> Normalized read depth track: output_ppois.sorted.bdg.gz  

Usage:
```
usage: cut_and_run_pipeline.py [-h] -r1 READ1 -r2 READ2 -o OUTPUT [-n NAME]
                               [-t THREADS] [-m MEMORY] [-q QUALITY]
                               --reference REFERENCE --picard-md PICARD_MD
                               [-f FRAGMENT_SIZE]
                               [--macs2-genome MACS2_GENOME]
                               [--genome-size GENOME_SIZE] [--skip-trim]
                               [--skip-align] [--skip-rmdup] [--skip-peaks]

Pipeline for cut and run to trim reads, align them to a reference genome, call
peaks, and generate a genome browser signal track.

optional arguments:
  -h, --help            show this help message and exit

I/O arguments:
  -r1 READ1, --read1 READ1
                        Path to paired-end reads 1 file
  -r2 READ2, --read2 READ2
                        Path to paired-end reads 2 file
  -o OUTPUT, --output OUTPUT
                        Output directory for processed files
  -n NAME, --name NAME  Output sample name to prepend

Alignment arguments:
  -t THREADS, --threads THREADS
                        Number of threads to use [8]
  -m MEMORY, --memory MEMORY
                        Maximum memory (in Gb) per thread for samtools sort
                        [4]
  -q QUALITY, --quality QUALITY
                        Mapping quality cutoff for samtools [30]
  --reference REFERENCE
                        Path to BWA-prepared reference genome
  --picard-md PICARD_MD
                        Path to picard MarkDuplicates.jar

Alignment arguments:
  -f FRAGMENT_SIZE, --fragment-size FRAGMENT_SIZE
                        Maximum fragment size [120]

MACS2 arguments:
  --macs2-genome MACS2_GENOME
                        MACS2 genome (e.g. hs or mm) for peak calling
  --genome-size GENOME_SIZE
                        Genome size file for hg19 from UCSC
                        [etc/hg19.chrom.sizes]

Skip processing steps:
  --skip-trim           Skip adapter trimming step [ON]
  --skip-align          Skip read alignment step [OFF]
  --skip-rmdup          Skip remove duplicates step [OFF]
  --skip-peaks          Skip calling peaks step [OFF]

```
