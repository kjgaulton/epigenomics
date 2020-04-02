## DGA Submission, v3

1.  **Adding experimental data**

Experiments are molecular assays run by a research group - for example ATAC-seq, RNA-seq, ChIP-seq, and Hi-C.  

1.1.	  Overview of necessary steps:

1)	Create ‘donor’ entry for all samples included in the experiment.  
2)	Create ‘biosample’ (e.g. tissue, cell type) entry for each tissue sample obtained from each ‘donor’ used in the experiment
3)	Create ‘library’ entry from each biosample that was assayed in experiment including all technical replicates of the assay for that biosample
4)	If there is an associated target (e.g. antibody for ChIP) and it doesn’t exist in database, then ‘target’ entry needs to be created prior to creating the experiment
5)	Create ‘experiment’ entry describing assay performed on donor biosamples
6)	Once ‘experiment’ is created add libraries for each donor biosample to experiment under ‘replicates’
7)	Optional: Create ‘publication’ entry describing publications associated with experiment
8)	Audit and submit data files associated with experiment record

If submitting lab doesn’t exist in database, then need to create ‘lab’ and associated ‘grant’ for lab prior to creating the experiment.  Email DGA team to help with creating the required lab and grant records, or if admin, can create lab/grant records directly via the web or command line scripts

If submitting user does not have access key and secret, please email DGA team to obtain them.  Admins can create access keys by signing in and viewing page for specific user via the web site


1.2.	  Adding experimental meta-data into the site

There are two primary ways to add meta-data:

1.2.1.	Visit web site and add in meta-data via web forms directly

Easiest when submitting small amount of data, <10-20 experiments.  Click ‘add’ at the top of the pages listed below and fill in all information on web form.  Required fields are marked with ‘*’, and for some fields the set of possible values are restricted to biomedical ontology terms

Create donors:  http://www.diabetesepigenome.org/donors/

Create biosamples: http://www.diabetesepigenome.org/biosamples/

Create libraries: http://www.diabetesepigenome.org/libraries/

If ChIP-seq (or another assay with a target protein), add target: http://www.diabetesepigenome.org/targets/ 

If there is an associated publication, add publication: http://www.diabetesepigenome.org/publications/

Create experiment: http://www.diabetesepigenome.org/experiments/ 

Once the experiment is created, add library accession numbers to the experiment by selecting ‘edit’ from the top right and adding ‘replicates’ – depending on the experiment there could be technical or biological replicates or both.  If only one library for the experiment the technical and biological replicate numbers would both be numbered 1.   

1.2.2.	Complete spreadsheet and post meta-data using macros

Easiest when submitting data in larger batches, >20 experiments

A template Google sheet for submission is here: https://docs.google.com/spreadsheets/d/1hQ24_CDW1b-rQ9chMl5GdUiFVMn7IGWAPLWQsEp_WX8/edit?usp=sharing – which contains examples of submitted meta-data and data files.  Copy this spreadsheet into a new sheet for your own submissions.  

IMPORTANT:  Make sure to modify the ‘init.gs’ script in the sheet to include your own access key and secret, and if you are submitting data for another site (e,g. not to DGA) make sure to update the script to point to your own site to post data (instead of diabetesepigenome.org).  Email Ying Sun with any questions pertaining to editing your scripts.  Furthermore, as part of the submission process meta-data is posted to an intermediate site where the schema is checked for accuracy – we provide an intermediate server which handles this, but in the case that you wanted to set up your own server you will need to modify the script ‘submission.gs’ and change the ‘url’ variable.  Email Ying Sun with any questions about how to set this server up with the required scripts through AWS.           

Complete DONOR form containing “award”, “lab”, “organism” and any other meta-data associated with donors (e.g. sex, age).  The ‘aliases’ in column 3 is your own internal unique ID/name for the donor and is needed to connect the donor to other records.

Complete BIOSAMPLE form containing “award”, “lab”, “biosample_term_id” (name of tissue/cell), “biosample_type” (tissue/primary cell/etc.), “source”, “organism” and any other meta-data for the biosamples associated with the donors.  The ‘aliases’ in column 3 is your own internal ID/name for the biosample and is needed to connect the biosample to other records, and ‘donor.text’ in column 4 is the alias of the donor associated with that biosample.

