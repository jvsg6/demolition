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
                //cout<<"Stage number ";
                i++;
                this->ParseStage(xml, demStage, i);
            }
            if (xml.name() == "typeOfDemolition")
            {
                this->ParseTypeOfDemolition(xml, demStage);
            }
            /*QString str = xml.text().toString();
            if (str.contains("\\n"))
            {
                cout<<"Wow"<<endl;
            }*/
            if (xml.name() == "nuclides")
            {
                this->ParseNuclides(xml, demStage);
            }
            if (xml.name() == "DR")
            {
                this->ParseDR(xml, demStage);
            }
            if (xml.name() == "ARF")
            {
                this->ParseARF(xml, demStage);
            }
            if (xml.name() == "LPF")
            {
                this->ParseLPF(xml, demStage);
            }
            if (xml.name() == "RF")
            {
                this->ParseRF(xml, demStage);
                allDemStage.append(demStage);
                demStage.clean();
            }
        }

    }
    QVector<demolitionStage> aaa = this->getDemStage();
    QVector<demolitionStage> bbb = this->getDemStage();


}
void XMLReader::ParseStage(QXmlStreamReader& xml, demolitionStage &demStage, int& i)
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
void XMLReader::ParseDR(QXmlStreamReader& xml, demolitionStage& demStage)
{
    xml.readNext();
    demStage.DR = xml.text().toString().toFloat();
    xml.readNext();
}
void XMLReader::ParseARF(QXmlStreamReader& xml, demolitionStage& demStage)
{
    xml.readNext();
    xml.readNext();
    while(xml.name().toString() != "ARF")
    {
        if (xml.name() == "ARFdem")
        {
            demStage.ARFdem = (this->ParseValue(xml, demStage, "ARFdem")).toFloat();
        }
        if (xml.name() == "ARFsize")
        {
            demStage.ARFsize = (this->ParseValue(xml, demStage, "ARFsize")).toFloat();
        }
        if (xml.name() == "ARFdrop")
        {
            if (xml.name() == "Wettering")
            {
                demStage.ARFWet = (this->ParseValue(xml, demStage, "Wettering")).toFloat();
            }
            if (xml.name() == "WindSpeed")
            {
                demStage.ARFWind = (this->ParseValue(xml, demStage, "WindSpeed")).toFloat();
            }
            if (xml.name() == "Density")
            {
                demStage.ARFDens = (this->ParseValue(xml, demStage, "Density")).toFloat();
            }
            if (xml.name() == "Heigh")
            {
                demStage.ARFH = (this->ParseValue(xml, demStage, "Heigh")).toFloat();
            }
        }
        xml.readNext();
    }
}
void XMLReader::ParseLPF(QXmlStreamReader& xml, demolitionStage& demStage)
{
    xml.readNext();
    xml.readNext();
    while(xml.name().toString() != "LPF")
    {
        if(xml.name() == "LPFdem")
        {
            demStage.LPF = (this->ParseValue(xml, demStage, "LPFdem")).toFloat();
        }

        if(xml.name() == "LPFdrop")
        {
            xml.readNext();
            while(xml.name().toString() != "LPFdrop")
            {
                this->ParseValueWithAttr(xml, demStage.LPFdropValue,demStage.LPFdropSize,"LPFdrop", "LPFp", "partSize" );
            }
        }
        xml.readNext();
    }
}
void XMLReader::ParseRF(QXmlStreamReader& xml, demolitionStage& demStage)
{
    xml.readNext();
    xml.readNext();
    while(xml.name().toString() != "RF")
    {
        if(xml.name() == "RFdem")
        {
            demStage.LPF = (this->ParseValue(xml, demStage, "LPFdem")).toFloat();
        }

        if(xml.name() == "RFdrop")
        {
            xml.readNext();
            while(xml.name().toString() != "RFdrop")
            {
                this->ParseValueWithAttr(xml, demStage.RFdropValue,demStage.RFdropSize,"RFdrop", "RFp", "partSize" );
            }
        }
        xml.readNext();
    }
}

QString XMLReader::ParseValue(QXmlStreamReader& xml, demolitionStage& demStage, QString str)
{
    QString val = "";
    if ((xml.name()).toString() == str)
    {
            xml.readNext();
            val = xml.text().toString();
            xml.readNext();
    }
    if (val == "")
    {
        QString s = "Cant find ";
        cout<<s.toStdString()<<str.toStdString()<<endl;
        return "NotFound";
    }
    else
    {
        return val;
    }
}
QString XMLReader::ParseValueWithAttr(QXmlStreamReader& xml, QVector<float> &Value, QVector<float> &Attribute,QString NameFather, QString str, QString attr)
{

    QString val = "";
    xml.readNext();
    if ((xml.name()).toString() == str)
    {
        while (xml.name().toString() != NameFather)
        {
            bool find = false;
            if (xml.name().toString() == str)
            {
                find = true;
                bool flag;
                QString a = QString(val);
                cout<<a.toStdString()<<endl;
                flag = a.contains(".", Qt::CaseInsensitive) or a.contains("0", Qt::CaseInsensitive) or a.contains("1", Qt::CaseInsensitive);
                cout<<flag<<endl;
                    if (flag)
                    {
                        xml.readNext();
                        val = xml.text().toString();
                        xml.readNext();
                    }
                    else
                    {
                        Attribute.append((xml.attributes().value(attr).toString()).toFloat());
                        xml.readNext();
                        Value.append((xml.text().toString()).toFloat());
                        val = xml.text().toString();
                        xml.readNext();
                    }
            }
            if (!find)
            {
                xml.readNext();
            }

        }
    }
    if (val == "")
    {
        QString s = "Cant find ";
        cout<<s.toStdString()<<str.toStdString()<<endl;
        return "NotFound";
    }
    else
    {
        return val;
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
