import copy
import time

t1=time.time()
origin = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 3, 6, 0, 0, 0, 0, 0],
          [0, 7, 0, 0, 9, 0, 2, 0, 0],
          [0, 5, 0, 0, 0, 7, 0, 0, 0],
          [0, 0, 0, 0, 4, 5, 7, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 3, 0],
          [0, 0, 1, 0, 0, 0, 0, 6, 8],
          [0, 0, 8, 5, 0, 0, 0, 1, 0],
          [0, 9, 0, 0, 0, 0, 4, 0, 0]]

class sudoku:
    def debug(self):  # 调试
        for list in origin:
            print(list)
        print("\n")

    def check_repetition(self,list):#判断表中是否有重复值，0除外
        flag=0
        for i in range(1,10):
            if list.count(i)>=2:
                return 1
            else:
                flag=flag+1
        if flag==9:
            return 0

    def check_row(self,row):#检测横向是否有重复值，无则为返回0，有则返回1
        list = origin[row]  # 横向
        r1 = self.check_repetition(list)
        if r1 == 0:
            return 0
        else :
            return 1

    def check_column(self,column):#检测纵向是否重复值，无则为返回0，有则返回1
        list = []  # 纵向
        for num in origin:
            list.append(num[column])
        r2 = self.check_repetition(list)
        if r2==0:
            return 0
        else:
            return 1

    def check_square(self,x,y):#检测九宫格是否有重复值，无则为返回0，有则返回1
        x,y=y,x
        if x>=9 or y>=9:
            return
        square = []#九宫格
        for i in range(0+y//3*3, 3+y//3*3):
            for j in range(0+x//3*3, 3+x//3*3):
                square.append(origin[i][j])
        r3 = self.check_repetition(square)
        if r3==0:
            return 0
        else:
            return 1

    def check(self,x,y):#检测是否有重复值，无则为0，有则不为0
        r1 = self.check_row(x)
        r2 = self.check_column(y)
        r3 = self.check_square(x, y)
        result=r1+r2+r3
        return result

    def get_next(self):  # 获得下一个空值，返回row,column值
        i = 0
        for list in origin:
            try:  # 当0不在列表中时，跳过
                column = list.index(0)
                row = origin.index(list)
                res = (row, column)
                return res
            except ValueError:
                i = i + 1
                if i == 9:
                    t2=time.time()
                    print("总用时={}".format(t2 - t1))
                    exit(0)

    def poi(self,row, column):  # 位置修正
        if row == 0 and column == -1:
            return
        if row == 8 and column == 9:
            return
        if column == -1:
            column = 8
            row = row - 1
        if column == 9:
            column = 0
            row = row - 1
        return (row, column)

    def get_last(self,row, column):
        origin[row].insert(column, 0)
        origin[row].pop(column + 1)
        column = column - 1  # 获得上一个已填值的行、列位置
        row, column = self.poi(row, column)#位置修正
        r = origin[row][column] * compare[row][column]
        while r != 0:
            column = column - 1
            row, column = self.poi(row, column)
            r = origin[row][column] * compare[row][column]
        return (row, column)

    def blank(self):
        try:
            row,column=self.get_next()
        except TypeError:#已填完
            exit(0)
        j=0
        flag=0
        for i in range(1,10):
            origin[row].insert(column,i)
            origin[row].pop(column+1)
            self.debug()
            r = self.check(row, column)
            if r==0:#无重复值
                return
            else:
                j = j + 1
                if j==9:
                    flag=1
                    break
        if flag==1:
            row, column = self.get_last(row, column)
            value=origin[row][column]
            self.debug()
            while value == 9:
                row, column = self.get_last(row, column)
                value = origin[row][column]
                self.debug()
            while value<9:
                for k in range(value+1,10):
                    origin[row].insert(column, k)
                    origin[row].pop(column + 1)
                    self.debug()
                    r=self.check(row,column)
                    if r!=0:#有重复
                        if k==9:
                            row, column = self.get_last(row, column)
                            value=origin[row][column]
                            self.debug()
                            while value==9:
                                row, column = self.get_last(row, column)
                                value = origin[row][column]
                                self.debug()
                            break
                    else:
                        return

if __name__=="__main__":
    compare = copy.deepcopy(origin)
    sudoku = sudoku()
    while 1:
        sudoku.blank()
