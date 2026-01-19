#This is sample code what I got
# Databricks notebook source
#Defining variables
dbutils.widgets.text('Environment','prod')
dbutils.widgets.text('Tablename','src_table')

#Assigning values to the variables
environment=dbutils.widgets.get('Environment')
Tablename=dbutils.widgets.get('Tablename')

# COMMAND ----------

adls='abfss://adlssynapse-bi@adlssynapseyaumi01.dfs.core.windows.net'
adls_file=adls+'/raw/PBI_Source_UC/'+Tablename+'/'
adls_table=adls+'/databases/bronze/'
db_name='yaumi_bi_prod.bronze'

# COMMAND ----------

from datetime import datetime, timedelta, timezone
from delta.tables import *
from pyspark.sql.functions import lower

run_status=0
try:
  list_of_tables=Tablename
  for i in range(1) :
     table1=list_of_tables
     table=list_of_tables.lower()
     file=table+'.parquet'
     path=adls+'databases/bronze/'+table
     start_time= datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")
     try:
       table_exists=False
       pre_loadcount=spark.sql("select count(*) as cnt from {}".format(db_name+'.'+table)).first().cnt
       print("Pre Load Record Count:",pre_loadcount)
       if pre_loadcount>=0:
         table_exists=True
         print('Merging {} table'.format(table))
         df=spark.read.format('Parquet').option('header',True).option('inferschema',True).option('escape','"').option('multiLine','true').load(adls_file)
         df = df.repartition(32)
         print("Source File Count:", df.count())
         df.write.format('delta').mode('overwrite').option('overwriteSchema',True).saveAsTable(db_name+'.'+table)
         post_load_count=spark.sql('select count(*) as cnt from {}.{}'.format(db_name,table)).first().cnt
         end_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")
         print('pre_load count={}'.format(pre_loadcount))
         print('post_load count={}'.format(post_load_count))
         print("Records  were merged into {} table successfully".format(table1))
         
     except Exception as e:
       if not table_exists:
         print('Create and append {} table'.format(table))
         df=spark.read.format('Parquet').option('header',True).option('inferschema',True).option('escape','"').option('multiLine','true').load(adls_file+file)
         df = df.repartition(32)
         df.write.format('delta').mode('overwrite').option('overwriteSchema',True).saveAsTable(db_name+'.'+table)         
         end_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")
         post_load_count=spark.sql('select count(*) as cnt from {}.{}'.format(db_name,table)).first().cnt
         print("Table not exist created and loaded for {} table with {} records".format(table,post_load_count))

     print('Updated Start and end date in load control')
     post_load_count1=spark.sql('select count(*) as cnt from {}.{}'.format(db_name,table)).first().cnt     
     spark.sql('insert into {}.yaumi_load_control_brnz values("{}","{}","{}")'.format(db_name,table1,start_time,post_load_count1))
except Exception as e:
  print(e)
  run_status=-1
  time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")