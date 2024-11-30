from flask import Flask

app = Flask(__kubu-hai__)

@app.route('/')
def home():
return "Hello, Flask!"

if __name__ == '__main__':
app.run(debug=True)
