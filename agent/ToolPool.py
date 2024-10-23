"""
@Function:
@Author : ZhangPeiCheng
@Time : 2024/12/6 11:19
"""


class ToolPool:
    def __init__(self,tool_pool_ip,tool_pool_port):
        # in one session, all the agent will share the same set of tool
        self.tool_pool_ip = tool_pool_ip
        self.tool_pool_port = tool_pool_port
        try:
            self.test_connection()
        except:
            print("tool pool connection fail!")
    def test_connection(self):
        # test the conn between the ComToolPool

        pass
    def gain_summary(self):
        # gain the config and summary of the tool pool
        # the config can gain from the orangeDB

        pass
    def search_tool(self,tool_description):
        # search the tool by the tool_description

        pass

    def call_tool(self):

        pass
