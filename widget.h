#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QtWidgets>

QT_BEGIN_NAMESPACE
namespace Ui {class Widget;}
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT
public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
private:
    Ui::Widget *ui;
    QTimer *timer;
    int speed = 300;
    bool sended = false;
    QProcess *send, *get, *com;
private slots:
    void slot_sendfile();
    void slot_openfile();
    void slot_timer();
    void slot_getcom();
    void slot_time();
    void slot_speed();
    void slot_enter();
    void slot_getfile();
    void slot_rx();
    void slot_chat();
    void slot_github();
};
#endif // WIDGET_H
