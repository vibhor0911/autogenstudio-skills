import requests
import json
import logging

# Configuration for ICM cluster
BEARER_TOKEN = ""
API_ENDPOINT = f"url"

def fetch_incident_details(incident_id):
    """
    Fetches incident details from the ICM cluster.
    
    Parameters:
    - incident_id (int): The incident ID for fetching details.
    
    Returns:
    - A JSON object containing the incident details.
    """
    headers = {
        'Authorization': BEARER_TOKEN,
        'Content-type':'application/json; charset=UTF-8', 
        'Accept':'application/json'
    }
    params = {
        "db": "IcmDataWarehouse",
        "csl": f"Incidents| join kind=inner  (IncidentDescriptions    | summarize Discussion = make_list(Text) by IncidentId) on IncidentId| where OwningTenantName == 'SxG Core 3P Genesys'| where IncidentId == {incident_id}| project IncidentId, Title, Summary, Discussion, Severity, Status, ModifiedDate| order by ModifiedDate desc nulls last| limit 1",
        "properties": {
            "Options": {
                "servertimeout": "00:04:00",
                "queryconsistency": "strongconsistency",
                "query_language": "csl",
                "request_readonly": False,
                "request_readonly_hardline": False
            }
        }
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=params)
        if response.ok:
            return format_result(response.json())
        else:
            logging.error(f"Failed to fetch incident details. Response: {response.text}")
            return "Failed to fetch incident details."
    except Exception as e:
        logging.exception(f"An error occurred while fetching incident details: {str(e)}")
        return f"An error occurred while fetching incident details: {str(e)}"

def format_result(query_result):
    """
    Formats the query result to extract relevant data.
    
    Parameters:
    - query_result (JSON): The JSON object containing the query result.
    
    Returns:
    - A formatted JSON object containing the extracted data.
    """
    formatted_data = {}
    
    for frame in query_result:
        if frame["FrameType"] == "DataTable" and frame["TableName"] == "PrimaryResult":
            columns = [column["ColumnName"] for column in frame["Columns"]]
            for row in frame["Rows"]:
                row_data = {}
                for col, value in zip(columns, row):
                    row_data[col] = value
                formatted_data["result"] = row_data
    
    return json.dumps(formatted_data, indent=4)

# Example incident ID - Replace with your actual incident ID
incident_id = 489412872
# Execute the API call
query_result = fetch_incident_details(incident_id)
# Print the result
print(query_result)
