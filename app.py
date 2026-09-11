import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
urls = {}

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>URL Shortener</title>
<style>body{font-family:system-ui;max-width:500px;margin:60px auto;padding:20px}
input,button{padding:10px;font-size:16px}input{width:70%}
button{background:#4a6cf7;color:#fff;border:0;border-radius:6px;cursor:pointer}
.short{margin-top:20px;background:#eee;padding:12px;border-radius:6px;font-family:monospace}</style>
</head><body>
<h1>Сокращатель ссылок</h1>
<form method="post">
  <input name="url" placeholder="https://example.com" required>
  <button>Сократить</button>
</form>
{% if short %}<div class="short"><a href="/{{short}}">{{ request.host_url }}{{short}}</a></div>{% endif %}
</body></html>
"""


def gen_code(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@app.route("/", methods=["GET", "POST"])
def index():
    short = None
    if request.method == "POST":
        url = request.form["url"]
        code = gen_code()
        urls[code] = url
        short = code
    return render_template_string(HTML, short=short)


@app.route("/<code>")
def follow(code):
    if code in urls:
        return redirect(urls[code])
    return "Не найдено", 404


if __name__ == "__main__":
    app.run(debug=True)