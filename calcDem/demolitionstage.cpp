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
    ARFdem = -1.0;
    ARFdrop = -1.0;
    ARFsize = 1.0;
    LPF = -1.0;
    RF = -1.0;
    nuclidesName.erase(nuclidesName.begin(), nuclidesName.end());
    nuclidesValue.erase(nuclidesValue.begin(), nuclidesValue.end());
    ARFWet = -1.0;
    ARFWind = -1.0;
    ARFDens = -1.0;
    ARFH = -1.0;
    LPFdropValue.erase(LPFdropValue.begin(), LPFdropValue.end());
    LPFdropSize.erase(LPFdropSize.begin(), LPFdropSize.end());
    RFdropValue.erase(RFdropValue.begin(), RFdropValue.end());
    RFdropSize.erase(RFdropSize.begin(), RFdropSize.end());

}
void demolitionStage::clean()
{

    stageId = -1;
    typeDemolition = 0;
    DR = -1.0;
    ARFdem = -1.0;
    ARFdrop = -1.0;
    ARFsize = 1.0;
    LPF = -1.0;
    RF = -1.0;
    nuclidesName.erase(nuclidesName.begin(), nuclidesName.end());
    nuclidesValue.erase(nuclidesValue.begin(), nuclidesValue.end());
    ARFWet = -1.0;
    ARFWind = -1.0;
    ARFDens = -1.0;
    ARFH = -1.0;
    LPFdropValue.erase(LPFdropValue.begin(), LPFdropValue.end());
    LPFdropSize.erase(LPFdropSize.begin(), LPFdropSize.end());
    RFdropValue.erase(RFdropValue.begin(), RFdropValue.end());
    RFdropSize.erase(RFdropSize.begin(), RFdropSize.end());
}
demolitionStage::~demolitionStage()
{

}
