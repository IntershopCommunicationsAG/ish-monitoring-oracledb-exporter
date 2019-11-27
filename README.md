# ISH-Monitoring-OracleDB Prometheus Exporter
Oracle Exporter for Prometheus in python. Metrics are scraped by scheduler, and the interval is configurable via environment variable


## Integration
Run `docker-compose up`. When the image is not build yet, please run `docker-compose up --build`

After launching up, metrics show up in `http://localhost:8000/metrics`,
by using promql `{__name__=~".+",job="prometheusOracleExporter"}`

To rebuild the image please run `docker-compose up --build`

## Setting up

##### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Learn more in [the documentation](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

Note: if you are using a python before 3.3, it doesn't come with venv. Install [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) with pip instead.

##### (If you're on a Mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Set Environment Variables

Please check `config.py`. `config.py` describes the environment, and
by setting `FLASK_CONFIG`  you can decide which environment to pick up, e.g.

`FLASK_CONFIG=config.TestingConfig`

or

`FLASK_CONFIG=config.DevelopmentConfig`

or

`FLASK_CONFIG=config.ProductionConfig`

## Running the app

```
$ source env/bin/activate
$ python3 manage.py runserver
```

## Formatting code

Before you submit changes, you may want to autoformat your code with `python manage.py format`.

## Development
Add new Metrics by extending `AbstractMetric`,
under `app/prom/metrics`, either `general`, which is related to system
or `business` that is related to business logic.

Check existing examples and the tests before adding them.

