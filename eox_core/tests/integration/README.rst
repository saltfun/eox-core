Running
=======

You can run the tests using the make target

.. code-block:: console

    $ make python-test

This test make several assumptions about the current state of the database
in case your setup differs you will have to modify ``data.json`` accordingly.

Data requirements
-----------------
The data.json file includes data necessary to run each test. It's content
must reflect the current database configuration of the platform you
are running the tests. The provided file is meant to run on a devstack
enviroment with the following requirements:

- There should be an DOT application with client_id ``apiclient`` and
  client_secret ``apisecret``
- There should be a user with username ``honor`` and email ``honor@example.com``
- There should be a course with id ``course-v1:edX+DemoX+Demo_Course``
- There user ``honor`` should be enrolled on the course
  ``"course-v1:edX+DemoX+Demo_Course``, the flag is_active should be ``true``,
  and the course mode should be ``audit``

Each test is performed sequentially ensuring that all CRUD operations are
performed successfully. In particular, CREATE and DELETE are dependant on each
other (the default enrollment is deleted and then created again), if one of those
were to fail the rest of the tests will probably fail too. In a similar vain,
the UPDATE operation is performed twice where the second one assumes the first one
was successful.

This behaviour can be changed by altering the data.json file, you must ensure a way
to restore de initial layout of the data in your DB, otherwise subsequent runs will
fail.


Current Tests
-------------

There are 8 tests making a GET, POST, PUT or DELETE with either the username
``honor`` or the email ``honor@example.com`` and course_id
``course-v1:edX+DemoX+Demo_Course``. This information is found in the data.json file.
Each test have their on ``test_#_data`` where # refers to the number of the test
found in each test name. The current list of tests is as follows:

- **Test 1:** GET    request with email and course_id.  Data: ``test1_data``
- **Test 2:** GET    request with username and course_id.  Data: ``test2_data``
- **Test 3:** DELETE request with username and course_id.  Data: ``test3_data``
- **Test 4:** POST   request with username, course_id and mode.  Data: ``test4_data``
- **Test 5:** DELETE request with email and course_id.  Data: ``test5_data``
- **Test 6:** POST   request with email, course_id and mode.  Data: ``test6_data``
- **Test 7:** PUT    request with email, course_id, mode and is_active.  Data: ``test7_data``
- **Test 8:** PUT    request with username, course_id, mode and is_active.  Data: ``test8_data``
