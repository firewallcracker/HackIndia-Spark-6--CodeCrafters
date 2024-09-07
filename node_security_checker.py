import aiohttp
import asyncio
import ssl
import logging
from datetime import datetime
from requests.exceptions import RequestException
from aiohttp.client_exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create an SSL context for verifying certificates
def create_ssl_context():
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.check_hostname = True
    return context

# Function to check SSL certificate details
async def check_ssl_certificate(session, node_url):
    try:
        ssl_context = create_ssl_context()
        async with session.get(node_url, ssl=ssl_context, timeout=10) as response:
            cert_info = response.connection.transport._ssl_protocol._sslpipe.ssl_object.getpeercert()
            valid_from = datetime.strptime(cert_info['notBefore'], '%b %d %H:%M:%S %Y %Z')
            valid_to = datetime.strptime(cert_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
            issuer = cert_info.get('issuer')
            return {
                'ssl_certificate': 'Valid',
                'issuer': issuer,
                'valid_from': valid_from.strftime('%Y-%m-%d'),
                'valid_to': valid_to.strftime('%Y-%m-%d'),
            }
    except ssl.SSLError:
        return {'ssl_certificate': 'Invalid or Expired'}

# Function to fetch URL with async request and return data
async def fetch_node_data(node_url):
    async with aiohttp.ClientSession() as session:
        try:
            # Measure response time
            start_time = datetime.now()
            async with session.get(node_url, timeout=10) as response:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                # Collect basic data
                data = {
                    'url': node_url,
                    'response_time': f"{response_time:.2f} seconds",
                    'status': f"Node returned status code {response.status}",
                }

                # Check SSL certificate
                ssl_data = await check_ssl_certificate(session, node_url)
                data.update(ssl_data)

                # Rate limiting headers
                rate_limit_remaining = response.headers.get('X-RateLimit-Remaining', None)
                data['rate_limiting'] = f"Rate limit remaining: {rate_limit_remaining}" if rate_limit_remaining else "No rate limiting detected"

                # Common security headers
                security_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
                for header in security_headers:
                    data[header] = response.headers.get(header, "Not present")

                return data
        except ClientError as e:
            logging.error(f"Error fetching node data: {e}")
            return {'status': 'Failed to connect to the node', 'error': str(e)}

# Wrapper function for multiple nodes
async def check_multiple_nodes(node_urls):
    tasks = [fetch_node_data(url) for url in node_urls]
    results = await asyncio.gather(*tasks)
    return results

# Advanced Error Handling with Custom Exceptions
class NodeCheckError(Exception):
    def __init__(self, node_url, message="Error checking node"):
        self.node_url = node_url
        self.message = message
        super().__init__(self.message)

# Function to handle detailed SSL and Node checks
async def advanced_check_node_security(node_urls):
    try:
        results = await check_multiple_nodes(node_urls)
        return results
    except RequestException as e:
        raise NodeCheckError(node_urls, message=str(e))

# Main function
if __name__ == "__main__":
    node_urls = ["https://example.com", "https://example2.com"]

    # Run the advanced node check
    security_report = asyncio.run(advanced_check_node_security(node_urls))
    for report in security_report:
        print(report)


