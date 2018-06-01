QT += core xml
QT -= gui

CONFIG += c++11

TARGET = calcDem
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    xmlparsing.cpp \
    demolitionstage.cpp

HEADERS += \
    xmlparsing.h \
    demolitionstage.h
INCLUDEPATH += $$PWD
