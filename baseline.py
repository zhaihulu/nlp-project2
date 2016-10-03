"""
--------------------------------------------------------------------------------
MODEL
--------------------------------------------------------------------------------
"""
"""
Idea: keep track of words that come immediately before and after a given word
                    B: if w1/POS has B-cue, these are the words that immediately precede w1
          before  { I: if w1/POS has I-cue, these are the words that immediately precede w1
                    O: if w1/POS has O-cue, these are the words that immediately precede w1
w1/POS  {
                    B: if w1/POS has B-cue, these are the words that immediately follow w1
          after   { I: if w1/POS has I-cue, these are the words that immediately follow w1
                    O: if w1/POS has O-cue, these are the words that immediately follow w1
So we look at a word and it's pos, we'll access this dictionary that's developed in training
For example, if we're given the word "likely / JJ", and the dictionary looks something like this:
d["likely JJ"]["before"]["B"] = ""
d["likely JJ"]["before"]["I"] = "most", "very", "is"
d["likely JJ"]["before"]["O"] = "so"
d["likely JJ"]["after"]["B"] = "that"
d["likely JJ"]["after"]["I"] = "that", "more"
d["likely JJ"]["after"]["O"] = "."
and we have a sentence:
"It is likely that it is not true."
B-count would be 1, I-count would be 2, and O-count would be 0.
We see we hve the highest counts for "I", so likely would be given the I-cue.
"""
# training
train_dict = {}
for filename in listdir(newpath):
  file = open(newpath + "/" + filename, "r")
  lines = file.readlines()
  for i in range(len(lines)):
    line = lines[i]
    word = line.split()[0] + " " + line.split()[1]
    tag = line.split()[2][0]
    if word not in train_dict:
      train_dict[word] = {}
      train_dict[word]["before"] = {"B": [], "I": [], "O": []}
      train_dict[word]["after"] = {"B": [], "I": [], "O": []}
    if i > 0:
      train_dict[word]["before"][tag].append(lines[i-1].split()[0])
    else:
      train_dict[word]["before"][tag].append("")
    if i < len(lines) - 1:
      train_dict[word]["after"][tag].append(lines[i+1].split()[0])
    else:
      train_dict[word]["after"][tag].append("")
    # remove duplicates
    list(set(train_dict[word]["before"][tag]))
    list(set(train_dict[word]["after"][tag]))
# sequence tagger
test_private = {}
test_public = {}
path_private = "nlp_project2_uncertainty/test-private"
path_public = "nlp_project2_uncertainty/test-public"
for filename in listdir(path_public):
  file = open(path_public + "/" + filename, "r")
  test_public[filename] = {}
  lines = file.readlines()
  for i in range(len(lines)):
    line = lines[i]
    # check if newline
    if line != "\n":
      word = line.split()[0] + " " + line.split()[1]
      if word in train_dict:
        before_words = train_dict[word]["before"]
        after_words = train_dict[word]["after"]
        if i > 0 and lines[i-1] != "\n":
          preceding = lines[i-1].split()[0]
        else:
          preceding = ""
        if i < len(lines) - 2 and lines[i+1] != "\n":
          following = lines[i+1].split()[0]
        else:
          following = ""
        b_count = before_words["B"].count(preceding) + after_words["B"].count(following)
        i_count = before_words["I"].count(preceding) + after_words["I"].count(following)
        o_count = before_words["O"].count(preceding) + after_words["O"].count(following)
        if b_count > i_count:
          tag = "B"
        elif b_count > o_count:
          tag = "B"
        elif i_count > o_count:
          tag = "I"
        else:
          tag = "O"
      else:
        # todo: handle unknown words
        # print word + " not in train_dict... giving it tag O"
        tag = "O"
    test_public[filename][i] = tag
  # print("For file " + filename + ", there are " + str(test_public[filename].values().count("B")) + " B-cue, " + str(test_public[filename].values().count("I")) + " I-cue, and " + str(test_public[filename].values().count("O") + " O."))