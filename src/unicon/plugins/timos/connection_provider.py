__author__ = 'Difu Hu <pyats-support@cisco.com;pyats-support-ext@cisco.com>'

from unicon.bases.routers.connection_provider import BaseSingleRpConnectionProvider
from unicon.eal.dialogs import Dialog

from .statements import (timos_pre_connection_statement_list,
                         timos_auth_other_statement_list,
                         timos_auth_username_password_statement_list,
                         custom_auth_username_password_statements)


class TimosSingleRpConnectionProvider(BaseSingleRpConnectionProvider):

    def init_handle(self):
        con = self.connection
        con._is_connected = True
        con.state_machine.go_to('mdcli',
                                self.connection.spawn,
                                context=con.context,
                                prompt_recovery=self.prompt_recovery,
                                timeout=con.connection_timeout)
        self.execute_init_commands()

    def get_connection_dialog(self):
        con = self.connection
        custom_user_pw_stmt = custom_auth_username_password_statements(
            con.settings.LOGIN_PROMPT,
            con.settings.PASSWORD_PROMPT
        )
        return con.connect_reply \
               + Dialog(timos_pre_connection_statement_list
                        + timos_auth_other_statement_list
                        + custom_user_pw_stmt
                        + timos_auth_username_password_statement_list)
