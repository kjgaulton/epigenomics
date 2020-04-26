# PLAC-seq/HiChIP pipeline

Requirements:
> Install feather/MAPS and all listed dependencies: https://github.com/ijuric/MAPS  
> Obtain reference genome and index with BWA  

Primary output:
> Interactions: output.resolution.2.sig3Dinteractions.bedpe  


```
MAPS_pipeline.py [-h] -f1 FASTQ1 -f2 FASTQ2 -p PEAKS -o OUTPUT
                        [-n NAME] -r REFERENCE -m MAPS [-t THREADS] [-b BUILD]
                        [--binsize BINSIZE] [--binrange BINRANGE]
                        [--mapq MAPQ] [--length LENGTH] [--model MODEL]
                        [--optdup OPTDUP]

Wrapper pipeline for analyzing PLAC-seq data using MAPS.

optional arguments:
  -h, --help            show this help message and exit

I/O arguments:
  -f1 FASTQ1, --fastq1 FASTQ1
                        Input fastq read 1
  -f2 FASTQ2, --fastq2 FASTQ2
                        Input fastq read 2
  -p PEAKS, --peaks PEAKS
                        Reference peak calls
  -o OUTPUT, --output OUTPUT
                        Output directory for processed files
  -n NAME, --name NAME  Output sample name to prepend

Tools:
  -r REFERENCE, --reference REFERENCE
                        Reference genome
  -m MAPS, --maps MAPS  Directory of MAPS installation

Parameters:
  -t THREADS, --threads THREADS
                        Number of threads [4]
  -b BUILD, --build BUILD
                        Genome build (hg19, hg38, mm10, mm9) [hg19]
  --binsize BINSIZE     Bin size (5000, 10000, 20000, 40000, 50000, 100000, 200000, 500000, 1000000)[10000]
  --binrange BINRANGE   Binning range [1000000]
  --mapq MAPQ           MAPQ threshold [30]
  --length LENGTH       Length cutoff [1000]
  --model MODEL         Model (pospoisson, negbinom) [pospoisson]
  --optdup OPTDUP       Optical duplicate distance [0]
```

