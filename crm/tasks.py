from celery import shared_task
from datetime import datetime
from graphene_django.settings import graphene_settings
from graphql import graphql_sync

@shared_task
def generate_crm_report():
    schema = graphene_settings.SCHEMA

    query = '''
    {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
            totalRevenue: edges {
                node {
                    totalamount
                }
            }
        }
    }
    '''

    result = graphql_sync(schema, query)

    customers = result.data['allCustomers']['totalCount']
    orders = result.data['allOrders']['totalCount']
    revenue = sum(float(order['node']['totalamount']) for order in result.data['allOrders']['totalRevenue'])

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(report)
