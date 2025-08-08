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