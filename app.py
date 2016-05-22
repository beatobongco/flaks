from flask import Flask, render_template
app = Flask(__name__)

def group_fieldsets(lines):
	separator = "---"
	r_list = []
	temp_list = []
	start_adding = False
	for index, line in enumerate(lines):
		_l = line.strip()
		
		if start_adding:
			if _l == separator:
				# remove previously added elem, return the templist
				_t = temp_list.pop(-1)
				r_list.append(temp_list)
				temp_list = [_t]
				continue
			else:
				temp_list.append(_l)

		if _l == separator:
			# Add prev line, dont add this line
			temp_list.append(lines[index - 1].strip())
			start_adding = True
			continue
	else:
		r_list.append(temp_list)

	return r_list

def group_rows(fieldset):
	r_list = []
	temp_list = []
	
	for x in fieldset:
		if x == '':
			r_list.append(temp_list)
			temp_list = []
			continue
		temp_list.append(x)

	return r_list

def make_form(t):
	form = {"fieldsets": []}
	lines = t.splitlines()
	form["title"] = lines.pop(0)
	action = lines.pop(-1).split()
	form["action"] = {
		"button_text": action[0],
		"url": action[2],
		"method": action[1].lower()
	}
	fieldsets = group_fieldsets(lines)

	for fieldset in fieldsets:
		fieldset_dict = {
			"title": fieldset.pop(0),
			"rows": [],
		}

		# Get the rows by whitespace 
		rows = group_rows(fieldset) 
		
		for row in rows:
			row_dict = {
				"size": len(row),
				"fields": []
			}

			for field in row:
				_field = field.split(":")
				field_type = _field[1].strip()
				field_dict = {
					"size": 1,
					"label": _field[0].strip(),
					"name": _field[0].strip(),
					"type": field_type 
				}

				if field_type in ["radio", "checkbox", "select"]:
					field_dict["choices"] = [x.strip() for x in _field[2].split("|")]

				row_dict["fields"].append(field_dict)
			
			fieldset_dict["rows"].append(row_dict)

		form["fieldsets"].append(fieldset_dict)
	return form

@app.route("/")
def hello():
	## How do we write forms?
	## Forms should be as easy as writing on paper!
	# Consider cases of only one choice
	## Gender: radio: m/f/unknown
	## Pick any: checkbox: banana/apple/sausage
	## Pick one: dropdown: a/b/c/d

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