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

### GET '/categories'
**What it does:** Fetches all categories. The structure is a dictionary wherein each item consists of a key:value pair.

**Request Arguments:** None

**Returns:** A JSON object that contains a success message and an object with categories.
```
curl http://127.0.0.1:5000/categories

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

### GET '/questions'
**What it does:** Fetches all questions along with their categories, answers, and difficulty ratings. This is structured as a list of numerous question dictionaries. Each question consists of key:value pairs for ID, question, answer, category, and difficulty. This is the default view of the application.

**Request Arguments:** None

**Returns:** A JSON object that contains a success message, a list of questions, the total number of questions, a list of categories, and the current category (defaults to **None**). Results are paginated, allowing up to 10 questions per page.
```
curl http://127.0.0.1:5000/questions

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
    ...,
    {
      'id': 14, 
      'question': 'In which royal palace would you find the Hall of Mirrors?', 'answer': 'The Palace of Versailles', 
      'category': 3, 
      'difficulty': 3
    }
  ],
  'total_questions': 20,
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

### POST '/questions/category/<int:category_id>'
**What it does:** Fetches all questions based on a category filter. The structure is identical to the main questions endpoint.

**Request Arguments:** category_id

**Returns:** A JSON object that contains a success message, a list of questions, the total number of questions, and the current category. Results are paginated, allowing up to 10 questions per page.
```
# curl http://127.0.0.1:5000/questions/category/1

{
  'success': True,
  'questions': [
    {
      'id': 20, 
      'question': 'What is the heaviest organ in the human body?', 
      'answer': 'The Liver', 
      'category': 1, 
      'difficulty': 4
    }, 
    {
      'id': 21, 
      'question': 'Who discovered penicilin?', 
      'answer': 'Alexander Fleming', 
      'category': 1, 
      'difficulty': 3
    },
    {
      'id': 22, 
      'question': 'Hematology is a branch of medicine involving the study of what?', 
      'answer': 'Blood', 
      'category': 1, 
      'difficulty': 4
    }
  ],
  'total_questions': 20,
  'current_category': 1
}
```

### POST '/questions/search'
**What it does:** Fetches all questions that match a search term provided by the user. The structure is identical to the main questions endpoint.

**Request Arguments:** searchTerm

**Returns:** A JSON object that contains a success message, a list of questions, the total number of questions, and the current category (defaults to **None**). Results are paginated, allowing up to 10 questions per page.
```
# curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'

{
  'success': True,
  'questions': [
    {
      'id': 5, 
      'question': 'Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?', 
      'answer': 'Maya Angelou', 
      'category': 4, 
      'difficulty': 2
    }, 
    {
      'id': 6, 
      'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
      'answer': 'Edward Scissorhands', 
      'category': 5, 
      'difficulty': 3
    }
  ],
  'total_questions': 20,
  'current_category': None
}
```

### POST '/questions'
**What it does:** Posts a new question to the database. 

**Request Arguments:** body object that includes question, answer, difficulty, and category

**Returns:** A JSON object that contains a success message, the ID of the question just created, and the total number of questions
```
# curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d
'{"question":"Where is Mount Rushmore?", "answer":"South Dakota", "difficulty":1, "category":3}'

{
  'success': True,
  'created': 40,
  'total_questions': 23
}
```

### DELETE '/questions/<int:question_id>'
**What it does:** Deletes a question from the database. 

**Request Arguments:** question_id

**Returns:** A JSON object that contains a success message, the ID of the question just deleted, and the total number of questions
```
# curl http://127.0.0.1:5000/questions/40 -X DELETE

{
  'success': True,
  'deleted': 40,
  'total_questions': 22
}
```

### POST '/quizzes'
**What it does:** Plays through a trivia game. Questions can be from all categories or restricted to a specific category. Once all available questions have been exhausted, the game exits and displays the player's total correct answers. 

**Request Arguments:** previous_questions and quiz_category

**Returns:** A JSON object that contains a success message and a randomly selected question. If there are no questions left, question is marked **False**

```
# curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d
'{"previous_questions": [2],"quiz_category": {"type":"Science","id": "1"}}'

{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}

# once all questions have been exhausted

{
  "question": False
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