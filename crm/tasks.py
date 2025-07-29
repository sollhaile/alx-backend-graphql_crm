from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        allCustomers {
            edges { node { id } }
        }
        allOrders {
            edges { node { totalAmount } }
        }
    }
    """)

    try:
        result = client.execute(query)
        total_customers = len(result["allCustomers"]["edges"])
        orders = result["allOrders"]["edges"]
        total_orders = len(orders)
        total_revenue = sum(float(order["node"]["totalAmount"]) for order in orders)

        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue\n")
    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(f"{timestamp} - Error: {str(e)}\n")