Before implementing a metric please go through the tips that ensure you
follow the [official guideline](https://prometheus.io/docs/practices/instrumentation/#things-to-watch-out-for)

In general the rules are:
#### Labels
- Use labels when required to aggregate the metrics, e.g. http status code should be one metrics with several labels(200, 400, 500)
- Do not use labels when cardinality is more than 100 and will increase more in the future

#### Existing metrics
```
# HELP oracledb_asm_diskgroup_total Total size of ASM disk group.
# TYPE oracledb_asm_diskgroup_total gauge
# HELP oracledb_asm_diskgroup_free Free space available on ASM disk group.
# TYPE oracledb_asm_diskgroup_free gauge
# HELP oracledb_cachehitratio Gauge metric witch Cache hit ratios (v$sysmetric).
# TYPE oracledb_cachehitratio gauge
oracledb_cachehitratio{type="buffer_cache_hit_ratio"} 99.6130407366754
oracledb_cachehitratio{type="cursor_cache_hit_ratio"} 53.1749969825794
oracledb_cachehitratio{type="row_cache_hit_ratio"} 97.8026327857615
oracledb_cachehitratio{type="library_cache_hit_ratio"} 94.5670141852013
# HELP oracledb_interconnect Gauge metric with interconnect block transfers (v$sysstat).
# TYPE oracledb_interconnect gauge
oracledb_interconnect{name="gc_cr_blocks_served"} 0.0
oracledb_interconnect{name="gc_cr_blocks_received"} 0.0
# HELP oracledb_process_count Gauge metric with count of processes.
# TYPE oracledb_process_count gauge
oracledb_process_count 223.0
# HELP oracledb_recovery_percent_space_used Generic counter metric of tablespaces bytes in Oracle.
# TYPE oracledb_recovery_percent_space_used gauge
oracledb_recovery_percent_space_used 0.0
# HELP oracledb_recovery_percent_space_reclaimable Generic counter metric of tablespaces bytes in Oracle.
# TYPE oracledb_recovery_percent_space_reclaimable gauge
oracledb_recovery_percent_space_reclaimable 0.0
# HELP oracledb_redo_log_switches Gauge metric with Redo log switches over last 5 min (v$log_history).
# TYPE oracledb_redo_log_switches gauge
oracledb_redo_log_switches 0.0
# HELP oracledb_resource_current_utilization Generic counter metric from v$resource_limit view in Oracle (current value).
# TYPE oracledb_resource_current_utilization gauge
oracledb_resource_current_utilization{resource_name="processes"} 223.0
oracledb_resource_current_utilization{resource_name="sessions"} 177.0
oracledb_resource_current_utilization{resource_name="enqueue_locks"} 153.0
oracledb_resource_current_utilization{resource_name="enqueue_resources"} 49.0
oracledb_resource_current_utilization{resource_name="ges_procs"} 0.0
oracledb_resource_current_utilization{resource_name="ges_ress"} 0.0
oracledb_resource_current_utilization{resource_name="ges_locks"} 0.0
oracledb_resource_current_utilization{resource_name="ges_cache_ress"} 0.0
oracledb_resource_current_utilization{resource_name="ges_reg_msgs"} 0.0
oracledb_resource_current_utilization{resource_name="ges_big_msgs"} 0.0
oracledb_resource_current_utilization{resource_name="ges_rsv_msgs"} 0.0
oracledb_resource_current_utilization{resource_name="gcs_resources"} 0.0
oracledb_resource_current_utilization{resource_name="gcs_shadows"} 0.0
oracledb_resource_current_utilization{resource_name="smartio_overhead_memory"} 0.0
oracledb_resource_current_utilization{resource_name="smartio_buffer_memory"} 0.0
oracledb_resource_current_utilization{resource_name="smartio_metadata_memory"} 0.0
oracledb_resource_current_utilization{resource_name="smartio_sessions"} 0.0
oracledb_resource_current_utilization{resource_name="dml_locks"} 5.0
oracledb_resource_current_utilization{resource_name="temporary_table_locks"} 0.0
oracledb_resource_current_utilization{resource_name="transactions"} 5.0
oracledb_resource_current_utilization{resource_name="branches"} 0.0
oracledb_resource_current_utilization{resource_name="cmtcallbk"} 59.0
oracledb_resource_current_utilization{resource_name="max_rollback_segments"} 71.0
oracledb_resource_current_utilization{resource_name="sort_segment_locks"} 16.0
oracledb_resource_current_utilization{resource_name="k2q_locks"} 0.0
oracledb_resource_current_utilization{resource_name="max_shared_servers"} 1.0
oracledb_resource_current_utilization{resource_name="parallel_max_servers"} 66.0
# HELP oracledb_resource_limit_value Generic counter metric from v$resource_limit view in Oracle (limit value).
# TYPE oracledb_resource_limit_value gauge
oracledb_resource_limit_value{resource_name="processes"} 3000.0
oracledb_resource_limit_value{resource_name="sessions"} 4528.0
oracledb_resource_limit_value{resource_name="enqueue_locks"} 52140.0
oracledb_resource_limit_value{resource_name="ges_procs"} 0.0
oracledb_resource_limit_value{resource_name="ges_rsv_msgs"} 0.0
oracledb_resource_limit_value{resource_name="max_rollback_segments"} 65535.0
oracledb_resource_limit_value{resource_name="parallel_max_servers"} 32767.0
# HELP oracledb_sessions Gauge metric with count of sessions by status and type.
# TYPE oracledb_sessions gauge
oracledb_sessions{status="ACTIVE",type="BACKGROUND"} 43.0
oracledb_sessions{status="INACTIVE",type="USER"} 109.0
oracledb_sessions{status="ACTIVE",type="USER"} 4.0
# HELP oracledb_sysmetric Gauge metric with read/write pysical IOPs/bytes (v$sysmetric).
# TYPE oracledb_sysmetric gauge
oracledb_sysmetric{type="physical_read_total_io_requests_per_sec"} 79.3373293373293
oracledb_sysmetric{type="physical_read_total_bytes_per_sec"} 1.67923383283383e+06
oracledb_sysmetric{type="physical_write_total_io_requests_per_sec"} 187.828837828838
oracledb_sysmetric{type="physical_write_total_bytes_per_sec"} 3.41353792873793e+06
# HELP oracledb_tablespace_bytes Generic counter metric of tablespaces bytes in Oracle.
# TYPE oracledb_tablespace_bytes gauge
oracledb_tablespace_bytes{tablespace="SYSAUX",type="PERMANENT"} 5.0289688576e+010
oracledb_tablespace_bytes{tablespace="UNDOTBS1",type="UNDO"} 1.2582912e+010
oracledb_tablespace_bytes{tablespace="IS_USERS",type="PERMANENT"} 6.4399343616e+010
oracledb_tablespace_bytes{tablespace="SYSTEM",type="PERMANENT"} 5.24288e+09
oracledb_tablespace_bytes{tablespace="IS_INDX",type="PERMANENT"} 4.5726302208e+010
oracledb_tablespace_bytes{tablespace="IS_INDX_CTX",type="PERMANENT"} 1.2335448064e+010
oracledb_tablespace_bytes{tablespace="TEMP",type="TEMPORARY"} 1.048576e+09
oracledb_tablespace_bytes{tablespace="IS_TEMP",type="TEMPORARY"} 1.493172224e+09
# HELP oracledb_tablespace_max_bytes Generic counter metric of tablespaces max bytes in Oracle.
# TYPE oracledb_tablespace_max_bytes gauge
oracledb_tablespace_max_bytes{tablespace="SYSAUX",type="PERMANENT"} 6.8719443968e+010
oracledb_tablespace_max_bytes{tablespace="UNDOTBS1",type="UNDO"} 3.4359721984e+010
oracledb_tablespace_max_bytes{tablespace="IS_USERS",type="PERMANENT"} 3.4359721984e+011
oracledb_tablespace_max_bytes{tablespace="SYSTEM",type="PERMANENT"} 3.4359721984e+010
oracledb_tablespace_max_bytes{tablespace="IS_INDX",type="PERMANENT"} 2.06158331904e+011
oracledb_tablespace_max_bytes{tablespace="IS_INDX_CTX",type="PERMANENT"} 1.7179860992e+011
oracledb_tablespace_max_bytes{tablespace="TEMP",type="TEMPORARY"} 3.4359721984e+010
oracledb_tablespace_max_bytes{tablespace="IS_TEMP",type="TEMPORARY"} 1.37438887936e+011
# HELP oracledb_tablespace_free Generic counter metric of tablespaces free bytes in Oracle.
# TYPE oracledb_tablespace_free gauge
oracledb_tablespace_free{tablespace="SYSAUX",type="PERMANENT"} 1.31006464e+09
oracledb_tablespace_free{tablespace="UNDOTBS1",type="UNDO"} 7.663976448e+09
oracledb_tablespace_free{tablespace="IS_USERS",type="PERMANENT"} 5.8916143104e+010
oracledb_tablespace_free{tablespace="SYSTEM",type="PERMANENT"} 9.45225728e+08
oracledb_tablespace_free{tablespace="IS_INDX",type="PERMANENT"} 3.9500644352e+010
oracledb_tablespace_free{tablespace="IS_INDX_CTX",type="PERMANENT"} 1.1578441728e+010
oracledb_tablespace_free{tablespace="TEMP",type="TEMPORARY"} 1.047527424e+09
oracledb_tablespace_free{tablespace="IS_TEMP",type="TEMPORARY"} 1.461714944e+09
# HELP oracledb_uptime Gauge metric with uptime in days of the Instance.
# TYPE oracledb_uptime gauge
oracledb_uptime 185.09552083333332
# HELP oracledb_up Oracle UP status
# TYPE oracledb_up gauge
oracledb_up 1.0
# HELP oracledb_activity_user_commits Generic counter metric from v$sysstat view in Oracle.
# TYPE oracledb_activity_user_commits gauge
oracledb_activity_user_commits 3.52355691e+08
# HELP oracledb_activity_user_rollbacks Generic counter metric from v$sysstat view in Oracle.
# TYPE oracledb_activity_user_rollbacks gauge
oracledb_activity_user_rollbacks 6.821281e+06
# HELP oracledb_activity_parse_count_total Generic counter metric from v$sysstat view in Oracle.
# TYPE oracledb_activity_parse_count_total gauge
oracledb_activity_parse_count_total 1.2732315284e+010
# HELP oracledb_activity_execute_count Generic counter metric from v$sysstat view in Oracle.
# TYPE oracledb_activity_execute_count gauge
oracledb_activity_execute_count 4.6199268828e+010
# HELP oracledb_wait_time_other Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_other gauge
oracledb_wait_time_other 0.837
# HELP oracledb_wait_time_application Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_application gauge
oracledb_wait_time_application 0.056
# HELP oracledb_wait_time_configuration Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_configuration gauge
oracledb_wait_time_configuration 0.001
# HELP oracledb_wait_time_administrative Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_administrative gauge
oracledb_wait_time_administrative 0.0
# HELP oracledb_wait_time_concurrency Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_concurrency gauge
oracledb_wait_time_concurrency 0.016
# HELP oracledb_wait_time_commit Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_commit gauge
oracledb_wait_time_commit 0.544
# HELP oracledb_wait_time_network Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_network gauge
oracledb_wait_time_network 0.002
# HELP oracledb_wait_time_user_io Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_user_io gauge
oracledb_wait_time_user_io 0.683
# HELP oracledb_wait_time_system_io Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_system_io gauge
oracledb_wait_time_system_io 1.559
# HELP oracledb_wait_time_scheduler Generic counter metric from v$waitclassmetric view in Oracle.
# TYPE oracledb_wait_time_scheduler gauge
oracledb_wait_time_scheduler 0.0
```

### Build and Push

```
 docker build -t intershopde/ish-monitoring-oracledb-exporter:latest .
 docker push intershopde/ish-monitoring-oracledb-exporter:latest
```