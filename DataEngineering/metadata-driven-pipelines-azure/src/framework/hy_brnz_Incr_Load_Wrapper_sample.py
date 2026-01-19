#hy_brnz_Incr_Load_Wrapper.py


 Databricks notebook source
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing.pool import ThreadPool

# COMMAND ----------

# MAGIC %md
# MAGIC Deleting metadata entries for the previous run

# COMMAND ----------

# MAGIC %sql
# MAGIC delete from hy_ws_1.bronze.hy_load_control_brnz
# MAGIC ;
# MAGIC   

# COMMAND ----------

# MAGIC %sql
# MAGIC update hy_ws_1.bronze.hy_load_control_jde_incr 
# MAGIC set LOAD_TO_ADLS='False' 
# MAGIC where Load_Type = 'Increment'
# MAGIC ;

# COMMAND ----------

parallelism=7
list_of_list=[]
config_table='hy_ws_1.bronze.hy_load_control_jde_incr'
result=0
run_status=0
dbutils.widgets.text('Environment','prod')
environment=dbutils.widgets.get('Environment')
db_name='hy_ws_1.bronze'
adls='abfss://aftersales-parks@adlssynapsehy01.dfs.core.windows.net/src/db2l/abc'

# COMMAND ----------

from datetime import datetime, timedelta, timezone

try:
    table_to_run_list = [x['TABLENAME'] for x in spark.sql("select distinct TABLENAME from {} where LOAD_TO_ADLS='False' and SHOULD_RUN='Y' and LOAD_TYPE in ('Increment','Increment_rerun')".format(config_table)).collect()]
    table_to_run_list.sort()
except Exception as e:
    print(e)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raise Exception("Process Failure")

# COMMAND ----------

# Set up buckets of eligible tables with each bucket size limited by parallelism(default=3)
try:
  for i in range(0, len(table_to_run_list),parallelism): 
        list_of_list.append(table_to_run_list[i:i + parallelism])
#  list_of_list=list_of_list+[['measurement_value']]
except Exception as e:
  print("Exception : ",e)
  raise Exception(str(e))

# COMMAND ----------

print("Lists of tables to be processed separately:",list_of_list)
print("Lists of all tables available to be processed:",table_to_run_list)

# COMMAND ----------

# Function to pass to executor map to iterate over , one per tablenames
def run_adls_load_for_tables(tablename):
  try:
    result=dbutils.notebook.run(path = "/hy_Live/hy_Databricks/hy_Bi_jde_brnz_Incr_Load",
                                          timeout_seconds = 43200, 
                                          arguments = {"Environment":environment,
                                                       "Tablename":tablename})
    if result is None:
      ret_result= "{}:SUCCESS".format(tablename)
    elif result=='-2':
      ret_result= "{}:PARTIAL SUCCESS".format(tablename)
    else:
      ret_result= "{}:FAILED".format(tablename)
    return ret_result
  except Exception as e:
    raise Exception("{}:FAILED".format(tablename))

# COMMAND ----------

# Actual execution pass
error_count = 0
success_count=0
try:
  result_list=[]
  for table_list in list_of_list:
    print("Beginning execution of bucket:",table_list)
    with ThreadPoolExecutor() as executor:
        results = executor.map(run_adls_load_for_tables, table_list)
        result_list.append(list(results))
    print("Finished executing bucket {},moving to next if any left.".format(table_list))
    success_count+=1
  print(result_list)
except Exception as e:
  error_count+=1
  print("Exception : ",e)
  raise Exception("Failed")

# COMMAND ----------

# MAGIC %sql
# MAGIC --This update is for when there is a failuer in the bronze process we need to run the adjusted notebook
# MAGIC --After that to make the process reset we need to perform below update.
# MAGIC update hy_ws_1.bronze.hy_load_control_jde_incr 
# MAGIC set Load_Type = 'Increment'
# MAGIC where Load_Type = 'Increment_rerun'
# MAGIC ;