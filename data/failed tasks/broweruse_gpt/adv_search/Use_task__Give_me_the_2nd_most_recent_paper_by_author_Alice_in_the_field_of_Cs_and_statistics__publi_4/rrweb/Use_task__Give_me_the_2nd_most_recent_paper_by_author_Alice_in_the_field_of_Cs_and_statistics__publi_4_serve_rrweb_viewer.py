import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser

def serve_files(directory, port=8001):
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('localhost', port), handler)
    print(f"Serving files from {directory} on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    directory_to_serve = os.path.dirname(__file__)
    rrweb_viewer_file = "Use_task__Give_me_the_2nd_most_recent_paper_by_author_Alice_in_the_field_of_Cs_and_statistics__publi_4_rrweb_viewer.html"
    print(f"Serving rrweb viewer: {rrweb_viewer_file}")
    webbrowser.open(f"http://localhost:8001/{rrweb_viewer_file}")
    serve_files(directory_to_serve)
    