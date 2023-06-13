from socket import *
from threading import Thread, Lock, Condition

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Server ready")

answer_key = {"1": "VVFFV", "2": "VVVV"}
total_questions = len(answer_key)

statistics = {}
lock = Lock()
condition = Condition(lock)
counter = 0

def print_statistics():
    print("Statistics:")
    for question, stats in statistics.items():
        print(f"Question {question}: correct={stats['correct']}, incorrect={stats['incorrect']}")

def process_message(connectionSocket):
    global counter
    message = connectionSocket.recv(1024).decode('utf-8')
    questionNumber, numberOfOptions, answers = message.split(';')

    correct_answer = answer_key.get(questionNumber, "")
  
    correct = sum(1 for a, b in zip(answers, correct_answer) if a == b)
    incorrect = len(answers) - correct

    with lock:
        if questionNumber not in statistics:
            statistics[questionNumber] = {'correct': 0, 'incorrect': 0}

        if correct == len(correct_answer):
            statistics[questionNumber]['correct'] += 1
        if incorrect:
            statistics[questionNumber]['incorrect'] += 1

        counter += 1

        if counter == total_questions:
            print_statistics()
            counter = 0

    response = f"{questionNumber};{correct};{incorrect}"
    connectionSocket.send(response.encode('utf-8'))
    connectionSocket.close()

while True:
    connectionSocket, addr = serverSocket.accept()
    Thread(target=process_message, args=(connectionSocket,)).start()
