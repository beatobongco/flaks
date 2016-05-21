from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
	form = {
		"title": "My form",
		"rows": 2,
		"fields": [
			{"label": "Foo", "type": "text", "size": 1},
			{"label": "Bar", "type": "text", "size": 1},
		]
	}
	return render_template("index.html", title="It works!", form=form)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=1337)