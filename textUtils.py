import logging

def fitTextToLine(text, lineWidth):
  line = []
  cl = 0
  if len(text) > lineWidth:
    words = text.split()
    line.append('')
      
    for word in words:
      # if line width < lineWidth
      logging.debug('cl: %d, word: %d, length: %d', cl, len(word), (len(word) + len(line[cl])))
      if (len(word) + len(line[cl])) < lineWidth:
        
        # add word to line, if line is empty, word is now line
        if len(line[cl]) == 0:
          line[cl] = word
        else:
          line[cl] = "{} {}".format(line[cl], word)
      else:
        cl += 1
        line.append(word)
  else:
    line.append(text)
  return line

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  line = fitTextToLine("12345 78901 3456 789012 456789 0123456", 17)
  logging.info(line)
  print("{}\n{}".format(line[0], line[1]))

  line = fitTextToLine("dylan", 17)
  logging.info(line)