"""
Module:
    unicon.plugins.ironware.state_machine

Author:
    James Di Trapani <james@ditrapani.com.au> - https://github.com/jamesditrapani

Description:
    Enables connection handle to transition into different router states, specific 
    to the Ironware NOS.
"""

__author__ = "James Di Trapani <james@ditrapani.com.au>"

from unicon.statemachine import Path
from unicon.eal.dialogs import Dialog
from unicon.plugins.generic.statemachine import GenericSingleRpStateMachine
from . import statements as stmts


class IronWareSingleRpStateMachine(GenericSingleRpStateMachine):

    def create(self):
        '''
        statemachine class's create() method is its entrypoint. This showcases
        how to setup a statemachine in Unicon. 
        '''
        super().create()

        # remove some known path
        self.remove_path('enable', 'rommon')
        self.remove_path('rommon', 'disable')
        self.remove_state('rommon')

        self.remove_path('disable', 'enable')
        enable = [state for state in self.states if state.name == 'enable'][0]
        disable = [state for state in self.states if state.name == 'disable'][0]
        disable_to_enable = Path(disable,
                                 enable,
                                 'enable',
                                 Dialog([stmts.password_stmt]))
        self.add_path(disable_to_enable)