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


def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    updatedProducts {
                        name
                        stock
                    }
                }
            }
        """)

        response = client.execute(mutation)

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"[{timestamp}] {response['updateLowStockProducts']['success']}\n")
            for product in response['updateLowStockProducts']['updatedProducts']:
                f.write(f"- {product['name']}: stock = {product['stock']}\n")

    except Exception as e:
        print(f"Error updating low stock: {e}")
