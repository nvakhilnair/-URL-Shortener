
# Text Sentiment Classification

API classifies textual data into positive, negative, and neutral based on the polarity score.
The model uses the Vader model for the classification which is a lexicon-based model.

## Docker

To containerize the application using Docker, follow these steps:

1. Build the Docker image: 
    ```
    docker build -t text-sentiment-classification .
    ```
2. Run the Docker container: 
    ```
    docker run -d -p 8000:8000 text-sentiment-classification
    ```

## Starting the Application

To start the application, you can use the provided batch (.bat) or shell (.sh) files:

- For Windows (.bat): 
    ```
    start_app.bat
    ```
- For Unix-based systems (.sh):
    ```
    ./start_app.sh
    ```

Ensure that you have installed the required dependencies mentioned in `requirements.txt` before starting the application.


## Usage

To utilize the text processing API provided by this project, you can send a `GET` request to the `/classify` endpoint. Below is an example `curl` command demonstrating how to use the endpoint:

### using curl
```
curl 'http://127.0.0.1:8000/classify/?input_text=Hello%20my%20name%20is%20akhil&preprocess=false
```

### using python

```
import requests

url = 'http://127.0.0.1:8000/classify/'
params = {
    'input_text': 'Hello my name is akhil',
    'preprocess': 'false'
}
response = requests.get(url, params=params)
```

## Tech Stack

- Python
- FastAPI
- Uvicorn
- HTML
- CSS
- Javascript

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

If you have any feedback, please reach out to us at madewithpy009@gmail.com

For support, email madewithpy009@gmail.com.## 🚀 About Me
- 👋 Hi, I’m @nvakhilnair
- 👀 I’m interested in Data Science,Machine learning, Data Mining, Data Visualization and Programing
- 🌱 I’m currently open to work
- 📫 How to reach me https://www.linkedin.com/in/akhilnvnair
## Authors

- [@nvakhilnair](https://github.com/nvakhilnair)