Complete LIBRARY form containing “award”, “lab”, “biosample” (accession number of biosample used to generate library), “nucleic_acid_term_id” (e.g. DNA, RNA), size range (e.g. 200, 400), and other meta-data for the library associated with these biosamples.  The ‘aliases’ in column 3 is your own internal unique ID/name for the library and is needed to connect the library to other records, and ‘biosample’ in column 8 is the alias of the biosample associated with that library.

Complete EXPERIMENT form containing “award”, “lab”, “assay_term” (e.g. ATAC-seq), “biosample_term_name”, “biosample_term_id” (CL/UBERON ID), “biosample_type” (tissue/primary cell/etc.), “target” (if target exists; can be blank), “possible_controls” (possible control used, e.g. for ChIP-seq; can leave blank) and other meta-data for experiments associated with these donors/biosamples/libraries.  The ‘aliases’ column 3 is your own internal unique ID/name for the experiment and is needed to connect the experiment to other records.   

Complete REPLICATES form which connects experiments to libraries.   Also include “biological_replicate_number” and “technical_replicate_number” in order to record which libraries are biological and technical replicates for the experiment.  If there is just one library associated with the experiment, the biological replicate number and the technical replicate number would both be 1.  The ‘aliases’ column 3 is your own internal unique ID/name for the replicate which is used to connect the replicate to other records, and ‘experiment’ in column 4 and ‘library’ in column 7 are the aliases for the experiment and library, respectively, that the replicate is associated with. 
  
After filling in, submit through “T2DREAM->ALL/Selected->Post to T2DREAM”.  For modifications to an existing record, submit through “T2DREAM->ALL/Selected->Patch to T2DREAM”.  

Column B needs to be left blank when doing submission.  If information has been submitted without any problems, column B will return “success”.  

The experiment accession number can be obtained from “T2DREAM->ALL/Selected->Get from T2DREAM”.  


1.3.	  Submit data files associated with experiment

There are two primary ways to submit data files to an experiment:

1.3.1.	Running a command line script

The script ‘submit_file.py’ in GitHub allows you to post data files to an experiment.  The inputs to the script need to be manually changed to include your access keys, the file path you are submitting, lab, award, the experiment accession and replicate the file belongs to, and meta-data about the file itself including file type and other information (e.g. read length if .fastq).

python3 submit_file.py  

** We are actively working on improving this script to help make file submission much easier without needing to manually update the script contents each time **

1.3.2.	 Completing spreadsheet and submitting via command line script

The data submission spreadsheet contains a FILE form which one can fill out with file info, including the ‘alias’ for the experiment in the ‘dataset’ column and - if associated with a specific library – for the replicate in the ‘replicate’ column.  (Note that the column ‘fastq_file’ for the file name can be any file type submitted to the site - fastq, bed, bigwig, etc.) 

Once the FILE form is completed then copy the contents of the sheet into a text file and run the script ‘gz2T2D.pl’:

perl gz2T2D.pl my_submission_spreadsheet.txt  

** In order for the gz2T2D.pl script to run correctly you may need to install module JSON::Parse **


1.4.	 Audit and release experiment

For data being submitted to DGA, the DGA team will audit and then release files.  

Once the meta-data and data files are successfully posted, email the DGA team a list of experiments to audit and desired release dates for each experiment.  

For non-DGA sites and submissions with manual auditing and release: 

To audit visit the experiment accession page to view meta-data, samples and data files and make sure everything looks consistent and the necessary information is present, and the data files pass quality metrics.  

Once the experiment is audited and correct, the experiment can be released using the script ‘ENCODE_release.py’ in Github:

python ENCODE_release.py --keyfile keypairs.json --update --force --infile ~/Desktop/assays_to_release.txt

Where ‘keypairs.json’ contains your access keys and ‘assays_to_release.txt’ contains a text list of accession numbers.

