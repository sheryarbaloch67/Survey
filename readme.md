Prerequisites:
Python 3.x (https://www.python.org/downloads/)
pip, Python's package installer (usually comes bundled with Python)
Git version control system (https://git-scm.com/)
A code editor or IDE of your choice (e.g., Visual Studio Code, PyCharm)

1.  Setting Up the Development Environment:

    Create a virtual environment:

        Open a terminal or command prompt.
        Create a virtual environment named venv using the following command:
        python3 -m venv venv

    Activate the virtual environment:

        venv\Scripts\activate.bat (Windows)
        source venv/bin/activate (Mac OS)

    Clone the GitHub repository:

        Obtain the GitHub repository URL for your survey project.
        In your terminal, navigate to the directory where you want to clone the project and execute the following command:

            git clone <https://github.com/sheryarbaloch67/survey.git>

    Install project dependencies:

        Navigate to the project directory,
        Install the required packages listed in requirements.txt:

            pip install -r requirements.txt

        Then setup the Database by running following 2 commands:

            python3 manage.py makemigrations
            python3 manage.py migrate

2.  Creating a Survey:

    Start the development server:

        Run the following command in your terminal to start the Django development server:

            python3 manage.py runserver

        This will typically start the server on http://127.0.0.1:8000/.

    Access the "Create Survey" page:

        Open http://127.0.0.1:8000/create_survey/ in your web browser.
        You should see a form to create a new survey.

    Fill out the survey details:

        Enter a title for your survey in the "Title" field.
        Optionally, provide a description in the "Description" field.
        Create your survey questions:
            Click on the "Add Question" button to add a new question.
            Enter the question text in the "Question Text" field.
            Choose the question type from the "Question Type" dropdown menu (e.g., Text, Number, Dropdown).
            Depending on the question type, additional fields may appear:
            For "Dropdown" type, enter the choices in the "Choices" section (one choice per line).
            Click on the "Add Question" button again to add more questions (limit: 5-10).
        Once you're done adding questions, click the "Create Survey" button.

    Submit the survey:

        Upon successful creation, you might receive a confirmation message or be redirected to the created survey.
        The system will automatically generate a unique survey ID for reference.

3.  Answering a Survey:

    Access the survey:

        If you were redirected after creating the survey, you're already on the survey page. Otherwise, navigate to the survey using the provided URL or by querying the system for the survey ID.
        The URL will typically be in the format http://127.0.0.1:8000/answer-survey/<survey_id>, replacing <survey_id> with the actual ID.

    Provide your answers:

        Answer each question by entering text in the corresponding field or selecting an option from the dropdown menu (if applicable).
        Ensure you provide answers to all required questions.

    Submit the answers:

        Once you've answered all questions, click the "Submit Answers" button.

4.  Viewing Survey Answers:

    Access the answer view:

        You can access the survey answer view using the provided URL or by querying the system for the survey ID.
        The URL will typically be http://127.0.0.1:8000/view_answers/<survey_id>, replacing <survey_id> with the actual ID.

5.  Running Tests:

    To run the test cases written in test.py run the following command in the terminal:

        python3 manage.py test main
