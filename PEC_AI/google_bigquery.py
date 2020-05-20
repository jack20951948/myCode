from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame

# Explicitly use service account credentials by specifying the private
# key file. All clients in google-cloud-python have this helper.
client = bigquery.Client.from_service_account_json(
    'PEC_AI/pec-project-c53f0019611e.json')

df_data = DataFrame()
for i in range(2008, 2018):
    query_string = 'SELECT * FROM test1.BN_{} LIMIT 100'.format(i)
    query_job = client.query(query_string)

    tamp_df_data = query_job.result().to_dataframe()
    tamp_df_data.insert(3, 'year', i)
    df_data = df_data.append(tamp_df_data)

# Print the results.
print(df_data)

############################################################

schema = [
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("gender", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("year", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("__index_level_0__", "INTEGER", mode="NULLABLE"),
]

# TODO(developer): Construct a BigQuery client object.
# client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create
table_id = "pec-project-240211.test1.BN_2008_2017"

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # API request
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)

dataset_ref = client.dataset('test1')
table_ref = dataset_ref.table('BN_2008_2017')

client.load_table_from_dataframe(df_data, table_ref).result()

# Print the results.