More detail about data release can be found here:  https://github.com/T2DREAM/t2dream-portal/blob/master/t2dream_docs/release-data.md


2.	Adding annotation data 

Annotations are analytical distillations of experiments, and can include files such as chromatin states, accessible chromatin sites, target gene predictions, QTLs, and other summary-level data 

2.1.	 Overview of steps

1)	If submitting lab doesn’t exist in database, then need to create ‘lab’ and associated ‘grant’ for lab prior to creating the annotation
2)	Create ‘annotation’ entry describing annotation created from experiments
3)	Optional: Create ‘publication’ entry describing publication associated with annotation
4)	Optional: Add ‘software’ used to create annotation, add new software record if not in database
5)	Submit data files associated with annotation record
6)	Audit and release annotation

If submitting lab doesn’t exist in database, then need to create ‘lab’ and associated ‘grant’ for lab prior to creating the annotation.  Email DGA team to help with creating the required lab and grant records.

If submitting user does not have access keys, please email DGA team to obtain them.  

2.2.	  Adding annotation meta-data into the site

Visit web site and add in meta-data via web form directly.  Click ‘add’ at the top of the www.diabetesepigenome.org/annotations/ page and fill in all information on form.  Required fields are marked with ‘*’, and for some fields the set of possible values are restricted to biomedical ontology terms.

2.3.	  Submit data files associated with annotation

There are two primary ways to submit data files to an experiment:

2.3.1.	Running a command line script

The script ‘submit_file.py’ in GitHub allows you to post data files to an annotation.  The inputs to the script need to be manually changed to include your access keys, the file path you are submitting, lab, award, the annotation accession and replicate the file belongs to, and meta-data about the file itself including file type and other information (e.g. read length if .fastq).

python3 submit_file.py  

** We are actively working on improving this script to help make file submission much easier without needing to manually update the script contents each time **

2.3.2.	Completing spreadsheet and running macro

A template Google sheet for submission is here: https://docs.google.com/spreadsheets/d/1hQ24_CDW1b-rQ9chMl5GdUiFVMn7IGWAPLWQsEp_WX8/edit?usp=sharing – which contains examples of submitted meta-data and data files.  There are two scripts ‘init.gs’ and ‘submission.gs’ that are required to post data.    

IMPORTANT:  Make sure to modify the scripts in the sheet to include your own access key and secret, and if you are submitting data for another site (e,g. not to DGA) make sure to update the script to point to your own site to post data instead of diabetesepigenome.org.  In addition, you will need to provide a server URL that JSON can be posted to as a staging area prior to submission to the site.  Email Ying with any questions pertaining to editing your scripts.         

The data submission spreadsheet contains a FILE form which one can fill out with file info, including the ‘alias’ for the annotation in the ‘dataset’ column.  (Note that the column ‘fastq_file’ for the file name can be any file type submitted to the site - fastq, bed, bigwig, etc.) 

Once the FILE form is completed then copy the contents into a tab-delimited text file and run the script ‘gz2T2D.pl’:

perl gz2T2D.pl my_submission_spreadsheet.txt  

** In order for the gz2T2D.pl script to run correctly you may need to install module JSON::Parse **

2.4.	Audit and release experiment

For data being submitted to DGA, the DGA team will audit and then release files.  

Once the meta-data and data files are successfully posted, email the DGA team a list of experiments to audit and desired release dates for each experiment.  

For non-DGA sites and submissions with manual auditing and release: 

To audit visit the experiment accession page to view meta-data, samples and data files and make sure everything looks consistent and the necessary information is present, and the data files pass quality metrics.  

Once the experiment is audited and correct, the experiment can be released using the script ‘ENCODE_release.py’ in Github:

python ENCODE_release.py --keyfile keypairs.json --update --force --infile ~/Desktop/assays_to_release.txt

Where ‘keypairs.json’ contains your access keys and ‘assays_to_release.txt’ contains a text list of accession numbers. 

More detail about data release can be found here:  https://github.com/T2DREAM/t2dream-portal/blob/master/t2dream_docs/release-data.md



