#include "xmlparsing.h"
#include <iostream>
#include <QFile>
#include <QDir>
#include <QXmlStreamReader>
#include <QXmlStreamWriter>
#include <typeinfo>
#include "demolitionstage.h"
using namespace std;

XMLReader::XMLReader(QString pathToXML)
{
    int i=0;
    cout << pathToXML.toStdString() << endl;
    QFile* file = new QFile(pathToXML);
    if(!file->open(QIODevice::ReadOnly | QIODevice::Text))
    {
    cout<<"I cant open"<<endl;
    return;
    }
    QXmlStreamReader xml(file);
    demolitionStage demStage;
    while(!xml.atEnd() && !xml.hasError())
    {

        QXmlStreamReader::TokenType token = xml.readNext();
        if(token == QXmlStreamReader::StartDocument)
        {
        continue;
        }
        if(token == QXmlStreamReader::StartElement)
        {
            if (xml.name() == "stageNumber")
            {
                demolitionStage demStage;
                //cout<<"Stage number ";
                i++;
                this->ParseStage(xml, demStage, i);
            }
            if(xml.name() == "typeOfDemolition")
            {
                this->ParseTypeOfDemolition(xml, demStage);
            }
            /*QString str = xml.text().toString();
            if (str.contains("\\n"))
            {
                cout<<"Wow"<<endl;
            }*/
            if(xml.name() == "nuclides")
            {
                this->ParseNuclides(xml, demStage);
                allDemStage.append(demStage);
            }
        }

    }


}
void XMLReader::ParseStage(QXmlStreamReader& xml, demolitionStage &demStage, int i)
{
    xml.readNext();
    cout<<(xml.text().toString()).toStdString()<<endl;
    demStage.stageId = i;
    xml.readNext();

}
void XMLReader::ParseTypeOfDemolition(QXmlStreamReader& xml, demolitionStage& demStage)
{
    cout<<xml.attributes().value("typeDem").toString().toInt()<<endl;
    demStage.typeDemolition = xml.attributes().value("typeDem").toString().toInt();
    xml.readNext();
    cout<<(xml.text().toString()).toStdString()<<endl;
    xml.readNext();

}
void XMLReader::ParseNuclides(QXmlStreamReader& xml, demolitionStage& demStage)
{
    xml.readNext();
    xml.readNext();
    while(xml.name().toString() != "nuclides")
    {
        if (xml.name().toString() == "activity")
        {
            cout<<(xml.text().toString()).toStdString()<<endl;
            demStage.nuclidesName.append(xml.attributes().value("nuclide").toString());
            xml.readNext();
            demStage.nuclidesValue.append(xml.text().toString().toFloat());
            xml.readNext();
            xml.readNext();
        }
        xml.readNext();
    }
}

QVector<demolitionStage> XMLReader::getDemStage()
{
    return allDemStage;
}
XMLReader::~XMLReader()
{
    cout << "Bye World!" << endl;
}
