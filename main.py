from avto_bot.parsavto import ParsaAvto
from avto_bot.recogn import AvtoNum
from avto_bot.vinru import get_inf_avto


# Распознаёт на фотографии авто изображение его номера
pa = ParsaAvto()
arr_num = pa.get_number('avto.jpg')
print(arr_num)


# Распознаём номер по фото
obj_num = AvtoNum()
str_avt_num = obj_num.pars_numb(arr_num)
print(f'Распознан номер: {str_avt_num}')


# Извлекаем информацию о фото по номеру
info_avto = get_inf_avto(str_avt_num)
print(info_avto)
