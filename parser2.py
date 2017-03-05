import struct

STRING_START = (b'\xFA\xFF')

QUESTION_ALL = bytearray(b'\xF5\xFF')
ANSWER_ALL   = bytearray(b'\x00\xF6\xFF\xFA\xFF')
ANSWER_CORRECT = bytearray(b'\xFC\xFF\x00\x00\x00\x00\x00\x00\xF0\x3F')

def findNextAnswer(b):
	pos = b.find(ANSWER_ALL)
	if pos == -1:
		return -1
	else:
		return pos + len(ANSWER_ALL)


def findNextQuestion(b):
	pos = b.find(QUESTION_ALL)
	if pos == -1:
		return -1
	else:
		skip_buffer = b[pos+len(QUESTION_ALL):].find(STRING_START) + len(STRING_START)
		return pos + len(QUESTION_ALL) + skip_buffer

# The bytestring that this searches for is after the answer itself.
def findNextCorrectAnswer(b):
	pos = b.find(ANSWER_CORRECT)
	return pos


def printTextBuffer(b, suff=""):
	length = struct.unpack("h", b[0:2])[0]
	text = b[1:(length*2)+1]
	text = text.replace(b'\0', b'')
	print(text.decode("UTF-8"), suff)



with open("binflows/chapter8.txt", "rb") as f:
	b = bytearray(f.read())
	


q_pos = findNextQuestion(b)
b = b[q_pos:]

while q_pos != -1:
	printTextBuffer(b)
	q_pos = findNextQuestion(b)
	a_pos = findNextAnswer(b)

	# Find all answers before the next question
	while(a_pos != -1 and a_pos < q_pos):
		b = b[a_pos:]
		
		q_pos = findNextQuestion(b)
		a_pos = findNextAnswer(b)
		if(findNextCorrectAnswer(b) < q_pos and findNextCorrectAnswer(b) < a_pos):
			printTextBuffer(b, "<--")
		else:
			printTextBuffer(b)

	# Set buffer to next question.
	q_pos = findNextQuestion(b)
	b = b[q_pos:]
	print()
