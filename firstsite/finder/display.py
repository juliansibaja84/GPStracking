from html.parser import HTMLParser
import sqlite3


class Navigator(HTMLParser):
    def __init__(self):
        super(Navigator, self).__init__()
        self.ini = ('', '')
        self.fin = ('', '')

    def handle_comment(self, comment):
        if self.ini == ('', ''):
            self.ini = navi.getpos()
        else:
            self.fin = navi.getpos()

if __name__ == '__main__':
    navi = Navigator()

    # Read the HTML file
    with open('templates/finder/logger.html') as f:
        content = f.read()

    # Encontrar comentario
    navi.feed(content)

    # Regresar el HTML a su estado original
    f = open('templates/finder/logger.html', 'r')
    linesx = f.readlines()
    f.close()

    lines = linesx[:navi.ini[0]]
    lines.extend(linesx[navi.fin[0]-1:])

    f = open('templates/finder/logger.html', 'w')
    lines = "".join(lines)
    f.write(lines)
    f.close()

    # Crear texto a insertar
    contents = ''
    conn = sqlite3.connect('log.db')
    cc = conn.cursor()

    cont = 0
    for row in cc.execute('SELECT * FROM log ORDER BY tiempo DESC'):
        cont += 1
        data = row[2].decode('utf-8')
        ip = row[0]
        port = row[1]
        time = row[3]
        latitude = ''
        longitude = ''
        if data[:4] == '>REV':
            latitude = data[16:19] + '.' + data[19:24]
            longitude = data[24:28] + '.' + data[28:33]

            # Crear tags HTML
            tag = '<th>' + latitude + '</th>' + '<th>' + longitude + '</th>'
            tag += '<th>' + time + '</th>' + '<th>' + ip + '</th>'
            tag += '<th>' + port + '</th>'
            tag = '<tr>' + tag + '</tr>'

            if cont == 1:
                f = open('/home/julian84/firstsite/top.txt', 'w')
                f.write(latitude + ',' + longitude + ',' + time)
                f.close()
            # Juntar todas las tags
            contents += contents + tag

    # Extender la tabla
    f = open('templates/finder/logger.html', 'r')
    linesx = f.readlines()
    f.close()

    lines = linesx[:navi.ini[0]]
    lines.append(contents + '\n')
    lines.extend(linesx[navi.ini[0]:])

    f = open('templates/finder/logger.html', 'w')
    lines = "".join(lines)
    f.write(lines)
    f.close()


