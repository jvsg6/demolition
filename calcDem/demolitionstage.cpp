#include "demolitionstage.h"
#include <QVector>
#include <Qstring>
#include <iostream>
using namespace std;
demolitionStage::demolitionStage()
{
    std::cout<<"I am here"<<std::endl;
    int stageId = -1;
    QVector<QString> nuclidesName;
    QVector<float> nuclidesValue;
    int typeDemolition = 0;
    float DR = -1.0;
    float ARF = -1.0;
    float ARFdrop = -1.0;
    float ARFsize = 1.0;
    float LPF = -1.0;
    float RF = -1.0;

}
demolitionStage::~demolitionStage()
{

}
