from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QColorDialog, QCompleter,\
    QTableWidgetItem, QFileDialog
from form import Ui_MainWindow
from PyQt5.QtCore import Qt
import requests
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.result = None
        self.lat = 51.679734
        self.lon = 39.197082
        self.delta = 0.1
        self.l = 'map'
        self.pt = ''
        self.spn = ''
        self.show_postal_code = False
        self.new_map()
        self.initUI()

    def initUI(self):
        self.search_btn.clicked.connect(self.search)
        self.clear_btn.clicked.connect(self.clear)
        self.type_btn.clicked.connect(self.change_type)
        self.label_photo.setPixmap(self.photo)
        self.search_line.returnPressed.connect(self.search)
        self.postal_code_checkbox.clicked.connect(self.postal_code_func)

    def search(self, search_text=None, central=True):
        if not search_text:
            search_res = search(self.search_line.text())
        else:
            search_res = search(search_text)
        if central:
            self.lon, self.lat = float(search_res[0]), float(search_res[1])
            self.spn = search_res[2]
        self.pt = search_res[3]
        if self.show_postal_code:
            self.address_label.setText(search_res[4] + ',\n' + search_res[5])
        else:
            self.address_label.setText(search_res[4])
        self.new_map()

    def clear(self):
        self.pt = ''
        self.search_line.clear()
        self.address_label.clear()
        self.new_map()

    def postal_code_func(self):
        if self.show_postal_code:
            self.show_postal_code = False
        else:
            self.show_postal_code = True
        try:
            self.search(self.address_label.text(), central=False)
        except Exception:
            pass

    def change_type(self):
        if self.l == 'map':
            self.l = 'sat'
        elif self.l == 'sat':
            self.l = 'sat,skl'
        else:
            self.l = 'map'
        self.new_map()

    def new_map(self):
        create_map(self.lon, self.lat, self.delta, self.l, self.pt)
        self.photo = QPixmap('map.png')
        self.label_photo.setPixmap(self.photo)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.lon += self.delta
        elif event.key() == Qt.Key_Left:
            self.lon -= self.delta
        elif event.key() == Qt.Key_Up:
            self.lat += self.delta
        elif event.key() == Qt.Key_Down:
            self.lat -= self.delta
        elif event.key() == Qt.Key_PageUp:
            if self.delta <= 10:
                self.delta -= self.delta / 2
            else:
                self.delta -= self.delta
            if self.delta < 0.001:
                self.delta = 0.001
        elif event.key() == Qt.Key_PageDown:
            if self.delta <= 10:
                self.delta += self.delta / 2
            else:
                self.delta += self.delta
            if self.delta > 90:
                self.delta = 90.0
        self.new_map()

    def mousePressEvent(self, event):
        self.x_pos, self.y_pos = event.x() - 400, event.y() - 245
        self.x_pos = self.lon + self.x_pos * self.delta / 150
        self.y_pos = self.lat - self.y_pos * self.delta / 225
        if event.button() == Qt.LeftButton:
            self.pt = str(self.x_pos) + ',' + str(self.y_pos) + ',pm2rdl'
            self.search(str(self.x_pos) + ',' + str(self.y_pos), False)
        elif event.button() == Qt.RightButton:
            search_res = org_search(str(self.x_pos) + ',' + str(self.y_pos))
            print(search_res)
            if search_res:
                self.address_label.setText(search_res[1] + '\n' + search_res[2])
                self.pt = ','.join([str(i) for i in search_res[0]]) + ',pm2rdl'
                self.new_map()


def create_map(lon, lat, delta, l, pt=''):
    map_request = "https://static-maps.yandex.ru/1.x/"
    map_file = "map.png"
    spn = ",".join([str(delta), str(delta)])
    a = ''
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": spn,
        "l": l
    }
    if pt:
        params['pt'] = pt
    resp = requests.get(map_request, params=params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        if a != resp.content:
            a = resp.content
        file.write(resp.content)
    file.close()


def spn(toponym):
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner'].split()
    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner'].split()
    print(lower_corner, upper_corner)
    size_y = abs(float(upper_corner[0])) - abs(float(lower_corner[0]))
    size_x = abs(float(upper_corner[1])) - abs(float(lower_corner[1]))
    return (str(round(size_y, 5)), str(round(size_x, 5)))


def search(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return 404
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    try:
        toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    except KeyError:
        toponym_address = 'Нельзя отобразить адресс для данного объекта'
    try:
        toponym_postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    except KeyError:
        toponym_postal_code = 'Нельзя отобразить почтовый индекс для данного объекта'

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    spn_res = spn(toponym)
    pt = f'{",".join(toponym_coodrinates.split())},pm2rdl'
    return (toponym_longitude, toponym_lattitude, ','.join(spn_res), pt, toponym_address,
            toponym_postal_code)


def org_search(pos):
    geosearch_api_server = "https://search-maps.yandex.ru/v1/"
    print(pos)
    search_params = {
        "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
        "lang": "ru_RU",
        'text': 'воронеж',
        "ll": str(pos),
        "type": "biz",
        "spn": '0.0007234,0.000449',
        'rspn': 1
    }
    response = requests.get(geosearch_api_server, params=search_params)
    json_response = response.json()
    print(json_response)
    try:
        coords = json_response["features"][0]["geometry"]["coordinates"]
        org_address = json_response["features"][0]["properties"]["CompanyMetaData"]["address"]
        org_name = json_response["features"][0]["properties"]["CompanyMetaData"]["name"]
    except KeyError:
        return None
    return (coords, org_address, org_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())