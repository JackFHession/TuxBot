#include <QApplication>
#include <QMainWindow>
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QComboBox>
#include <QMessageBox>
#include <QDialog>

class MyWindow : public QMainWindow {
    Q_OBJECT

public:
    MyWindow(QWidget *parent = nullptr);
    ~MyWindow();

private slots:
    void handleInput();
    void updateMode(const QString &modeText);
    void selectMode();

private:
    QTextEdit *textEdit;
    QLineEdit *inputField;
    QComboBox *modeCombo;
    QString mode;

    void audioMode();
    void processInput(const QString &text);
    void setMode(const QString &modeText); // Private member function
};

MyWindow::MyWindow(QWidget *parent) : QMainWindow(parent) {
    setWindowTitle("Janex Assistant");
    setGeometry(100, 100, 600, 400);
    setMinimumSize(600, 400);

    textEdit = new QTextEdit(this);
    textEdit->setGeometry(10, 10, 580, 300);
    textEdit->setStyleSheet("background-color: black; color: white;");
    textEdit->setReadOnly(true);

    inputField = new QLineEdit(this);
    inputField->setGeometry(10, 320, 400, 30);
    connect(inputField, &QLineEdit::returnPressed, this, &MyWindow::handleInput);

    modeCombo = new QComboBox(this);
    modeCombo->setGeometry(420, 320, 170, 30);
    modeCombo->addItems({"Text", "Audio"});
    connect(modeCombo, QOverload<const QString &>::of(&QComboBox::currentTextChanged), this, &MyWindow::updateMode);

    mode = "text";
}

MyWindow::~MyWindow() {
    delete textEdit;
    delete inputField;
    delete modeCombo;
}

void MyWindow::handleInput() {
    QString text = inputField->text();
    textEdit->append("You: " + text);
    inputField->clear();

    processInput(text);
}

void MyWindow::updateMode(const QString &modeText) {
    setMode(modeText); // Call setMode to update mode
    textEdit->append("Communication mode switched to " + modeText);
}

void MyWindow::selectMode() {
    // Implement ModeDialog logic here
}

void MyWindow::audioMode() {
    // Implement audio mode logic here
}

void MyWindow::processInput(const QString &text) {
    if (mode == "audio") {
        // Call audioMode() method
    } else if (mode == "text") {
        // Handle text input
    }
}

void MyWindow::setMode(const QString &modeText) {
    mode = modeText.toLower();
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MyWindow window;

    if (argc > 1) {
        QString mode = argv[1];
        window.setMode(mode); // Call setMode to set initial mode
    }

    window.show();
    return app.exec();
}

#include "main.moc"
