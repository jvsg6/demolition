#include <QCoreApplication>
#include <iostream>
#include <QString>
#include "xmlparsing.h"
#include "demolitionstage.h"
#include <QDir>
#include <cmath>
using namespace std;
float calcAFR(demolitionStage::ARFstruct & drop)
{
    if (drop.ARFdrop == -1.0)
    {
        if (drop.ARFWind != -1.0)
        {
            return (1.6e-06)*pow(drop.ARFWind/2.2, 1.3)/pow(drop.ARFWet/2, 1.4)*drop.ARFsize;
        }
        else
        {
            return (2.0e-11)*980.0*drop.ARFDens*drop.ARFH*drop.ARFsize;
        }
    }
    else
    {
        return drop.ARFdrop*drop.ARFsize;
    }

}

float calcLPF_RF(demolitionStage::LPFstruct & dropLPF, demolitionStage::RFstruct & dropRF)
{
    if (dropLPF.LPFdrop != -1.0)
    {
        return dropLPF.LPFdrop*dropRF.RFdrop;
    }
    else
    {
        float sum = 0.0;
        for (int i = 0 ; i<dropLPF.LPFdropSize.size(); i++)
            sum += dropLPF.LPFdropValue[i]*dropRF.RFdropValue[i];
        return sum;
    }
}


int main()
{
    demolitionStage ds;
    cout<<ds.ARF.ARFdem<<endl;
    //QDir::current().absolutePath();
    QString path = QDir::current().absolutePath();
    QString pathToInput = path + "/inputData.xml";
    cout<<path.toStdString()<<endl;
    QString pathToXML(pathToInput);
    XMLReader readXML(pathToXML);
    QVector<demolitionStage> demAll = readXML.getDemStage();
    QVector<float> STdemArr;
    QVector<float> STdropArr;
    for (int i = 0 ; i<demAll.size(); i++)
    {   cout<<endl<<"--------------------------------------------------------------------------------"<<endl;
        cout<<"Calculate stage "<<demAll[i].stageId<<endl<<endl;
        cout<<"Calculate demolition's part"<<endl;
        float STdem = 0.0;
        float sumAct = 0.0;
        for (int j = 0 ; j<demAll[i].Nuclides.nuclidesName.size(); j++)
        {
            sumAct += demAll[i].Nuclides.nuclidesValue[j];
        }

        STdem = sumAct*demAll[i].DR*demAll[i].ARF.ARFdem*demAll[i].LPF.LPFdem*demAll[i].RF.RFdem;
        STdemArr.append(STdem);

        cout<<"Calculate drop's part"<<endl;
        float STdrop = 0.0;
        float ARFdrop = calcAFR(demAll[i].ARF);
        float LPF_RFdrop = calcLPF_RF(demAll[i].LPF, demAll[i].RF);
        STdrop = sumAct*demAll[i].DR*ARFdrop*LPF_RFdrop;
        STdropArr.append(STdrop);

    }
    cout<<endl<<"--------------------------------------------------------------------------------"<<endl;
    cout<<"Results:"<<endl;
    for (int i = 0 ; i<demAll.size(); i++)
    {
        cout<<"\tStage "<<i<<endl;
        cout<<"\t\tDemolition ";
        cout<< STdemArr[i]<<endl;
        cout<<"\t\tDrop ";
        cout<< STdropArr[i]<<endl;
    }
    return 0;

}
