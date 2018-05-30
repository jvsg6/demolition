#include "demolitionstage.h"
#include <QVector>
#include <Qstring>
#include <iostream>
using namespace std;

demolitionStage::demolitionStage()
{
    stageId = -1;
    typeDemolition = 0;
    DR = -1.0;
    ARF = -1.0;
    ARFdrop = -1.0;
    ARFsize = 1.0;
    LPF = -1.0;
    RF = -1.0;

}
void demolitionStage::clean()
{

}
demolitionStage::~demolitionStage()
{

}
