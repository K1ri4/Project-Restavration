#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) : QWidget(parent), ui(new Ui::Widget) {
    ui->setupUi(this);
    connect(ui -> choose_file, &QPushButton::released, this, &Widget::slot_openfile);
    connect(ui -> speeds, &QComboBox::currentTextChanged, this, &Widget::slot_speed);
    connect(ui -> l_filename, &QLineEdit::textChanged, this, &Widget::slot_enter);
    connect(ui -> choose_file, &QPushButton::released, this, &Widget::slot_sendfile);
    timer = new QTimer();
    connect(timer, &QTimer::timeout, this, &Widget::slot_timer);
    timer -> start(1000); // 1 sec
    system("COM.exe");
}

void Widget::slot_sendfile() {
    QString fileName = "send.txt";
    if (!fileName.isEmpty()) {
        QFile f(fileName);
        f.open(QIODevice::WriteOnly | QFile::Truncate);
        QTextStream stream(&f);
        stream.setAutoDetectUnicode(true);
        stream << ui -> l_filename -> text();
        f.close();
    }
    fileName = "speed.txt";
    if (!fileName.isEmpty()) {
        QFile f(fileName);
        f.open(QIODevice::WriteOnly | QFile::Truncate);
        QTextStream stream(&f);
        stream.setAutoDetectUnicode(true);
        stream << ui -> speeds -> currentText();
        f.close();
    }
    ui -> standby -> setText("Отправка файла...");
    sended = true;
    system("TX.exe");
}

void Widget::slot_timer() {
    slot_getcom();
    QString fileName = "get.txt";
    if (QFileInfo("get.txt").exists()) {
        QFile f(fileName);
        f.open(QIODevice::ReadOnly);
        QTextStream stream(&f);
        stream.setAutoDetectUnicode(true);
        QString s;
        bool ok = true;
        while (stream.readLineInto(&s)) {
            if (stream.status() != QTextStream::Ok) {
                QMessageBox MessageBox;
                MessageBox.setWindowTitle("Ошибка чтения файла");
                MessageBox.setText("Ошибка во время чтения файла!");
                MessageBox.setInformativeText("Возможно файл недоступен для чтения или повреждён");
                MessageBox.setIcon(QMessageBox::Warning);
                MessageBox.exec();
                ok = false;
                break;
            }
        }
        f.close();
        if (ok) {
            QFileInfo fileInfo(s);
            ui -> standby -> setText("Успешно получен файл: " + fileInfo.fileName());
        }
        QFile fg("get.txt");
        fg.remove();
        system("RX.exe");
    }
    if (!QFileInfo("send.txt").exists() & sended) {
        ui -> standby -> setText("Успешно отправлен файл: " + QFileInfo(ui -> l_filename -> text()).fileName());
        sended = false;
    }
}

void Widget::slot_getcom() {
    QFile f("com.txt");
    f.open(QIODevice::ReadOnly);
    QTextStream stream(&f);
    stream.setAutoDetectUnicode(true);
    QString s = "", res;
    bool ok = true;
    while (stream.readLineInto(&s)) {
        if (stream.status() != QTextStream::Ok) {
            QMessageBox MessageBox;
            MessageBox.setWindowTitle("Ошибка чтения файла");
            MessageBox.setText("Ошибка во время чтения файла!");
            MessageBox.setInformativeText("Возможно файл недоступен для чтения или повреждён");
            MessageBox.setIcon(QMessageBox::Warning);
            MessageBox.exec();
            ok = false;
            break;
        }
        if (s != "") res = s;
    }
    f.close();
    if (ok) {
        ui -> comp -> setText("COM-порт: " + res);
    }
}

void Widget::slot_openfile() {
    QString dir = QDir::homePath();
    QString filter = "All Files (*.*)";
    QString fileName = QFileDialog::getOpenFileName(this, "Открыть файл", dir, filter, &filter);
    ui -> l_filename -> setText(fileName);
    slot_time();
}

void Widget::slot_time() {
    QFileInfo fileInfo(ui -> l_filename -> text());
    int secs = fileInfo.size() * 8 / speed;
    QString s = QString("Примерное время передачи составит: %1 секунд").arg(secs);
    ui -> info_label -> setText(s);
}

void Widget::slot_speed() {
    speed = ui -> speeds -> currentText().toInt();
    slot_time();
}

void Widget::slot_enter() {
    QFileInfo fileInfo(ui -> l_filename -> text());
    if (fileInfo.exists()) {
        slot_time();
    } else {
        ui -> info_label -> setText("Примерное время передачи составит:");
    }
}

Widget::~Widget() {delete ui;}
