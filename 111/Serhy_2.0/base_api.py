'''
Created on Jun 21, 2016

@author: Serhy
'''

import unittest
import requests
import xmltodict


class BaseApi(unittest.TestCase):
    '''
    classdocs
    '''
    def setUp(self):
        self.base_url = 'https://codespace-api.myjetbrains.com/youtrack/rest'
        self.creds = ('root', 'c11desp@ce')
        self.cookies = self._login()
         
         
    def _login(self):
        url = self.base_url + '/user/login'
        params = {
                 'login': 'root',
                 'password': 'c11desp@ce'                                  
                }              
        r = requests.post(url, data=params)
        return r.cookies
    
    def create_issue(self):
        url = self.base_url + '/issue'
        params = {
                  'project': 'API',
                  'summary': "Generated by robots",
                  'description': 'Hurray.'
                  }
         
        r = requests.put(url, data=params, cookies=self.cookies)
        self.assertEquals(r.status_code, 201)
        issue_id = r.headers['location'].split('/')[-1]
        
        return issue_id


    def request(self, url, method, params=None):
        # method could be POST GET DELETE
        # will return something like requests.get(url, data=params, cookies=self.cookies)
        return getattr(requests, method)(url, data=params, cookies=self.cookies)
        
    
    def get_summary_value_from_issue(self, data):
        """
        This method returns the value of the summary of the issue
        that been called by 'GET' request 
        """
        return xmltodict.parse(data.content)['issue']['field'][2]['value']
    
    def get_description_value_from_issue(self, data):
        """
        This method returns the value of the description of the issue
        that been called by 'GET' request 
        """
        return xmltodict.parse(data.content)['issue']['field'][3]['value']
    
    def get_issue_ids_from_list(self, data):
        """
        Returns dict of ids of the issues from xml data in pair key:value=entityId:id  
        """
        _xml_of_all_issues = xmltodict.parse(data.content)['issues']['issue']
     
        return {_xml_of_all_issues[item]['@entityId']: _xml_of_all_issues[item]['@id'] for item in range(len(_xml_of_all_issues))}
            
    def get_user_details_from_response(self, data):
        
        """
        'data' must be provided as data in XML format.
        Returns login, email and fullName values 
        """    
        return [
                xmltodict.parse(data.content)['user']['@login'].encode("utf-8"),
                xmltodict.parse(data.content)['user']['@email'].encode("utf-8"),
                xmltodict.parse(data.content)['user']['@fullName'].encode("utf-8")
                ]
        
        
    def get_error_message_from_request(self,data):
        """
        Returns message strings from XML with single node. data have to be in xml format
        """    
        return xmltodict.parse(data.content)['error'].encode("utf-8")
        
        
    def get_data_about_all_projects(self,data):
        """
        Returns message strings from XML with single node. data have to be in xml format
        """
       
        _xml_of_all_projects = xmltodict.parse(data.content)['projects']['project']
     
        return [[_xml_of_all_projects[item]['@name'], _xml_of_all_projects[item]['@shortName']] for item in range(len(_xml_of_all_projects))]
            
        
        