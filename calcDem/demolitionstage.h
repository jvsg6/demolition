#ifndef DEMOLITIONSTAGE_H
#define DEMOLITIONSTAGE_H
#include <QVector>



class demolitionStage
{
    public:
    int stageId;

    int typeDemolition;
    float DR;

    struct NuclidesStruct
    {
        QVector<QString> nuclidesName;
        QVector<float> nuclidesValue;
    }Nuclides;

    struct ARFstruct
    {
        float ARFdem;
        float ARFdrop;
        float ARFsize;
        float ARFWet;
        float ARFWind;
        float ARFDens;
        float ARFH;
    } ARF;

    struct LPFstruct
    {
        float LPFdem;
        float LPFdrop;
        QVector<float> LPFdropValue;
        QVector<float> LPFdropSize;
    }LPF;

    struct RFstruct
    {
        float RFdem;
        float RFdrop;
        QVector<float> RFdropValue;
        QVector<float> RFdropSize;
    }RF;





    demolitionStage();
    void clean();
    ~demolitionStage();
};


#endif // DEMOLITIONSTAGE_H


