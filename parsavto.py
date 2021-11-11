import cv2 as cv


class ParsaAvto:
    """
    Класс реализует объект для парсинга фото авто.
    В результате получаем фото номера
    """

    def __init__(self):
        # устанавливаем каталог программы
        # self.dir_prog = os.path.dirname(os.path.abspath(__file__))
        # загрузка какадного классификатора
        self.haar_cascade = cv.CascadeClassifier('haarcascade_russian_plate_number.xml')


    def get_number(self, img_name: str):
        """
        Распознаёт на фотографии авто изображение его номера
        :param img_name: Имя файла изображения авто
        :return: Номер авто -- <class 'numpy.ndarray'>
        """
        img = cv.imread(img_name)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = self.haar_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            area_number = img_gray[y:y + h, x:x + w]  # часть изображения вырезанная по размерам распознанной области
            return area_number
        else:
            return []


if __name__ == '__main__':
    pa = ParsaAvto()
    arr_num = pa.get_number('avto.jpg')
    print(type(arr_num))
