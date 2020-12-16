Integration tests
=================

.. contents:: 

Enrollments API
+++++++++++++++

Running
-------

You can run the tests using the make target

.. code-block:: console

    $ make python-test

This test make several assumptions about the current state of the database
in case your setup differs you will have to modify ``test_data`` accordingly.

Data requirements
-----------------
The test_data file includes the data necessary to run each test. It's content
must reflect the current database configuration of the platform you
are running the tests. The provided test are meant to be run on a devstack
environment with the following requirements:

1. There should be a DOT application with client_id ``apiclient`` and
   client_secret ``apisecret``
2. There should be two sites available with Domain Name ``site1.localhost`` and
   ``site2.localhost``
3. Each site should have one user with username ``user_site1`` and email
   ``user_site1@example.com`` for ``site1`` and ``user_site2`` and
   ``user_site2@example.com`` for ``site2``.
4. ``site1`` should have a ``site1_course`` with id
   ``course-v1:edX+DemoX+Demo_Course`` this course should not be available on
   ``site2``. You must enable the ``audit`` and ``honor`` modes for ``site1_course``

``test_data`` layout
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "base_url": "http://localhost:18000",
        "client_id": "apiclient",
        "client_secret": "apisecret",
        "site1_data": {
            "fake_user": "fakeuser",
            "user_id": "user_site1",
            "user_email": "user_site1@example.com",
            "host": "site1.localhost",
            "course": {
                "id": "course-v1:edX+DemoX+Demo_Course",
                "mode": "audit"
            }
        },
        "site2_data": {
            "user_id": "user_site2",
            "user_email": "user_site2@example.com",
            "host": "site2.localhost"
        }
    }

Current Tests
-------------

Each test from this suite performs an http request to guarantee
that all CRUD operations are handled correctly. Bellow are
several tables, one for each operation, with all the parameters
combinations used for all the tests with data from ``test_data``

- **CREATE**

.. list-table::
  :header-rows: 1

  * - Method
    - Username or email
    - Course
    - Mode
    - Site
    - Force
    - Expected Result

  * - POST 
    - ``user_site1``
    - ``site1_course``
    - ``audit``
    - ``site1``
    - no
    - Pass

  * - POST 
    - ``user_site1``
    - ``site1_course``
    - ``audit``
    - ``site1``
    - yes
    - Pass

  * - POST 
    - ``fakeuser``
    - ``site1_course``
    - ``audit``
    - ``site1``
    - no
    - Fail

  * - POST 
    - ``user_site2``
    - ``site1_course``
    - ``audit``
    - ``site1``
    - no
    - Fail

  * - POST 
    - ``user_site1``
    - fake_course
    - ``audit``
    - ``site1``
    - yes
    - Pass

  * - POST 
    - ``user_site2``
    - ``site1_course``
    - ``audit``
    - ``site2``
    - yes
    - Fail

  * - POST 
    - ``user_site1``
    - ``site1_course``
    - ``masters``
    - ``site1``
    - no
    - Fail

- **READ**

.. list-table::
  :header-rows: 1

  * - Method
    - Username or email
    - Course
    - Site
    - Expected Result

  * - GET 
    - ``user_site1``
    - ``site1_course``
    - ``site1``
    - Pass

  * - GET 
    - ``user_site2``
    - ``site1_course``
    - ``site2``
    - Fail

  * - GET 
    - ``user_site1``
    - ``site1_course``
    - ``site2``
    - Fail

- **UPDATE**

.. list-table::
  :header-rows: 1

  * - Method
    - Username or email
    - Course
    - Mode
    - ``is_active``
    - Site
    - Force
    - Expected Result

  * - PUT 
    - ``user_site1``
    - ``site1_course``
    - ``audit -> audit``
    - ``true->false``
    - ``site1``
    - No
    - Pass

  * - PUT 
    - ``user_site1``
    - ``site1_course``
    - ``audit -> honor``
    - ``true->true``
    - ``site1``
    - No
    - Pass

  * - PUT 
    - ``user_site1``
    - ``site1_course``
    - ``audit -> masters``
    - ``true->true``
    - ``site1``
    - No
    - Pass

  * - PUT 
    - ``user_site2``
    - ``site1_course``
    - ``audit -> audit``
    - ``true->false``
    - ``site1``
    - No
    - Pass

  * - PUT 
    - ``user_site2``
    - ``site1_course``
    - ``audit -> honor``
    - ``true->true``
    - ``site1``
    - No
    - Pass

- **DELETE**

.. list-table::
  :header-rows: 1

  * - Method
    - Username or email
    - Course
    - Site
    - Expected Result

  * - GET 
    - ``user_site1``
    - ``site1_course``
    - ``site1``
    - Pass

  * - GET 
    - ``user_site2``
    - ``site1_course``
    - ``site2``
    - Fail

  * - GET 
    - ``user_site1``
    - ``site1_course``
    - ``site2``
    - Fail

Testing on stage
----------------
WIP
