import datetime
import constants
import threading

def enum(**enums):
    return type('Enum', (), enums)


UrgeState = enum(IHAVE=1,
		IGIVE=2,
		IACCEPT=3,
		OTHERHAS=4,
		OTHERGIVES=5,		
		OTHERACCEPTS=6,
		NONE=7)

DIALOGON = False

def reset():
    global IWANTTURN
    global OTHERWANTSTURN
    global IAMDONE
    global IAMTALKING
    global m_urgestate
    global m_time_last_have
    global m_time_now
    IWANTTURN = False
    OTHERWANTSTURN = False
    IAMTALKING = False
    IAMDONE = False
    m_urgestate = UrgeState.NONE
    m_time_last_have = datetime.datetime.now
    m_time_now = datetime.datetime.now


m_connected = True
m_moduleID = 'P1' # Robot is P1

m_strModuleIDSuffix = "."+str(m_moduleID)
m_strModuleIDPrefix = str(m_moduleID)+"."
m_iLastSpeaker = 'P2'

#shutdown;
debug=True
m_bHasSomethingToSay = False

def printurgestate():
    global m_urgestate
    if m_urgestate == UrgeState.IHAVE:
        api.logPrint("current state: IHAVE")
    elif m_urgestate == UrgeState.IGIVE:
        api.logPrint("current state: IGIVE")
    elif m_urgestate == UrgeState.IACCEPT:
        api.logPrint("current state: IACCEPT")
    elif m_urgestate == UrgeState.OTHERHAS:
        api.logPrint("current state: OTHERHAS")
    elif m_urgestate == UrgeState.OTHERGIVES:
        api.logPrint("current state: OTHERGIVES")
    elif m_urgestate == UrgeState.OTHERACCEPTS:
        api.logPrint("current state: OTHERACCEPTS")
    
def post(message,api):
    api.logPrint(1, "$$POST " + message)
    outMsg = cmsdk.DataMessage()
    api.postOutputMessage(message, outMsg)

def postStop(api):
    global m_urgestate
    setUrgeState(UrgeState.OTHERHAS);
    post("OtherHasTurn",api);
    post("AudioPause",api);

def setUrgeState(state):
    global m_urgestate
    api.logPrint(1, "*_*_*_*_*_*_*_" + str(state) +"_*_*_*_*_*_*_*_*_*")
    m_urgestate = state

def giveturn(api): 
    global IAMDONE
    global m_urgestate

    if (m_urgestate == UrgeState.IHAVE or OTHERWANTSTURN):
        if (debug):
            api.logPrint(1, "                                        --giveturn---")
        m_dUrgeLevel = 0;	        
        setUrgeState(UrgeState.IGIVE);
        post("IGiveTurn",api)  #Todo: debug
#        initializeTimer();
#        m_time_last_give = datetime.datetime.now;	
        IAMDONE = False;
        return True;
    else:
        if (debug):
            api.logPrint(1, "                                        cannot give")
            printurgestate
        return True;

def otheraccepts(api): 
    global m_urgestate
    if (debug):
        api.logPrint(1, "                                        **OTHERACCEPTS**")
    setUrgeState(UrgeState.OTHERACCEPTS);
    setUrgeState(UrgeState.OTHERHAS);
    post("OtherAcceptsTurn",api);  #Todo: debug	
    post("OtherHasTurn",api);  #Todo: debug	

def othergives(api):
    setUrgeState(UrgeState.OTHERGIVES)
    post("OtherGivesTurn",api)
    threading.Timer(0.5, iaccept, [api]).start()

def iaccept(api):    
    global m_urgestate
    if(m_urgestate == UrgeState.OTHERGIVES):
        if (debug):
            api.logPrint(1, "                                        **I ACCEPT**")
        setUrgeState(UrgeState.IACCEPT);
        post("IAcceptTurn",api);
    #postPlay("on accept");

def getperson(messagetype):
    return messagetype.rpartition('.')[0]

