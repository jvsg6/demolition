#include <QCoreApplication>
#include <iostream>
#include <QString>
#include "xmlparsing.h"
#include "demolitionstage.h"
using namespace std;
int main()
{
    demolitionStage ds;
    cout<<ds.ARF<<endl;
    QString pathToXML(".\\inputData.xml");
    XMLReader aa(pathToXML);
    cout << "Hello World!" << endl;
    return 0;
}
