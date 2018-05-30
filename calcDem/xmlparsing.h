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
    void ParseStage(QXmlStreamReader& xml, demolitionStage& demStage , int i);
    void ParseTypeOfDemolition(QXmlStreamReader& xml, demolitionStage& demStage);
    void ParseNuclides(QXmlStreamReader& xml, demolitionStage& demStage);
    ~XMLReader();
};

#endif // XMLPARSING_H
