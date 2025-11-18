from flask import Flask, render_template_string, request
import explorerhat, time, random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>🏆 COMP1313 Interactive Quiz</title>
  <style>
    body { font-family: Arial; text-align: center; background-color: #f4f4f4; margin-top: 50px; }
    h1 { color: #007acc; }
    .question-box { 
      background-color: white; 
      border-radius: 10px; 
      box-shadow: 0 0 10px rgba(0,0,0,0.1); 
      padding: 20px; 
      width: 60%; 
      margin: auto;
    }
    button {
      padding: 10px 20px; 
      margin: 5px; 
      font-size: 16px; 
      border: none; 
      border-radius: 5px; 
      background-color: #2196f3; 
      color: white; 
      cursor: pointer;
    }
    button:hover { background-color: #1976d2; }
    .message { font-size: 22px; margin-top: 20px; }
  </style>
</head>
<body>
  <h1>🏆 COMP1313 Interactive Quiz System</h1>

  {% if not answered %}
  <div class="question-box">
    <h2>Q{{ q['id'] }}. {{ q['question'] }}</h2>
    <form method="POST">
      {% for opt in q['options'] %}
        <button type="submit" name="answer" value="{{ opt }}">{{ opt }}</button>
      {% endfor %}
      <input type="hidden" name="correct" value="{{ q['answer'] }}">
    </form>
  </div>
  {% else %}
    <div class="message">{{ message }}</div>
    <meta http-equiv="refresh" content="2"> <!-- Auto refresh after 2s for next question -->
  {% endif %}
</body>
</html>
"""

# --- Quiz questions ---
questions = [
    {
        "id": 1,
        "question": "What does CPU stand for?",
        "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Control Program Utility"],
        "answer": "Central Processing Unit"
    },
    {
        "id": 2,
        "question": "Which component performs arithmetic operations?",
        "options": ["RAM", "ALU", "Cache", "Bus"],
        "answer": "ALU"
    },
    {
        "id": 3,
        "question": "Which of the following is volatile memory?",
        "options": ["ROM", "SSD", "RAM", "Flash Drive"],
        "answer": "RAM"
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form["answer"]
        correct = request.form["correct"]

        if selected == correct:
            # Correct → Blue LED for 2s
            explorerhat.output.two.on()
            time.sleep(2)
            explorerhat.output.two.off()
            return render_template_string(HTML, answered=True, message="✅ Correct!", q=None)
        else:
            # Incorrect → Red LED + Buzzer for 1s
            explorerhat.output.three.on()
            explorerhat.output.one.on()
            time.sleep(1)
            explorerhat.output.three.off()
            explorerhat.output.one.off()
            return render_template_string(HTML, answered=True, message="❌ Incorrect!", q=None)
    else:
        # Show a random question
        q = random.choice(questions)
        return render_template_string(HTML, q=q, answered=False, message=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
