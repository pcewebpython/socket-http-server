# SOCKET HTTP SERVER

Once you're done, you should be able to start the web server inside the homework directory using `python -u http_server.py` and then point your web browser at locations like:
  * http://localhost:10000/sample.txt
  * http://localhost:10000/a_web_page.html
  * http://localhost:10000/images/sample_1.png

and see the corresponding file located under homework/webroot. Take a moment to look into the homework/webroot and see these files. 

Inside this repository you'll find the http_server.py file. I've added enough stub code for the missing functions to let the server run. And there are more tests for you to make pass!

You do NOT need to execute the `make_time.py` Python file. When a web user visits `http://localhost:1000/make_time.py` you only need to _serve up_ the contents of that file. But if you'd like to take on a challenge, then you _can_ choose to execute the file and serve up the result of performing that execution.


## Building the Response

Your `response_path` function will need to accomplish the following tasks:

  * It should take a URI as the sole argument
  * It should map the pathname represented by the URI to a filesystem location.
  * It should have a ‘home directory’, and look only in that location.
  * If the URI is a directory, it should return a plain-text listing of the directory contents and the mimetype text/plain.
  * If the URI is a file, it should return the contents of that file and its correct mimetype.
  * If the URI does not map to a real location, it should raise an exception that the server can catch to return a 404 response.

Because your server will be transmitting files as bytes, you might want to try searching for "reading a file as bytes in Python".

To find the correct mimetype for a file, you might find the following code helpful:

```
>>> import mimetypes
>>> mimetypes.guess_type('file.txt')[0]
    'text/plain'
>>> mimetypes.types_map['.txt']
    'text/plain'
```

## Hints

* Your `response_path` method is going to be looking at the incoming path and checking whether the path represents a directory, a file, or none of the above. There are relevant methods in the [os.path](https://docs.python.org/3/library/os.path.html) module.
* To complete the assignment, you'll have to get a list of files inside of a directory and then turn that list into a bytestring. There's a method inside of [the os module](https://docs.python.org/3/library/os.html) that can help you address the first part of that problem. You'll then have to turn that list into a string and then a byte-string using techniques you've learned in this class and previous classes.
* Finally, your `response_path` method will be receiving `path` arguments such as "/a_sample_page.html". Suppose that you are running your server with the command `python http_server.py` from inside the `socket-http-server` directory. Then if you have expressions like `os.path.isfile(path)` in your `response_path` method, these will be looking for a file named "a_sample_page.html" inside of your `socket-http-server` directory. That file **doesn't exist**: the "a_sample_page.html" exists inside of the `webroot` directory. So as you're writing your `response_path` method, you're going to have to somehow modify the `path` variable to make python look for files _inside_ of the `webroot` directory.

## Use Your Tests

As you work your way through the steps outlined above, look at your tests. Write code that makes them pass.

There are integration tests that you can run with `python tests.py` and unit tests that you can run with `python unit-tests.py`. The unit tests test everything except for the server method.

You may find it helpful to work through the homework using either or both sets of tests. If you're not sure how to proceed, it may be easier to begin by running the unit tests and trying to make them pass one at a time.

