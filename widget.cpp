#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) : QWidget(parent), ui(new Ui::Widget) {
    ui->setupUi(this);
    setWindowTitle("Project Restavration");
    connect(ui -> choose_file, &QPushButton::released, this, &Widget::slot_openfile);
    connect(ui -> speeds, &QComboBox::currentTextChanged, this, &Widget::slot_speed);
    connect(ui -> l_filename, &QLineEdit::textChanged, this, &Widget::slot_enter);
    connect(ui -> send_file, &QPushButton::released, this, &Widget::slot_sendfile);
    connect(ui -> get_file, &QPushButton::released, this, &Widget::slot_getfile);
    connect(ui -> chat, &QPushButton::released, this, &Widget::slot_chat);
    connect(ui -> github, &QPushButton::released, this, &Widget::slot_github);
    timer = new QTimer();
    connect(timer, &QTimer::timeout, this, &Widget::slot_timer);
    timer -> start(1000); // 1 sec
    com = new QProcess(this);
    com -> start("COM.exe");
    com -> waitForFinished(-1);
    send = new QProcess(this);
    get = new QProcess(this);
    slot_getcom();
}

void Widget::slot_github() {
    system("start https://github.com/K1ri4/Project-Restavration");
}

void Widget::slot_chat() {
    system("FDC.exe");
}

void Widget::slot_getfile() {
    ui -> standby -> setText("Приём файла...");
    slot_rx();
}

void Widget::slot_rx() {
    system("RX.exe");
}

void Widget::slot_sendfile() {
    ui -> standby -> setText("Отправка файла...");
    QString fileName = "send.txt";
    if (!fileName.isEmpty()) {
        QFile f(fileName);
        f.open(QIODevice::WriteOnly | QFile::Truncate);
        QTextStream stream(&f);
        stream.setAutoDetectUnicode(true);
        stream << ui -> l_filename -> text();
        f.close();
    }
    sended = true;
    system("TX.exe");
}

void Widget::slot_timer() {
    QString fileName = "get.txt";
    if (QFileInfo("get.txt").exists()) {
        QFile f(fileName);
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
            QFileInfo fileInfo(res);
            qDebug() << res;
            qDebug() << fileInfo.fileName();
            ui -> standby -> setText("Успешно получен файл: " + fileInfo.fileName());
        }
        QFile f1("get.txt");
        f.remove();
    }
    if (!QFileInfo("send.txt").exists() & sended) {
        ui -> standby -> setText("Успешно отправлен файл: " + QFileInfo(ui -> l_filename -> text()).fileName());
        sended = false;
        ui -> l_filename -> setText("");
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
    fileName.replace("/", "\\");
    ui -> l_filename -> setText(fileName);
    slot_time();
}

void Widget::slot_time() {
    QFileInfo fileInfo(ui -> l_filename -> text());
    if (fileInfo.exists()) {
        int secs = fileInfo.size() * 8 / speed;
        QString s = QString("Примерное время передачи составит: %1 секунд").arg(secs);
        ui -> info_label -> setText(s);
    } else {
        ui -> info_label -> setText("Примерное время передачи составит:");
    }
}

void Widget::slot_speed() {
    speed = ui -> speeds -> currentText().toInt();
    QString fileName = "speed.txt";
    if (!fileName.isEmpty()) {
        QFile f(fileName);
        f.open(QIODevice::WriteOnly | QFile::Truncate);
        QTextStream stream(&f);
        stream.setAutoDetectUnicode(true);
        stream << ui -> speeds -> currentText();
        f.close();
    }
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
