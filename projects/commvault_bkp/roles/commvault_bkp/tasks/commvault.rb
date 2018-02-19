
#### Script to connect to Commvault server and add/configure the new VM/instance in Commvault server with selected backup policy 

require 'net/http'
require 'base64'
require 'rexml/document'
#require 'commvault/commvault_host_entry_update'
#require_relative '/usr/share/ruby/commvault/commvault_host_entry_update.rb'
include REXML
include Net

def fail(msg)
   $evm.log("info", '#{msg}')
   exit
end

def getResp(res, failureMsg)
   fail(failureMsg) if !res.kind_of? HTTPSuccess
   res.body
end


server = "172.16.6.16"
user = "admin"
pwd = "admin"
pwd = Base64.encode64(pwd)

service = "http://#{server}:81/SearchSvc/CVWebService.svc/"

clientName = ARGV[0]
storagePolicyName = ARGV[1]

#1. Login
loginReq = "<DM2ContentIndexing_CheckCredentialReq mode='Webconsole' username='#{user}' password='#{pwd}' />"

uri = URI(service + "Login")
req = HTTP::Post.new(uri)
req.body = loginReq

response = HTTP.start(uri.hostname, uri.port) do |http|
   http.request(req)
end
token = ""
respBody = getResp(response, "Login Failed")
doc = Document.new(respBody)
token = XPath.first(doc, ".//@token")
fail("Login Failed") if token == nil

#$evm.log("info", "Login successful")

#2. get clientId

clientUrl = service + "Client"

req = Net::HTTP::Get.new(URI(clientUrl))
req['Authtoken'] = token

response = Net::HTTP.start(uri.hostname, uri.port) {|http|
   http.request(req)
}

getClientResp = getResp(response, "Getting clients failed")
doc = Document.new(getClientResp)


doc.elements.each("*/clientProperties/client/clientEntity"){|element|
   if element.attributes["clientName"]=="#{clientName}"
        @clientId =  element.attributes["clientId"]
   end
}

clientId = @clientId
#$evm.log("info", "Fetched Client ID: #{clientId} ")

#3. get Subclient

subclientUrl = service + "Subclient?clientid=#{clientId}"

req = Net::HTTP::Get.new(URI(subclientUrl))
req['Authtoken'] = token

response = Net::HTTP.start(uri.hostname, uri.port) {|http|
   http.request(req)
}

getsubClientResp = getResp(response, "Getting subclients failed")
doc = Document.new(getsubClientResp)


doc.elements.each("*/subClientProperties/subClientEntity"){|element|
   if element.attributes["subclientName"]=="default"
        @subclientId =  element.attributes["subclientId"]
   end
}

subclientId = @subclientId
#$evm.log("info", "Fetched subclient ID: #{subclientId} ")

#4. update Subclient


#$evm.log("info", "Updating default subclient with #{storagePolicyName} ")

xmldoc ="<App_UpdateSubClientPropertiesRequest><subClientProperties><commonProperties><storageDevice><dataBackupStoragePolicy><storagePolicyName>#{storagePolicyName}</storagePolicyName></dataBackupStoragePolicy></storageDevice></commonProperties></subClientProperties></App_UpdateSubClientPropertiesRequest>"

#$evm.log("info",  "#{xmldoc}" )
subclientPropsUrl = service + "Subclient/#{subclientId}"
req = HTTP::Post.new(URI(subclientPropsUrl))
req.body = xmldoc
req['Authtoken'] = token

response = Net::HTTP.start(uri.hostname, uri.port) {|http|
   http.request(req)
}


getsubClientPropsResp = getResp(response, "Getting subclients failed")
doc = Document.new(getsubClientPropsResp)



#$evm.log("info", "Updated storage policy for default subclient ")


#5. Assign task(schedule policy) to subclient


xmldoc = "<TMMsg_ModifyTaskReq><taskInfo><associations clientName='#{clientName}' appName='File System' backupsetName='defaultBackupSet' subclientName='default'/><task><task taskName='#{storagePolicyName}'/></task><taskOperation>MODIFY</taskOperation></taskInfo></TMMsg_ModifyTaskReq>"

scheduleAssignUrl = service + "Task"
req = HTTP::Put.new(URI(scheduleAssignUrl))
req.body = xmldoc
req['Authtoken'] = token

response = Net::HTTP.start(uri.hostname, uri.port) {|http|
   http.request(req)
}


getscheduleAssignResp = getResp(response, "Assigning schedule policy to subclients failed")
doc = Document.new(getscheduleAssignResp)

#$evm.log("info", "Assigned schedule policy to subclient")

#6. Hosts file update in Commvault server

#$evm.log("info", "Executing Commvault server hosts entry update")
#dns(vm,float_ip)

