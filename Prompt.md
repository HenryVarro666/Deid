输入到messages的content里的内容

# explicit

    prompt = "Please anonymize the following clinical note. Specifically, replace all the following information with the term “[redacted]”: redact any strings that might be a name or acronym or initial, redact any strings separated by the \/ symbol, redact patients' names, doctors' names and the strings in front of M.D. or after Dr., redact pager names and medical staff names, redact any strings that look like something years old or age 37, redact any dates and IDs and numbers and record dates, redact locations and addresses and clinic names, redact professions and ages and contacts, redact any acronyms and initials.: \n" + list_of_text_contents[i]  

# implicit

    prompt = "Please anonymize the following text: \n" + list_of_text_contents[i]  

---

# other

```python
# iterate over files in the source directory
for filename in tqdm(sorted(os.listdir(source_dir))):
    # checking if it is a file
    if os.path.isfile(os.path.join(source_dir, filename)):
        print("Processing file:", filename)
        # load the XML file
        with open(os.path.join(source_dir, filename), 'r') as f:
            soup = BeautifulSoup(f, features="xml")
            # extract the text content
            text = soup.find('TEXT').text
            # extract the answers to the 7 questions
            result1 = qamt0.extract(text, "What are the names?", iterate=True)
            result2 = qamt0.extract(text, "Who are the professions?", iterate=True)
            result3 = qamt0.extract(text, "What are the locations?", iterate=True)
            result4 = qamt0.extract(text, "What are ages?", iterate=True)
            result5 = qamt0.extract(text, "What are dates?", iterate=True)
            result6 = qamt0.extract(text, "What are contacts?", iterate=True)
            result7 = qamt0.extract(text, "What are IDs?", iterate=True)
            result8 = qamt0.extract(text, "What are the phone numbers?", iterate=True)
            # replace the matching characters with [redacted]
            for result in [result1, result2, result3, result4, result5, result6, result7, result8]:
                for r in result:
                    # print(r)
                    if '(' or ')' in r:
                      text = text.replace(r, '[redacted]')
                    else:
                      pattern = r'\b{}\b'.format(r)
                      text = re.sub(pattern, '[redacted]', text)
```
