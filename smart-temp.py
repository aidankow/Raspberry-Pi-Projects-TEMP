from flask import Flask, render_template_string
import explorerhat, time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Smart Temperature Monitor</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: Arial; text-align: center; margin-top: 60px; }
    .temp { font-size: 48px; color: #007acc; }
    .alert { color: red; font-weight: bold; }
  </style>
</head>
<body>
  <h1>🌡️ Smart Temperature Monitor</h1>
  <div class="temp">{{ temp }} °C</div>
  {% if temp > 30 %}
    <p class="alert">Warning: High Temperature!</p>
  {% endif %}
  <p>Auto-refresh every 5 seconds</p>
</body>
</html>
"""

@app.route("/")
def index():
    analog_value = explorerhat.analog.one.read()
    voltage = analog_value * 3.3
    temp_c = round((voltage - 0.5) * 100, 2)
    if temp_c > 30:
        explorerhat.output.one.on()
        time.sleep(1)
        explorerhat.output.one.off()
    return render_template_string(HTML, temp=temp_c)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

