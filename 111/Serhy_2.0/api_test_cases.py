'''
Created on Jun 21, 2016

@author: Serhy
'''

import unittest
from base_api import BaseApi
from replacements import *

#from yaml import load
    
class TestCreateIssue(BaseApi):
     
    def test_create_issue(self):
        
        issue_id = self.create_issue()
        
        url = self.base_url + '/issue/' + issue_id
        r = self.request(url, 'get')
        self.assertEquals(r.status_code, 200)
   
   
class TestDeleteIssue(BaseApi):
      
    def test_delete_issue(self):
        issue_id = self.create_issue()
          
        url = self.base_url + '/issue/' + issue_id
        r = self.request(url, 'delete')
         
        self.assertEquals(r.status_code, 200)
         
        r = self.request(url, 'get')
        self.assertEquals(r.status_code, 404)
         
    def test_delete_unexisted_issue(self):
        url = self.base_url + '/issue/' + 'blabla'
        r = self.request(url, 'delete')
         
        self.assertEquals(r.status_code, 404)
           
           
class TestUpdateIssue(BaseApi):
      
    def test_update_existing_issue(self):
        """
        Test to verify issue updated successfully. Checking status code, updated summary and updated description here.
        """
        issue_id = self.create_issue()
        new_summary_and_description = {
                                       'new_s': 'This is a new summary',
                                       'new_d': 'This is a new description'
                                      }
        url = self.base_url + '/issue/' + issue_id 
        url_for_update = url + '?summary=' + new_summary_and_description['new_s'] + '&description=' + new_summary_and_description['new_d']
        update_request = self.request(url_for_update, 'post')
  
        self.assertEquals(update_request.status_code, 200)
          
        get_updated_data = self.request(url, 'get')
          
        self.assertEquals(self.get_summary_value_from_issue(get_updated_data), new_summary_and_description['new_s'])
        self.assertEquals(self.get_description_value_from_issue(get_updated_data), new_summary_and_description['new_d'])
          
                     
    def test_update_non_existing_issue(self):
        """
        Test to verify that issue that not exist returns 404 for update action.
        """
        new_summary_and_description = {
                                       'new_s': 'This is a new summary',
                                       'new_d': 'This is a new description'
                                      }
        url = self.base_url + '/issue/' + 'notexist' 
        url_for_update = url + '?summary=' + new_summary_and_description['new_s'] + '&description=' + new_summary_and_description['new_d']
        update_request = self.request(url_for_update, 'post')
          
        self.assertEquals(update_request.status_code, 404)
  
          
                 
class TestGetIssuesInProject(BaseApi):
     
    def test_check_the_project_name(self):
        """
        Test that request returns list of available issues in project
        according to query params used:
        filter="This is a new summary" (a filter to issues in a project)
        max=100 (Maximum number of issues to be imported)
        after=500 (A number of issues to skip before getting a list of issues)
        """
        #issue_id = self.create_issue()
 
        url = self.base_url + '/issue/byproject/API?filter=This%20is%20a%20new%20summary&max=100'
         
        response_data = self.request(url, 'get')         
        issue_list_ids_in_proj = self.get_issue_ids_from_list(response_data)
 
        self.assertDictContainsSubset(expected_ids, issue_list_ids_in_proj)        
        #print response_data.content
         
          
        
class TestGetInfoForCurrentUser(BaseApi):
    
    def test_check_user_details_match(self):
        """
        Test that response for current user request data is 200
        and user details expected
        """ 
        url = self.base_url + '/user/current'
        response = self.request(url, 'get')
        
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_user_details, self.get_user_details_from_response(response))
        #print self.get_user_details_from_response(response)
         

 
class TestGetUserByLoginName(BaseApi):
     
    def test_check_user_details_for_valid_login_name(self):
        """
        Test that response is 200, user details are expected and correct in response
        received from valid request for login name
        """
        url = self.base_url + '/user/root'
        response = self.request(url, 'get') 
         
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_user_details, self.get_user_details_from_response(response))
        
                
    def test_403_is_returned_for_invalid_login_name(self):
        """
        Test of 403rd response with appropriate error message on the 
        request to unexisting login name
        
        """
            
        url = self.base_url + '/user/root11111111'
        response = self.request(url, 'get') 
         
        self.assertEqual(response.status_code, 403)
        self.assertEqual(error_for_invalid_user_login_name, self.get_error_message_from_request(response))       



class TestGetAllAccessibleProjects(BaseApi):
    
    def test_all_projects_response(self):
        """
        Get a list of all accessible projects from the server and check
        if the data is valid
        """
        
        url = self.base_url + '/project/all'
        response = self.request(url, 'get') 
        
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list_of_projects, self.get_data_about_all_projects(response))
        
       
if __name__ == '__main__':
    unittest.main()