#ifndef XMLPARSING_H
#define XMLPARSING_H
#include <QString>
#include <QVector>
#include <QXmlStreamReader>
#include "demolitionstage.h"
class XMLReader
{
    QVector<demolitionStage> allDemStage;
public:
    /*explicit*/ XMLReader(QString pathToXML);
    QVector<demolitionStage> getDemStage();
    void ParseStage(QXmlStreamReader& xml, demolitionStage& demStage , int &i);
    void ParseTypeOfDemolition(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseNuclides(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseDR(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseARF(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseLPF(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseRF(QXmlStreamReader& xml, demolitionStage& demStage);

    QString ParseValue(QXmlStreamReader& xml, demolitionStage& demStage,QString str);
    QString ParseValueWithAttr(QXmlStreamReader& xml, QVector<float>& ,QVector<float>&,QString NameFather, QString str, QString attr);

    ~XMLReader();
};

#endif // XMLPARSING_H
