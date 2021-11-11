import easyocr

class AvtoNum:
    """
    Класс реализует механизм распознавания номера авто по фото
    """

    def __init__(self):
        # При вервом запуске модель копируется в C:\Users\D.Vetrov\.EasyOCR\model
        # и загружается в память
        self.reader = easyocr.Reader(['ru'], gpu=False)
        self.allowlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х',
                     'а', 'в', 'е', 'к', 'м', 'н', 'о', 'р', 'с', 'т', 'у', 'х', ]


    def pars_numb(self, path_img) -> str:
        """
        Распознаёт номер
        :param path_img: имя файла фото либо numpy.ndarray
        :return: распознаный номер
        """
        result = self.reader.readtext(path_img, detail=0, allowlist=self.allowlist)
        return result[0]


if __name__ == '__main__':
    a_num = AvtoNum()
    print(a_num.pars_numb('number_avto.jpg'))