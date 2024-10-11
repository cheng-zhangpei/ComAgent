"""
@Function: the define of session is like to combine all component
@Author : ZhangPeiCheng
@Time : 2024/10/23 19:45
"""
class ExpertSession:
    def __init__(self,expert,sub_agent,decomposer):
        self.expert = expert
        self.sub_agent = sub_agent
        self.decomposer = decomposer
