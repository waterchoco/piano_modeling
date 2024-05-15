class Calculator:
    def __init__(self):

        self.expression = "(a)(E+A+C+b)"
        self.pp_list = []

    def list_to_expression(self, list):
        self.expression = ""

        self.expression = '+'.join(list)

        print(self.expression)
        print("")

    def bracket(self, ex):  # 괄호푸는 함수
        first = -1
        last = -1
        a = []
        self.pp_list = []

        plus1 = ex.find('+')
        # 괄호와 관련없는 문자들을 pp_list에 append
        if ex[0].isalpha() == True and ex.find('(', 0, ex.find('+')) == -1:
            self.pp_list.append(ex[:ex.find('+')])
        while True:

            plus2 = ex.find('+', plus1 + 1)
            if plus2 == -1:
                break
            if ex.find(')', plus1) < ex.find('(', plus1) or ex.rfind(')', 0, plus1) < ex.rfind('(', 0, plus1):
                plus1 = plus2
                continue

            if ex.find('(', plus1, plus2) == -1 and ex.find(')', plus1, plus2) == -1:
                self.pp_list.append(ex[plus1 + 1:plus2])
            plus1 = plus2

        if ex[len(ex) - 1].isalpha() == True and ex.rfind(')', ex.rfind('+'), len(ex) - 1) == -1:
            self.pp_list.append(ex[ex.rfind('+') + 1:])

        while True:
            # first와 last는 여러개의 괄호가 묶여있을때 첫번째 괄호만 나타냄

            first = ex.find('(', first + 1)
            last = ex.find(')', last + 1)
            print(first)
            if ex[first - 1] == ')':
                print(1)
                continue
            if first == -1:
                break
            print(first)
            # rlast는 괄호가 여러개 묶여있을 때 가장 오른쪽 닫는괄호
            rlast = last
            if last != len(ex) - 1:
                if ex[last + 1] != '(':
                    rlast = last
                else:
                    while True:
                        rlast = ex.find(')', rlast + 1)
                        if rlast >= len(ex) - 1:
                            break
                        if ex[rlast + 1] != '(':
                            break
                        if ex[rlast + 1] == -1:
                            break

            if last == len(ex) - 1:
                rlast = last
                after = last

            # before은 첫번째 괄호 이전에 묶인 상수들
            before = first
            if first != 0:
                before = first
                while ex[before - 1] != ')' and ex[before - 1] != "'" and ex[before - 1] != '+':
                    before -= 1
                    if before == -1:
                        before = 0
                        break

            # after은 마지막 괄호 이후에 묶인 상수들
            after = rlast

            if rlast != len(ex) - 1:
                after = rlast
                while ex[after + 1] != '(' and ex[after + 1] != "'" and ex[after + 1] != '+':
                    after += 1
                    if after >= len(ex) - 1:
                        after = len(ex) - 1
                        break

            # 첫번째 괄호에서 +들을 찾아 저장
            # 나중에 첫번째 괄호 안의 상수들을 하나하나 곱해줄 때 사용 (A+B)(B+C+D)(  =  A(B+C+D)( +B(B+C+D)(
            a = []
            for i in range(first, last):
                if ex[i] == '+':
                    a.append(i)
            if len(a) == 0:
                a.append(last)

            self.pp_list.append(
                ex[rlast + 1:after + 1] + ex[before:first] + ex[first + 1:a[0]] + ex[last + 1:rlast + 1])
            if len(a) > 1:
                for i in range(len(a) - 1):
                    self.pp_list.append(
                        ex[rlast + 1:after + 1] + ex[before:first] + ex[a[i] + 1:a[i + 1]] + ex[last + 1:rlast + 1])
                self.pp_list.append(
                    ex[rlast + 1:after + 1] + ex[before:first] + ex[a[len(a) - 1] + 1:last] + ex[last + 1:rlast + 1])
            # rlast:after: last  뒤의 모든 상수 곱하기
            # before:first first 앞의 모든 상수 곱하기
            # 첫번째 괄호 안에서 +가 아닌 상수들 곱하기
            # last+1:rlast+1     첫번째 괄호 이후의 모든 괄호 곱하기

            if last >= len(ex) - 1:
                break

        self.list_to_expression(self.pp_list)


cal = Calculator()
print(cal.expression)
cal.bracket(cal.expression)