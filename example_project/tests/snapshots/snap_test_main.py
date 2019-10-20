# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['BasicTestCase::test_basic_single_arg_component 1'] = '''<html>
  <head>
    <title>title</title>
    <style>
      .alert {
        border: 1px solid black;
      }
      .alert.alert-danger {
        border-color: red;
      }
      .alert.alert-success {
        border-color: green;
      }
      .panel {
        padding: 10px;
        border: 1px solid red;
        margin-top: 20px;
      }
      .panel.panel--with-title {
        padding-top: 20px;
        border-top-width: 0px;
      }

    </style>
  </head>
  <body>
  
  
  dict  

  
  
    <div class="alert alert-danger">
  
      <p> this is an alert with <strong> block </strong> content! </p>
      
        <p> you can stick other templatetags in here </p>
        <div style="padding:20px">
          <div class="alert alert-success">
  
            <p> Including <strong> nested </strong> alerts! </p>
            <p> The inner content has access to context, like danger  </p>
          

  Note that the re-used parts of the templates don't get any context by default. For this case, 
  request url: 

</div>
        </div>
      
    

  Note that the re-used parts of the templates don't get any context by default. For this case, 
  request url: 

</div>
  


  <div>
    
<div
  class="panel  panel--with-title "
>
  
    <div class="panel-header">
      <a href="">hello world</a>
    </div>
  
  <div class="panel-body">
    
      <p> This is a panel body </p>
      x  
        <table><tbody>
          
          True
            <tr  style="background-color: #ccc; " >
              <th> value </th>
              <td> 1 </td>
            </tr>
            
          False
            <tr >
              <th> value </th>
              <td> 2 </td>
            </tr>
            
          True
            <tr  style="background-color: #ccc; " >
              <th> value </th>
              <td> 3 </td>
            </tr>
            
          False
            <tr >
              <th> value </th>
              <td> 4 </td>
            </tr>
            
        </tbody></table>
      
    
    <strong> lorem ipsum </strong>

    
      <div style="padding: 20px">
        
<div
  class="panel  panel--with-title "
>
  
    <div class="panel-header">
      <a href="">note that the nested panel does not </a>
    </div>
  
  <div class="panel-body">
    
          nested content <br>
          
      <p> This is a panel body </p>
      x  
        <table><tbody>
          
          True
            <tr  style="background-color: #ccc; " >
              <th> value </th>
              <td> 1 </td>
            </tr>
            
          False
            <tr >
              <th> value </th>
              <td> 2 </td>
            </tr>
            
          True
            <tr  style="background-color: #ccc; " >
              <th> value </th>
              <td> 3 </td>
            </tr>
            
          False
            <tr >
              <th> value </th>
              <td> 4 </td>
            </tr>
            
        </tbody></table>
      
    

        
    <strong> lorem ipsum </strong>

    
  </div>
</div>
      </div>
    
  </div>
</div>
  </div>
  

  <div class="margin-top:50px">
    
<div
  class="panel "
>
  
    <div class="panel-header">
      
        some <strong> rich </strong> title here
      
    </div>
  
  <div class="panel-body">
    
        
          This is the <i>panel body</i>
        
      
  </div>
  
    <div class="panel-footer" style="margin:5px; padding: 5px; border: 1px solid green;">
      
        This be the footer
      
    </div>
  
</div>
  </div>

  </body>
</html>'''
