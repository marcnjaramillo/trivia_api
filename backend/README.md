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

## Endpoints
There are a total of seven endpoints you can interact with. This section gives a brief description of what each endpoint does, what request arguments are required, what HTTP methods are allowed, and what the expected return is.

### '/categories'
**What it does:** Fetches all categories. The structure is a dictionary wherein each item consists of a key:value pair.

**Request Arguments:** None

**HTTP Methods Allowed:** GET

**Returns:** A JSON object - categories - that contains an object with key:value pairs (id: 'category_name').
```
{
  'categories': {
    1 : 'Science',
    2 : 'Art',
    3 : 'Geography',
    4 : 'History',
    5 : 'Entertainment',
    6 : 'Sports'
  }
}
```
### '/questions'
**What it does:** Fetches all questions along with their categories, answers, and difficulty ratings. This is structured as a list of numerous question dictionaries. Each question consists of key:value pairs for ID, question, answer, category, and difficulty.

**Request Arguments:** None

**HTTP Methods Allowed:** GET

**Returns:** A JSON object - questions - that contains a success boolean, a list of question dictionaries with several key:value pairs, the total number of questions, a list of categories, and the current category (defaults to **None**). Results are paginated, allowing up to 10 questions per page
```
{
  'success': True,
  'questions': [
    {
      'id': 2, 
      'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 
      'answer': 'Apollo 13', 
      'category': 5, 
      'difficulty': 4
    }, 
    {
      'id': 4, 
      'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 
      'answer': 'Tom Cruise', 
      'category': 5, 
      'difficulty': 4
    }, 
    ...,
    {
      'id': 14, 
      'question': 'In which royal palace would you find the Hall of Mirrors?', 'answer': 'The Palace of Versailles', 
      'category': 3, 
      'difficulty': 3
    }
  ],
  'total_questions': 18,
  'categories': {
    1 : 'Science',
    2 : 'Art',
    3 : 'Geography',
    4 : 'History',
    5 : 'Entertainment',
    6 : 'Sports'
  },
  'current_category': None
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