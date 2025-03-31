## What can you get from OSS-FGI:

1. Dataset of malicious software packages.
2. FGI extraction code.
3. Data analysis code.

## Documentation 

### Extract_FGI
We have written the front-end of the webpage type. We have two extraction modes: online or offline. You need to enter the file (.txt) address or folder address respectively to perform batch processing to extract information.

### Data_Analysis

**Classifer_BaseOnNPM** contains code and dataset for classifier training(NPM ecosystem).
- word2vec_embedding: embed many kinds of text data as vectors.
- machine_learing_4kinds: use machine learning and deep learning algorithms to learn and classify vectors.
- end_result: metadata、static、dynamic and all 3 machine/deep learning result data.
- other folder: word-text dataset,embedding-vector dataset. Especially, the dataset with noget in the name represents the dataset after removing the empty data in static.

**Data_acquisition** contains dataset we extracted and the extraction method
- get_all_sum: get all types of data(name, OSS, description, author, maintainer, URL, dependencies number, Static_APIs, Dynamic_APIs).
- Dynamic_msg_ip: count the number of messages and IP addresses in the dynamic API.
- other folder: Statistical dataset. 
