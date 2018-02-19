import sys
import acitoolkit.acitoolkit as aci
import time

def main():
    time.sleep(70)
    description = ('Simple application that logs on to the APIC'
                   ' and displays all of the Endpoints.')
    creds = aci.Credentials('apic', description)
    args = creds.get()

    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    data = []
    endpoints = aci.IPEndpoint.get(session)
    for ep in endpoints:
        epg = ep.get_parent()
        app_profile = epg.get_parent()
        tenant = app_profile.get_parent()
        if (tenant.name == 'Devops' and ((epg.name == 'app'))):
          data.append((ep.mac, ep.ip, epg.name))
    #print "Test here\n"
    y = len(data)
    print "[APP]"
    print data[y-1][1]
    #col_widths = [19, 17, 15]
    #template = ''
    #for idx, width in enumerate(col_widths):
    #    template += '{%s:%s} ' % (idx, width)
    #print(template.format("MACADDRESS", "IPADDRESS", "EPG"))
    #fmt_string = []
    #for i in range(0, len(col_widths)):
     #  fmt_string.append('-' * (col_widths[i] - 2))
      # print(template.format(*fmt_string))
    #for rec in data:
     #   print(template.format(*rec))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

