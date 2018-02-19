Connect-VIServer -Server “172.17.66.156” -User Administrator -Password Wipro@123
#Get-Cluster -name "Openshift" | Get-VMhost | Get-VMHostStorage –RescanAllHBA
New-Datastore -VMHost “172.17.65.11” -Name ‘VMFS_Datastore_2’ -Path naa.624a9370e62aa0b26b124c9700011028  -vmfs
