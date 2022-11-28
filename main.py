# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import json
import re
from collections import OrderedDict

def setShotInfo():
    basePath = os.path.dirname(os.path.abspath(__file__))
    jsonFile =  os.path.join(basePath, 'setShotInfo.json')  
            
    PRJNAME = ""
    CKEY = ""
    CONF_PATH = ""
    if "PRJNAME" in os.environ :
        PRJNAME = os.environ['PRJNAME']
    if "CKEY" in os.environ :
        CKEY = os.environ['CKEY']
    if "CONF_PATH" in os.environ :
        CONF_PATH = os.environ['CONF_PATH']

    if CONF_PATH != "" :
        path = os.path.abspath( os.path.join( CONF_PATH, CKEY,"setShotInfo") )
        if os.path.isdir(path):
            jsonFile =  os.path.join(path, PRJNAME+'.json')

    shotInfo = cmds.ls(type="clgShotInfo")
    if shotInfo :
        cam = cmds.listConnections(shotInfo[0]+".cameras")
        if cam :
            camShape = cmds.listRelatives(cam[0],s=True)[0]

            presetDic = json.load(open(jsonFile), object_pairs_hook=OrderedDict)
   
            cmds.setAttr(shotInfo[0]+".referenceAperture",presetDic['referenceAperture'])
            cmds.setAttr(shotInfo[0]+".horizontalFilmAperture",presetDic['filmbackAperture'][0])
            cmds.setAttr(shotInfo[0]+".verticalFilmAperture",presetDic['filmbackAperture'][1])

            cmds.setAttr(shotInfo[0]+".filmGateMaskColor",*presetDic['filmGateMaskColor'])
            cmds.setAttr(shotInfo[0]+".filmGateMaskTrans",presetDic['filmGateMaskTrans'])
            cmds.setAttr(shotInfo[0]+".renderGateLineColor",*presetDic['renderGateLineColor'])
            cmds.setAttr(shotInfo[0]+".renderGateLineTrans",presetDic['renderGateLineTrans'])

            isVray = ( cmds.getAttr( u'defaultRenderGlobals.currentRenderer' ) == u'vray' )
            width = cmds.getAttr( u'vraySettings.width' ) if isVray else cmds.getAttr( u'defaultResolution.width' )
            height = cmds.getAttr( u'vraySettings.height' ) if isVray else cmds.getAttr( u'defaultResolution.height' )

            fWidth = presetDic["finalResolution"][0]
            fHeight = presetDic["finalResolution"][1]

            hfa = cmds.getAttr( u'%s.horizontalFilmAperture' % camShape )
            vfa = cmds.getAttr( u'%s.verticalFilmAperture' % camShape )
            cmds.setAttr(u'%s.horizontalRenderGate' % shotInfo[0] ,(float(fWidth) / float(width)) * hfa )
            cmds.setAttr(u'%s.verticalRenderGate' % shotInfo[0] ,(float(fHeight) / float(height)) * vfa )

            for key, v in presetDic['text'].iteritems():
                num = int(key)
                value = v['textType']
                cmds.setAttr(shotInfo[0]+".text[%s].textType"%(num),value)

                filePath = cmds.file(q=True,expandName=True)
                textStr = v['textStr']
                filePattern = re.compile( presetDic['filePresetPattern'] )
                fileSearch = filePattern.search( filePath )
                if fileSearch :
                    buf = fileSearch.groupdict()
                    for key, value in buf.iteritems():
                        textStr = textStr.replace("{%s}"%key,buf[key])
                    cmds.setAttr(shotInfo[0]+".text[%s].textStr"%(num),textStr,type="string")
                    
                value = v['textAlign']
                cmds.setAttr(shotInfo[0]+".text[%s].textAlign"%(num),value)

                value = v['textVAlign']
                cmds.setAttr(shotInfo[0]+".text[%s].textVAlign"%(num),value)

                value = v['textPosition']
                cmds.setAttr(shotInfo[0]+".text[%s].textPosX"%(num),value[0])
                cmds.setAttr(shotInfo[0]+".text[%s].textPosY"%(num),value[1])

                value = v['textPosRel']
                cmds.setAttr(shotInfo[0]+".text[%s].textPosRel"%(num),value)

                value = v['textColor']
                cmds.setAttr(shotInfo[0]+".text[%s].textColor"%(num),*value)

                value = v['textTrans']
                cmds.setAttr(shotInfo[0]+".text[%s].textTrans"%(num),value)

                value = v['textBold']
                cmds.setAttr(shotInfo[0]+".text[%s].textBold"%(num),value)

                value = v['textScale']
                cmds.setAttr(shotInfo[0]+".text[%s].textScale"%(num),value)

                value = v['textSize']
                cmds.setAttr(shotInfo[0]+".text[%s].textSize"%(num),value)