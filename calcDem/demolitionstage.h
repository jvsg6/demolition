#ifndef DEMOLITIONSTAGE_H
#define DEMOLITIONSTAGE_H
#include <QVector>



class demolitionStage
{
    public:
    int stageId;
    QVector<QString> nuclidesName;
    QVector<float> nuclidesValue;
    int typeDemolition;
    float DR;
    float ARFdem;
    float ARFdrop;
    float ARFsize;
    float ARFWet;
    float ARFWind;
    float ARFDens;
    float ARFH;
    QVector<float> LPFdropValue;
    QVector<float> LPFdropSize;
    QVector<float> RFdropValue;
    QVector<float> RFdropSize;
    float LPF;
    float RF;


    demolitionStage();
    void clean();
    ~demolitionStage();
};

#endif // DEMOLITIONSTAGE_H
