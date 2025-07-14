import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Append heartbeat log
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")

    # Optional: GraphQL "hello" query for health check
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        print(f"GraphQL response: {result}")
    except Exception as e:
        print(f"GraphQL health check failed: {e}")
