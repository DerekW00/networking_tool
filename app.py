
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace 'your_openai_api_key_here' with your actual OpenAI API key
openai.api_key = 'your_openai_api_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        experience = request.form['experience']
        alumni = request.form['alumni']
        age = request.form['age']
        intent = request.form['intent']
        
        prompt = f"Create a {intent} message for {name}, a {experience} at {company}. Alumni: {alumni}, Age: {age}."
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=prompt,
            max_tokens=150
        )
        message = response.choices[0].text.strip()
        return render_template('index.html', message=message)
    return render_template('index.html', message='')

if __name__ == '__main__':
    app.run(debug=True)
