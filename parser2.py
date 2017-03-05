import struct


QUESTION_ALL = bytearray(b'\xF5\xFF')
ANSWER_ALL   = bytearray(b'\x00\xF6\xFF\xFA\xFF')
ANSWER_CORRECT = bytearray(b'\xFC\xFF\x00\x00\x00\x00\x00\x00\xF0\x3F')

# Legacy
QUESTION_ALT   = bytearray(b'\xF6\xFF\x00\x00\xF4\xFF\x04\x00\xF4\xFF\x05\x00\xF4\xFF\x05\x00\xF4\xFF')
QUESTION_START = bytearray(b'\xF6\xFF\x00\x00\xF4\xFF\x05\x00\xF4\xFF\x06\x00\xF4\xFF\x06\x00\xF4\xFF')
ANSWER_ALT_FREE   = bytearray(b'\xF4\xFF\x05\x00\xF4\xFF\x03\x00\xF6\xFF\xFA\xFF')
ANSWER_ALT        = bytearray(b'\xF4\xFF\x09\x00\xF4\xFF\x03\x00\xF6\xFF\xFA\xFF')
ANSWER_START      = bytearray(b'\xF4\xFF\x03\x00\xF4\xFF\x04\x00\xF6\xFF\xFA\xFF')
ANSWER_START_FREE = bytearray(b'\xF4\xFF\x0B\x00\xF4\xFF\x04\x00\xF6\xFF\xFA\xFF')

#ANSWER_CORRECT = bytearray(b'\x00\xF0\x3F\xF4')
#ANSWER_CORRECT = bytearray(b'\xF4\xFF\x05\x00\xF4\xFF\x06\x00\xF4\xFF\x06\x00\xF4\xFF\x04\x00\xF6\xFF\xFA\xFF\x00\x00\xF4\xFF\x05\x00\xF4\xFF\x06\x00\xF4\xFF\x06\x00\xF4\xFF\x04\x00\xF6\xFF\xFC\xFF\x00\x00\x00\x00\x00\x00\xF0\x3F\xF4\xFF\x05\x00\xF4\xFF\x06\x00\xF4\xFF\x06\x00')

def findNextAnswer(b):
	next_answers = list()
	next_answers.append(b.find(ANSWER_ALL))
	#next_answers.append(b.find(ANSWER_START_FREE))
	# next_answers.append(b.find(ANSWER_ALT))
	# next_answers.append(b.find(ANSWER_ALT_FREE))
	if next_answers[0] == -1 and len(set(next_answers)) == 1:
		return -1
	pos = min(i for i in next_answers if i != -1)
	return pos + len(ANSWER_ALL)


def findNextQuestion(b):
	next_questions = list()
	next_questions.append(b.find(QUESTION_ALL))
	#next_questions.append(b.find(QUESTION_START))
	# next_questions.append(b.find(QUESTION_ALT))
	if next_questions[0] == -1 and len(set(next_questions)) == 1:
		return -1
	pos = min(i for i in next_questions if i != -1)
	skip_buffer = b[pos+len(QUESTION_ALL):].find(b'\xFA\xFF') + 2
	#print(skip_buffer)
	return pos + len(QUESTION_ALL) + skip_buffer # 14 is useless space

# The bytestring that this searches for is after the answer itself.
def findNextCorrectAnswer(b):
	pos = b.find(ANSWER_CORRECT)
	return pos


def printTextBuffer(b, suff=""):
	#print(b[:10])
	length = struct.unpack("h", b[0:2])[0]
	text = b[1:(length*2)+1]
	#print(length)
	#print(text[:10])
	text = text.replace(b'\0', b'')
	print(text.decode("UTF-8"), suff)



with open("binflows/chapter8.txt", "rb") as tf:
	f = tf.read()
	b = bytearray(f)
	


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
