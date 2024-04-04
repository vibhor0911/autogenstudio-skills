from optparse import Option
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
import json
import datetime

# Create an instance of the DefaultAzureCredential class, which will authenticate
# using environment variables, managed identity, or Azure CLI credentials.
credential = DefaultAzureCredential(managed_identity_client_id='')

# Create an instance of the LogsQueryClient class, which allows you to run KQL queries
# against the Application Insights workspace.
client = LogsQueryClient(credential)

# Specify the KQL query you want to run.
query =  """workspace('').dnstatechanged_CL
| where agentState_s == "LoggedOut" and agentId_s !contains "availability" and agentId_s <> "OTHER"
| summarize LogOuts = count() by bin(eventTime_t,30min),agentId_s
| where LogOuts >5
"""

# Specify the time range for the query (e.g., last 7 days).
duration = timedelta(days=7)

# Run the query and get the results.
results = client.query_workspace(
    workspace_id="",
    query=query,
    timespan=duration
)

data = []
for table in results.tables:
    for row in table.rows:
        data.append(dict(zip(table.columns, row)))

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

json_data = json.dumps(data, cls=DateTimeEncoder)

# Print the formatted JSON object
print(json_data)
