#include "xmlparsing.h"
#include <iostream>
#include <QFile>
#include <QDir>
#include <QXmlStreamReader>
#include <QXmlStreamWriter>
using namespace std;

XMLReader::XMLReader(QString pathToXML)
{
    cout << pathToXML.toStdString() << endl;

}

XMLReader::~XMLReader()
{
    cout << "Bye World!" << endl;
}
