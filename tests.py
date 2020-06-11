import unittest
import subprocess
import http.client
import os


class WebTestCase(unittest.TestCase):
    """tests for the echo server and client"""

    def setUp(self):
        self.server_process = subprocess.Popen(
            [
                "python",
                "http_server.py"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def tearDown(self):
        self.server_process.kill()
        self.server_process.communicate()

    def get_response(self, url):
        """
        Helper function to get a response from a given url, using http.client
        """

        conn = http.client.HTTPConnection('localhost:10000')
        conn.request('GET', url)

        response = conn.getresponse()

        conn.close()

        return response

    def test_post_yields_method_not_allowed(self):
        """
        Sending a POST request should yield a 405 Method Not Allowed response
        """

        conn = http.client.HTTPConnection('localhost:10000')
        conn.request('POST', '/')

        response = conn.getresponse()

        conn.close()

        # both .getcode() and .status can be used to check the response code.
        self.assertEqual(response.status, 405)
        #self.assertEqual(response.getcode(), 405)

    def test_get_sample_text_content(self):
        """
        A call to /sample.txt returns the correct body
        """
        file = 'sample.txt'

        local_path = os.path.join('webroot', *file.split('/'))
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        # response.read() will read the http response body.
        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_text_mime_type(self):
        """
        A call to /sample.txt returns the correct mimetype
        """
        file = 'sample.txt'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        # response.getheader(header_name) will return the value of the header name
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain', error_comment)

    def test_get_sample_scene_balls_jpeg(self):
        """
        A call to /images/Sample_Scene_Balls.jpg returns the correct body
        """
        file = 'images/Sample_Scene_Balls.jpg'

        local_path = os.path.join('webroot', *file.split('/'))
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_scene_balls_jpeg_mime_type(self):
        """
        A call to /images/Sample_Scene_Balls.jpg returns the correct mimetype
        """
        file = 'images/Sample_Scene_Balls.jpg'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'),
                         'image/jpeg', error_comment)

    def test_get_sample_1_png(self):
        """
        A call to /images/sample_1.png returns the correct body
        """
        file = 'images/sample_1.png'

        local_path = os.path.join('webroot', *file.split('/'))
        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)

        with open(local_path, 'rb') as f:
            self.assertEqual(f.read(), response.read(), error_comment)

    def test_get_sample_1_png_mime_type(self):
        """
        A call to /images/sample_1.png returns the correct mimetype
        """
        file = 'images/sample_1.png'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'), 'image/png', error_comment)

    def test_get_404(self):
        """
        A call to /asdf.txt (a file which does not exist in webroot) yields a 404 error
        """
        file = 'asdf.txt'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 404, error_comment)

    def test_images_index(self):
        """
        A call to /images/ yields a list of files in the images directory
        """

        directory = 'images'
        local_path = os.path.join('webroot', directory)
        web_path = '/' + directory
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)
        body = response.read().decode()

        for path in os.listdir(local_path):
            self.assertIn(path, body, error_comment)

    def test_root_index(self):
        """
        A call to / yields a list of files in the images directory
        """

        directory = ''
        local_path = os.path.join('webroot', directory)
        web_path = '/' + directory
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)
        body = response.read().decode()

        for path in os.listdir(local_path):
            self.assertIn(path, body, error_comment)

    def test_ok_response_at_root_index(self):
        """
        A call to / at least yields a 200 OK response
        """

        directory = ''
        web_path = '/' + directory

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200)

    def test_make_time_python_file(self):
        """
        A call to wobroot/make_time.py and execute the file and serve up the
        result of performing that execution.
        """
        file = 'make_time.py'

        web_path = '/' + file
        error_comment = "Error encountered while visiting " + web_path

        response = self.get_response(web_path)

        self.assertEqual(response.getcode(), 200, error_comment)
        self.assertEqual(response.getheader('Content-Type'),
                         'text/x-python', error_comment)
        # HTTPResponse.read() will read the response body in bytestring.
        self.assertIn('<http>', response.read().decode(), error_comment)


if __name__ == '__main__':
    unittest.main()
