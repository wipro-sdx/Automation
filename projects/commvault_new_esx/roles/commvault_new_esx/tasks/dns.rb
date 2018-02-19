#require 'winrm'
require 'pywinrm'

vm = ARGV[0]
float_ip = ARGV[1]

clientName = vm
ip = float_ip

opts = {
  endpoint: 'http://172.17.65.18:5985/wsman',
  user: 'administrator',
  password: 'Wipro@123'
}
conn = WinRM::Connection.new(opts)
list1 = "Add-Content \'C:\\Windows\\System32\\drivers\\etc\\hosts '" + ip + "`t" + clientName

conn.shell(:powershell) do |shell|
  output = shell.run(list1) do |stdout, stderr|
    STDOUT.print stdout
    STDERR.print stderr
  end
  puts "The script exited with exit code #{output.exitcode}"
end
