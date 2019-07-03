import unittest
import os
import http_server


class TestCase(unittest.TestCase):

    def test_response_ok(self):
        mimetype = b"image/bmp"
        body = b"foo"

        response = http_server.response_ok(body=body, mimetype=mimetype)
        str_response = response.decode()

        self.assertIn("\r\n\r\n", str_response)

        str_header, str_body = str_response.split("\r\n\r\n")

        self.assertEqual(body.decode(), str_body)
        self.assertEqual("HTTP/1.1 200 OK",
                         str_header.splitlines()[0])
        self.assertIn("Content-Type: " + mimetype.decode(), str_header)

    def test_response_method_not_allowed(self):
        response = http_server.response_method_not_allowed()
        str_response = response.decode()

        self.assertEqual("HTTP/1.1 405 Method Not Allowed",
                         str_response.splitlines()[0])

    def test_response_not_found(self):
        response = http_server.response_not_found()
        str_response = response.decode()

        self.assertEqual("HTTP/1.1 404 Not Found",
                         str_response.splitlines()[0])

    def test_parse_request_bad_method(self):
        request_head = "POST /foo HTTP/1.1"

        with self.assertRaises(NotImplementedError):
            http_server.parse_request(request_head)

    def test_parse_request(self):
        path = "/foo"
        request_head = "GET {} HTTP/1.1".format(path)

        self.assertEqual(path, http_server.parse_request(request_head))

    def test_response_path_file(self):
        path = "/a_web_page.html"

        content, mime_type = http_server.response_path(path)

        self.assertEqual(b"text/html", mime_type)
        
        with open(os.path.join("webroot", "a_web_page.html"), "rb") as f:
            self.assertEqual(f.read(), content)

    def test_response_path_dir(self):
        path = "/"

        content, mime_type = http_server.response_path(path)

        self.assertIn(b"favicon.ico", content)
        self.assertIn(b"make_time.py", content)
        self.assertIn(b"sample.txt", content)
        self.assertIn(b"a_web_page.html", content)

    def test_response_path_not_found(self):
        path = "/foo/bar/baz/doesnt/exist"

        with self.assertRaises(NameError):
            http_server.response_path(path)


if __name__ == '__main__':
    unittest.main()