def messageloop(msg,api):
    global m_urgestate
    global IAMDONE
    global IAMTALKING
    global m_iLastSpeaker
    global DIALOGON
    if msg is not None:
        messageContent = "" #Todo how do I get content?
        messagetype = api.getCurrentTriggerName()
        sender = ""
        time_ms = msg.getCreatedTime()
        if messagetype == "DialogOn":
            DIALOGON = True
            reset()
            othergives(api)
        elif messagetype == "DialogOff":
            DIALOGON = False
            setUrgeState(UrgeState.NONE);  
        if DIALOGON:  
            if messagetype == constants.MSG_ALL_QUIT:
                exit()                                   
            elif messagetype == constants.MSG_CG_HAVESOMETHINGTOSAY:
                if (messageContent.getField("value").equalsIgnoreCase("True")): #Todo: get param
                    m_bHasSomethingToSay = True
                else:
                    m_bHasSomethingToSay = False
            elif messagetype == "StoppedSpeaking":                
                if (not IAMTALKING):
                    giveturn(api)    
                else:
                    IAMDONE = True
            elif messagetype == "SpeechOnOutput":
                person = getperson(messagetype)       
                m_iLastSpeaker = person;
                IAMTALKING = True;
                if (m_urgestate == UrgeState.NONE or m_urgestate == UrgeState.IACCEPT or m_urgestate == UrgeState.OTHERGIVES):
                    if (debug):
                        api.logPrint(1, " **IHAVE***")
                    setUrgeState(UrgeState.IHAVE)
                    IWANTTURN = False
                    m_time_last_have = time_ms;
                    post("IHaveTurn",api) #Todo post  
            elif messagetype == "SpeechOnInput":              
                if (m_urgestate == UrgeState.IHAVE):
                    OTHERWANTSTURN = True;
                    post("OtherWantsTurn",api) #Todo post
                elif m_urgestate == UrgeState.IGIVE:
                    otheraccepts(api)
                elif (m_urgestate == UrgeState.OTHERGIVES):
                    postStop(api)
                elif (m_urgestate == UrgeState.IACCEPT):
                    postStop(api);
            elif messagetype == "SpeechOffOutput":
                person = getperson(messagetype)
                IAMTALKING = False;              
                if (IAMDONE):
                    giveturn(api);            
            elif messagetype == "SpeechOffInput":
                person = getperson(messagetype)                
                if m_urgestate == UrgeState.OTHERHAS:                    
                    othergives(api)
            elif "Other-gives-turn" in messagetype:
                if m_urgestate == UrgeState.OTHERHAS:
                    if (m_bDebug):
                        api.logPrint(1, "**OTHERGIVES** EXTERNAL")
                    setUrgeState(UrgeState.OTHERGIVES);
            elif (messagetype == constants.MSG_PA_OVERLAP_START):
                x = rand();
                i = x%2;
        
                diff = m_time_now-m_time_last_have;
                if (m_iLastSpeaker == m_moduleID):
                    postStop(api)
                else:
                    #raise voice    
                    if (debug):
                        api.logPrint(1, " --- VOLUME UP --- ")
                    vol = {'value': '100'}
                    post(constants.MSG_LOQ_VOLUME,vol)
            elif messagetype == constants.MSG_PA_OVERLAP_STOP:
                vol = {'value': '50'}
                post(constants.MSG_LOQ_VOLUME,api);
            elif "Instruct.Speech.Start" in messagetype:
                if (variables.m_urgestate == UrgeState.OTHERHAS):
                    post("oninstruct",api)

#MD = MainDecider.MainDecider()
#urgetospeak

def PsyCrank(apilink):
    global api
    api = cmsdk.PsyAPI.fromPython(apilink);
    name = api.getModuleName();
    
    api.logPrint(1, "Module name: %s" % name)
    key = api.getParameterInt("Key");
    while (api.shouldContinue()):
        msg = api.waitForNewMessage(20)
        if msg != None:
            messageloop(msg,api)
      

#msgPlayer = cmsdk.MessagePlayer()
#msgPlayer.initRead("C:/Projects/CoCoDist101/Python/Annotate", 0, True)
#while(True):
#    msg = msgPlayer.waitForNextMessage(1000)
#    if msg != None:
#        print("Trigger name: " + msgPlayer.getCurrentTriggerName() + " size: " + str(msg.getSize()) + " at " + cmsdk.PrintTime(msg.getCreatedTime()))
#    else:
#        print("---")
#    messageloop(msg)
  
    
