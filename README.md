# 🏠 Sensor Window Duration Analysis: A Comparison of Hadoop MapReduce and Spark Approaches

This project analyzes and computes the average window duration for each sensor location based on smart home sensor logs. The goal is to understand space utilization and user behavior by determining how long sensors remain active in different areas of the home. The analysis is conducted using two approaches:  
➤ a Hadoop MapReduce pipeline (via Hadoop Streaming on AWS EC2) and  
➤ a non-MapReduce method using Apache Spark.

We aim to compare both methods in terms of implementation and output while processing a large dataset efficiently.

---

## 📂 Files in this Repo

- data preprocessing.ipynb : Data preprocessing script
- mapper.py : Python mapper script  
- reducer.py : Python reducer script  
- spark.py : Spark-based analysis script  
- README.md : Project overview and full execution instructions

---

## 📁 Dataset

This project uses smart home sensor log data sourced from the UCI Machine Learning Repository:  

🔗 [Human Activity Recognition from Continuous Ambient Sensor Data (UCI)](https://archive.ics.uci.edu/dataset/506/human+activity+recognition+from+continuous+ambient+sensor+data)  

- **Original File Name:** `csh102.rawdata.features`  
- **File Size:** ~1.6 GB  
- **Total Records:** 6,472,309 rows  

Due to GitHub’s 25MB file size limit, the cleaned dataset used in this project has been hosted externally:  

🔗 [Download `sensor_duration_cleaned.csv` (Dropbox)](https://www.dropbox.com/scl/fi/8m8pbrw0nmylh10n7efqt/sensor_duration_cleaned.csv?rlkey=ryxu0ia6we8imo97dycq5304i&st=ta0tygsd&dl=1)  

The cleaned version contains only the relevant columns used for analysis:  

- `lastSensorLocation` → Encoded identifier for the last activated sensor location in the home  
- `windowDuration` → Duration (in seconds) the sensor remained active during the time window  


## 📘 Full Execution Guide (Hadoop MapReduce Approach)

### 📥 Download the dataset on EC2

```bash
wget "https://www.dropbox.com/scl/fi/8m8pbrw0nmylh10n7efqt/sensor_duration_cleaned.csv?rlkey=ryxu0ia6we8imo97dycq5304i&st=54t4tyaj&dl=1" -O sensor_duration_cleaned.csv
```

### 📤 Upload to HDFS

```bash
hdfs dfs -rm -r /user/hadoop/sensordata
hdfs dfs -mkdir -p /user/hadoop/sensordata
hdfs dfs -put sensor_duration_cleaned.csv /user/hadoop/sensordata/
```

### 🧾 Mapper Script (mapper.py)

```python
#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        fields = next(csv.reader([line]))
        location = fields[0].strip()
        duration = float(fields[1].strip())
        print(f"{location}\t{duration}")
    except:
        continue
```

### 🧾 Reducer Script (reducer.py)

```python
#!/usr/bin/env python3
import sys

current_key = None
total_duration = 0
count = 0

print("SensorLocation\tAverageDuration")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key, value = line.split("\t")
        value = float(value)
    except:
        continue

    if key == current_key:
        total_duration += value
        count += 1
    else:
        if current_key is not None:
            print(f"{current_key}\t{round(total_duration / count, 2)}")
        current_key = key
        total_duration = value
        count = 1

if current_key:
    print(f"{current_key}\t{round(total_duration / count, 2)}")
```

### ▶️ Run the MapReduce Job

```bash
hadoop jar /home/hadoop/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /user/hadoop/sensordata/sensor_duration_cleaned.csv \
  -output /user/hadoop/output_sensor_avg \
  -mapper ./mapper.py \
  -reducer ./reducer.py \
  -file mapper.py \
  -file reducer.py
```

### 📄 View the Output

```bash
hdfs dfs -cat /user/hadoop/output_sensor_avg/part-00000 | column -t
```

---

## ⚡ Full Execution Guide (Apache Spark Approach)

### 📄 Spark Script (sensor_avg_spark.py)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

# 1. Start Spark
spark = SparkSession.builder.appName("SensorAverageDuration").getOrCreate()

# 2. Read CSV
df = spark.read.csv("sensor_duration_cleaned.csv", header=False, inferSchema=True)

# 3. Rename columns
df = df.withColumnRenamed("_c0", "SensorLocation") \
       .withColumnRenamed("_c1", "WindowDuration")

# 4. Group by SensorLocation and calculate average
result = df.groupBy("SensorLocation") \
           .agg(
               count("*").alias("Count"),
               avg("WindowDuration").alias("AverageDuration")
           ) \
           .orderBy("SensorLocation")

# 5. Show the results
result.show(truncate=False)

# Optional: save to output file
# result.coalesce(1).write.csv("sensor_output_spark", header=True)

# 6. Stop Spark
spark.stop()
```

### ▶️ Run the Spark Script

```bash
spark-submit spark.py
```

---

## 📈 Sample Output

MapReduce:

```
SensorLocation   Count    AverageDuration
0                179924   111.69
1                168927   578.49
3                46160    243.15
..               ..       ..
```

Spark:

```
+---------------+----------------+-----------------------+
|SensorLocation |Count           |AverageDuration        |
+---------------+----------------+-----------------------+
|0              |179924          |111.6902469931749      | 
|1              |168927          |578.4855351719974      |  
|3              |46160           |243.15259965337955     |
|..             |..              |..                     |
+---------------+----------------+-----------------------+
```

## 👥 Group Members

| Name                               | Student ID |
|------------------------------------|------------|
| Kok Yi Shuen                       | 22027288   |
| Ee Xie Wen                         | 21032362   |
| Siobhan Goh Shze Mun Su            | 22002570   |

