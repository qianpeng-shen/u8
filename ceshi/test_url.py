def fun(data):
	if data == '1':
		return '壹'
	elif data == '2':
		return '贰'
	elif data == '3':
		return '叁'
	elif data == '4':
		return '肆'
	elif data == '5':
		return '伍'
	elif data == '6':
		return '陆'
	elif data == '7':
		return '柒'
	elif data == '8':
		return '捌'
	elif data == '9':
		return '玖'
number = input('请输入数字')

num_list = ['億','仟','佰','拾','萬','仟','佰','拾']
num_count = len(number) -1
num_str = ''
for num in number:
    data = fun(num)
    num_str += data
    if num_count != 0:
        num_str+= num_list[-(num_count)]
    num_count -= 1
print(num_str)