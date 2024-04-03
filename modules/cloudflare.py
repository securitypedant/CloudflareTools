from cloudflare import Cloudflare

import os

def get_cf_api():
    # client = Cloudflare(api_key=os.environ.get('CF_API_TOKEN'))
    client = Cloudflare(api_token=os.environ.get('CF_API_TOKEN'))
    return client

def create_update_dns_record(fqdn, ip, type='A'):
    cf_api = get_cf_api()

    # Split the domain name into its components, remove the hostname and just get the domain
    parts = fqdn.split(".")
    domain_name = ".".join(parts[1:])

    # Create or update a DNS record in Cloudflare.
    zones_result = cf_api.zones.list()
    zones = zones_result.result

    for zone in zones:
        # Do we have access to the domain we want to create the record in?
        if zone.name == domain_name:
            zone_records = cf_api.dns.records.list(zone_id=zone.id, type=type)
            records = zone_records.result
            for record in records:
                if record.name == fqdn:
                    # Record already exists. Update if the ip is different.
                    if record.content != ip:
                        cf_api.dns.records.update(zone_id=zone.id,
                                                  content=ip
                                        )
                    break
            else:
                # No record exists, let's create it.
                cf_api.dns.records.create(zone_id=zone.id,
                                        content=ip,
                                        name=fqdn,
                                        type=type
                                    )
            break
    else:
        # We did not find the domain we are looking for.
        raise ValueError(f'Domain {domain_name} not found')