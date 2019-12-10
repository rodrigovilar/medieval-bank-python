# medieval-bank-python

To run automated tests, type:

  python3 -m unittest test_burgos_agency.py

To build container:
docker build -t bank-python .

To create the database in the container:
    docker run -it bank-python bash -c "cd /home/pyuser/medieval-bank-python && python -m persistence.models"

To run dockerized tests:
        docker run -it bank-python bash -c "cd /home/pyuser/medieval-bank-python && python -m persistence.models && python -m tests.test_service_attendant"

just change `test_service_attendant` to the name of the file that contains the tests you wanna run (**without the file extension**)
