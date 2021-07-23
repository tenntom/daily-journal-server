from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from entries import get_all_entries, get_single_entry, create_entry, delete_entry, update_entry, search_entry

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists
            except ValueError:
                pass  # Request had trailing slash

            return (resource, id)

    def _set_headers(self, status):
        """
        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server"""
        self._set_headers(200)
        response = {}  # Default response

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

        # It's an if..else statement
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"

            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = get_all_moods()

            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tags(id)}"
                else:
                    response = get_all_tags()
            else:
                response = []

        # elif len(parsed) == 3:
        #     (resource, key, value) = parsed

        #     if key == "email" and resource == "customers":
        #         response = get_customers_by_email(value)

        self.wfile.write(f"{response}".encode())


    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, _) = self.parse_url(self.path)

        # Initialize new response
        response = None

        # function next.
        if resource == "entries":
            response = create_entry(post_body)
        elif resource == "moods":
            response = create_mood(post_body)
        elif resource == "moods":
            response = create_mood(post_body)
  
        # Encode the new item and send in response
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Update a single item
        if resource == "entries":
            success = update_entry(id, post_body)
        if resource == "moods":
            success = update_mood(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single object from the list
        if resource == "entries":
            delete_entry(id)
        if resource == "moods":
            delete_mood(id)

        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
