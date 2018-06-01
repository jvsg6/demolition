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



    Nuclides.nuclidesName.erase(Nuclides.nuclidesName.begin(), Nuclides.nuclidesName.end());
    Nuclides.nuclidesValue.erase(Nuclides.nuclidesValue.begin(), Nuclides.nuclidesValue.end());

    ARF.ARFWet = -1.0;
    ARF.ARFWind = -1.0;
    ARF.ARFDens = -1.0;
    ARF.ARFH = -1.0;
    ARF.ARFdem = -1.0;
    ARF.ARFdrop = -1.0;
    ARF.ARFsize = 1.0;

    LPF.LPFdem = -1.0;
    LPF.LPFdrop = -1.0;
    LPF.LPFdropValue.erase(LPF.LPFdropValue.begin(), LPF.LPFdropValue.end());
    LPF.LPFdropSize.erase(LPF.LPFdropSize.begin(), LPF.LPFdropSize.end());

    RF.RFdem = -1.0;
    RF.RFdrop = -1.0;
    RF.RFdropValue.erase(RF.RFdropValue.begin(), RF.RFdropValue.end());
    RF.RFdropSize.erase(RF.RFdropSize.begin(), RF.RFdropSize.end());

}
void demolitionStage::clean()
{

    stageId = -1;
    typeDemolition = 0;
    DR = -1.0;


    Nuclides.nuclidesName.erase(Nuclides.nuclidesName.begin(), Nuclides.nuclidesName.end());
    Nuclides.nuclidesValue.erase(Nuclides.nuclidesValue.begin(), Nuclides.nuclidesValue.end());
    ARF.ARFWet = -1.0;
    ARF.ARFWind = -1.0;
    ARF.ARFDens = -1.0;
    ARF.ARFH = -1.0;
    ARF.ARFdem = -1.0;
    ARF.ARFdrop = -1.0;
    ARF.ARFsize = 1.0;

    LPF.LPFdem = -1.0;
    LPF.LPFdrop = -1.0;
    LPF.LPFdropValue.erase(LPF.LPFdropValue.begin(), LPF.LPFdropValue.end());
    LPF.LPFdropSize.erase(LPF.LPFdropSize.begin(), LPF.LPFdropSize.end());

    RF.RFdem = -1.0;
    RF.RFdrop = -1.0;
    RF.RFdropValue.erase(RF.RFdropValue.begin(), RF.RFdropValue.end());
    RF.RFdropSize.erase(RF.RFdropSize.begin(), RF.RFdropSize.end());
}
demolitionStage::~demolitionStage()
{

}

