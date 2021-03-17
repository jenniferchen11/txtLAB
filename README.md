# txtLAB
txtlAB is a natural language processing and data science research at McGill University. The Python scripts in this repository were created to conduct text analysis in a comparison between LGBTQ+ fan-fictions and New York Times bestsellers. 

## To get started

Download the files.

```bash
git clone https://github.com/bam-emr/ipfs-react.git <FOLDER NAME>
```
Now navigate to the directory, 

Certain libraries require Anaconda environment.
Download Anaconda: https://www.anaconda.com/products/individual

Creating a conda environment:

```bash
conda create -n name_of_my_env python
```
Other libraries may need to be downloaded as well:

```bash
conda install pandas
```

## Using Python Scripts

```bash
topic_model_2.py
```
Outputs 2 term topic matrices (k=35,40) AND a topic probability matrix for each data set.

```bash
bootstrap.p
```
Creates 1000 bootstrap samples from the topic probability matrix.

```bash
events.py
```
Captures bigrams and trigrams of (subject, action) or (subject, action, object).


