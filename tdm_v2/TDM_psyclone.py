"""
25.01.18
Author 
    david@iiim.is

About
The task dialog(ue) manager [TDM] to psyclone setup. The manger is initialized
within this function and controlled via psyclone with messaging. 
"""

import TDM
import cmsdk2

global api
api = None


def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize the TDM by calling an instance of object TDM
    _TDM = TDM.TDM(api=api)

    # TODO: Add functionality and connectors to the psycrank

    while api.shouldContinue():
        msg = None
        msg = api.wautForNewMessage(20)

        # Process is as follows, once we meet a criteria of starting 
        # encounter (e.g. person found, person dist < 3m, facing person)
        # start by greating. 
        # Then move onto getting a task

        if _TDM.check_for_person():
            if _TDM.start_name("greet"):
                _TDM.start_name("get_objective")
            
            # If person gets lost
            _TDM.reset_TDM()




