#!/usr/bin/env python3

import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # GraphQL query: get orders within last 7 days
    query = gql(
        """
        query GetRecentOrders($startDate: DateTime!) {
          orders(filter: {order_date_gte: $startDate}) {
            edges {
              node {
                id
                customer {
                  email
                }
                order_date
              }
            }
          }
        }
        """
    )
    
    # Calculate date 7 days ago in ISO format
    from datetime import datetime, timedelta
    start_date = (datetime.utcnow() - timedelta(days=7)).isoformat()

    params = {"startDate": start_date}
    
    # Execute query
    result = client.execute(query, variable_values=params)
    orders = result.get("orders", {}).get("edges", [])
    
    # Open log file in append mode
    with open(LOG_FILE, "a") as f:
        for order_edge in orders:
            order = order_edge.get("node")
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            log_line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Order ID: {order_id}, Customer Email: {email}\n"
            f.write(log_line)
    
    print("Order reminders processed!")

if __name__ == "__main__":
    main()
