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
    float ARF;
    float ARFdrop;
    float ARFsize;
    float LPF;
    float RF;


    demolitionStage();
    void clean();
    ~demolitionStage();
};

#endif // DEMOLITIONSTAGE_H
