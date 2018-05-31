#include <QCoreApplication>
#include <iostream>
#include <QString>
#include "xmlparsing.h"
#include "demolitionstage.h"
#include <QDir>
using namespace std;
int main()
{
    demolitionStage ds;
    cout<<ds.ARFdem<<endl;
    //QDir::current().absolutePath();
    QString path = QDir::current().absolutePath();
    QString pathToInput = path + "/inputData.xml";
    cout<<path.toStdString()<<endl;
    QString pathToXML(pathToInput);
    XMLReader aa(pathToXML);
    cout << "Hello World!" << endl;
    return 0;

}
