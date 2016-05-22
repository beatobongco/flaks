from flask import Flask, render_template
from flaks.forms import make_form

app = Flask(__name__)

@app.route("/forms")
def forms():
	# How do we write forms?
	# Forms should be as easy as writing on paper!
	# Make a form easily using a string/file OR from a dict 

	form = make_form("""My Awesome Form
		
		Please open account at
		---
		Branch name: text

		Personal Details (Sole/First Accountholder/Minor)
		---
		Title: radio: Mr. |Mrs.|Ms.
		Full name: text

		Date of birth: date
		Nationality: select: American|Filipino|Japanese

		Account details
		---
		Choice of account: checkbox: Savings|Current|Fixed deposits
		Mode of funding: checkbox: Cash|Check|NEFT
		One radio: radio: Wow
		One checkbox: checkbox: Cool

		Go! POST https://httpbin.org/post""")

	return render_template("index.html", title="It works!", form=form)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=1337)