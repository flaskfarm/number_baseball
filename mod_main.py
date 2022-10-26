from .setup import *

name = 'main'

class ModuleMain(PluginModuleBase):
    
    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name=name)
        default_route_socketio_module(self)
        self.baseball = NumberBaseball(4,3)


    def process_menu(self, page, req):
        return render_template(f'{__package__}_{name}.html', arg={})
        
    def process_command(self, command, arg1, arg2, arg3, req):
        if command == 'start':
            self.baseball = NumberBaseball(int(arg1), int(arg2))
            self.send_data()
            return jsonify({"msg":f"초기화 하였습니다.<br>내 숫자 : {self.baseball.answer}", "ret":"success"})
        elif command == 'input_question':
            if self.baseball.check_only_one(arg1) == False:
                return jsonify({"msg":f"중복 숫자가 있습니다.<br>숫자 : {arg1}", "ret":"danger"})

            self.baseball.input_question_result(int(arg1), int(arg2), int(arg3))
            self.send_data()
        elif command == 'input_answser':
            if self.baseball.check_only_one(arg1) == False:
                return jsonify({"msg":f"중복 숫자가 있습니다.<br>숫자 : {arg1}", "ret":"danger"})

            self.baseball.input_answer_data(int(arg1))
            self.send_data()
        elif command == 'remove_data':
            if arg1 == 'question':
                self.baseball.input_remove_data(arg1, arg2)
                self.send_data()
        return jsonify('')

    def socketio_connect(self):
        self.send_data()
    
    def send_data(self):
        F.socketio.emit("status", self.baseball.get_status(), namespace=f'/{P.package_name}/{name}', broadcast=True)



import copy
import math
from random import randint


class NumberBaseball:

    def __init__(self, question_len, answer_len):
        self.question_len = question_len
        self.answer_len = answer_len
        self.answer = self.random_answer()
        self.question_data = []
        self.answer_data = []

    def input_question_result(self, *args):
        self.question_data.append([args[0], args[1], args[2]])
        ret = self.check(self.question_len, self.question_data)
        self.question_data[-1].append(ret)
        self.question_data[-1].append(self.make_info(ret))

    def input_remove_data(self, mode, index):
        if mode == 'question':
            copy_data = copy.deepcopy(self.question_data)
            self.question_data = []
            for idx, item in enumerate(copy_data):
                if idx != int(index):
                    self.input_question_result(*item)
        else:
            copy_data = copy.deepcopy(self.answer_data)
            self.answer_data = []
            for idx, item in enumerate(copy_data):
                if idx != int(index):
                    self.input_answer_data(*item)
           
    def make_info(self, ret):
        if len(ret) == 0: return []
        data = []
        for i in range(0, len(str(ret[0]))):
            tmp = []
            for _ in ret:
                if str(_)[i] not in tmp:
                    tmp.append(str(_)[i])
            data.append(sorted(tmp))
        return data



    def get_status(self):
        ret = {}
        ret['answer'] = self.answer
        ret['question_data'] = self.question_data
        ret['question_result'] = self.check(self.question_len, self.question_data)
        ret['answer_data'] = self.answer_data
        ret['answer_result'] = self.check(self.answer_len, self.answer_data)
        return ret
        

    def random_answer(self):
        start_number = int(math.pow(10, (self.answer_len-1)))
        last_number = int(math.pow(10, self.answer_len)-1)

        while True:
            number = randint(start_number, last_number)
            if self.check_only_one(str(number)):
                return number

    

    def input_answer_data(self, number):
        strike = 0
        ball = 0
        self.answer = str(self.answer)
        number = str(number)
        for i  in range(0,len(self.answer)):
            for j in range(0,len(self.answer)):
                if self.answer[i] == number[j]:
                    if i == j:
                        strike += 1
                    else:
                        ball += 1
        self.answer_data.append([int(number), strike, ball])
        ret = self.check(self.answer_len, self.answer_data)
        self.answer_data[-1].append(ret)
        self.answer_data[-1].append(self.make_info(ret))

    def check_only_one(self, number_str):
        tmp = [number_str[0]]
        for i in range(1, len(number_str)):
            if number_str[i] not in tmp:
                tmp.append(number_str[i])
            else:
                return False
        return True


    def check(self, length, data):
        ret = []
        start_number = int(math.pow(10, (length-1)))
        last_number = int(math.pow(10, length)-1)

        for i in range(start_number, last_number):
            if self.check_only_one(str(i)):
                if self.available(str(i), data):
                    ret.append(i)
        return ret


    def available(self, value, data):
        for item in data:
            number = str(item[0])
            strike = 0
            ball = 0
            for idx, no in enumerate(value):
                if no == number[idx]:
                    strike += 1
                elif no in number:
                    ball += 1
            if str(strike) == str(item[1]) and str(ball) == str(item[2]):
                continue
            else:
                return False
        return True

