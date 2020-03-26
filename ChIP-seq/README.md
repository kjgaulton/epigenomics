# ChIP-seq pipeline

NOTE: several files necessary for the pipeline are in the etc/ directory.  An indexed reference genome is another necessary file but due to size not supplied here

Required tools that need to be installed in order to run pipeline:  
> **BWA**:  http://bio-bwa.sourceforge.net/  
> **samtools**:  http://www.htslib.org/  
> **MACS**:  https://github.com/taoliu/MACS  
> **deepTools**:  https://deeptools.readthedocs.io/en/develop/content/installation.html  
  
Primary output files from the pipeline:
> Peak calls: output_peaks.narrowPeak  
> Filtered, sorted alignment: output.sort.filt.rmdup.bam 
> Filtered, sorted control alignment: output_control.sort.filt.rmdup.bam
> Read depth track: output_treat_pileup.bdg  
> Control-normalized read depth track: output.ppois.bdg  
> RPKM-normalized genome browser read depth track: output.rpkm.bw 

Usage:
```
ChIP-seq_pipeline.py [-h] -t TREATMENT -c CONTROL -o OUTPUT [-n NAME]
                            [-p PROCESSES] [-m MEMORY] [-q QUALITY]
                            [-ref REFERENCE] [-markdup MARKDUP]
                            [--qvalue QVALUE] [--broad]
                            [--broad_cutoff BROAD_CUTOFF] [--color COLOR]
                            [--macs2_genome MACS2_GENOME]
                            [--genomeSize GENOMESIZE] [--skip_align]
                            [--skip_peaks] [--skip_track] [--skip_rpkm]

Pipeline for ChIP to align reads to a reference genome, and then call peaks.

optional arguments:
  -h, --help            show this help message and exit

I/O arguments:
  -t TREATMENT, --treatment TREATMENT
                        Path to treatment file [.fastq.gz OR .bam if
                        --skip_align is ON]
  -c CONTROL, --control CONTROL
                        Path to control file [.fastq.gz OR .bam if
                        --skip_align is ON]
  -o OUTPUT, --output OUTPUT
                        Output directory for processed files
  -n NAME, --name NAME  Output sample name to prepend

Alignment and rmdup arguments:
  -p PROCESSES, --processes PROCESSES
                        Number of processes to use [4]
  -m MEMORY, --memory MEMORY
                        Maximum memory per thread [8]
  -q QUALITY, --quality QUALITY
                        Mapping quality cutoff for samtools [10]
  -ref REFERENCE, --reference REFERENCE
                        Path to reference genome prepared for BWA
                        [ucsc.hg19.fasta]
  -markdup MARKDUP, --markdup MARKDUP
                        Path to MarkDuplicates.jar [etc/MarkDuplicates.jar]

MACS2 parameters:
  --qvalue QVALUE       MACS2 callpeak qvalue cutoff [0.05]
  --broad               Broad peak option for MACS2 callpeak [OFF]
  --broad_cutoff BROAD_CUTOFF
                        MACS2 callpeak qvalue cutoff for broad regions [0.05]
  --color COLOR         Color in R,G,B format to display for genome browser
                        track [0,0,0]
  --macs2_genome MACS2_GENOME
                        MACS2 genome size (e.g. hs for human, mm for mouse)

Signal track parameters:
  --genomeSize GENOMESIZE
                        Genome size for RPKM calculation [2864785220 for hg19]

Skip processing:
  --skip_align          Skip read alignment step [OFF]
  --skip_peaks          Skip calling peaks step [OFF]
  --skip_track          Skip making signal track for genome browser [OFF]
  --skip_rpkm           Skip making rpkm normalized browser track [OFF]
  ```
