# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE ...

GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}

GET '/questions'
    A => If there is no search criteria in POST body
    - Fetches a list of all questions if no search criteria is in the body.
    - Fetches a list of search matches if a search term is entered in the post body
    - Request Arguments: None
    - Returns all a dictionary of all categories
    -Returns a list of all questions paginated to be 10 questions per page in json format as seen in example below.

    "current_category": null, 
    "questions": [
        {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ], 
    "questions_on_this_page": 10, 
    "success": true, 
    "total_questions": 21
    }

    B => GET '/questions?search=who'
    If there is search criteria in request Body
    - Fetches a list of all questions that march search criteria that is in the request body.
    - Request Arguments: search term in request body. example: '/question?search=who'
    - Returns a list of all questions that match given search criteria as show below, search criteria is "who"

    {
  "questions": [
    {
      "answer": "A mystic, a high man, a smuggler.", 
      "category": 2, 
      "difficulty": 5, 
      "id": 27, 
      "question": "Who is Sadguru"
    }
  ], 
  "search string": "who", 
  "search_result_on_this_page": 5, 
  "success": true, 
  "total search result": 5
}


POST '/questions'
    - Post/create new question entry indicating all required parameters for entry.
    - Request parameters: question, answer, category, difficulty as shown the the curl request  below

    curl -X POST -H "Content-Type: application/json" -d '{"question":"Where is the Kanji dam", "answer":"Nigeria", "category":"5"}' http://127.0.0.1:5000/questions

    - Returns json object showing object ID created and all questions on page one with an increased number of total questions as shown below 

    {
  "created": 28, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
  "success": true, 
  "total questions": 22


POST '/play'
    - Takes previous_questions and trivia_category parameter in POST body as shown below

    curl -X POST -H "Content-Type: application/json" -d '{"trivia_category":4, "previous_question":4}' http://127.0.0.1:5000/play

    - Returns a random question as shown below
{
  "question": "Which dung beetle was worshipped by the ancient Egyptians?", 
  "success": true
}


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```