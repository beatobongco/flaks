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
		"url": action[1],
		"method": action[2].lower()
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
				
				row_dict["fields"].append({
					"size": 1,
					"label": _field[0].strip(),
					"name": _field[0].strip().replace(" ", "_").lower(),
					"type": _field[1].strip()
				})
			
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

	form = make_form("""My Awesome Form
		
		Personal Info
		---
		First name: text
		Family name: text		
		Address: text

		Personal Info2
		---
		Wow: text
		Cool: text

		Beans: text
		Sausage: text

		Go! https://httpbin.org/post POST""")

	form2 = {
		"title": "My form",
		"fieldsets": [
			{
				"title": "Personal Info", 
				"rows": [
					{
						"size": 2, 
						"fields": [
							{"size": 1, "name": "cool", "label": "Cool", "type": "text"},
							{"size": 1, "name": "beans", "label": "Beans", "type": "text"}
						],
					},
				],
			}
		],
		"action": {
			"button_text": "Go!",
			"method": "post",
			"url": "https://httpbin.org/post"
		}
	}
	return render_template("index.html", title="It works!", form=form)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=1337)