from cloudflare import Cloudflare

import os

def get_cf_api():
    client = Cloudflare(api_token=os.environ.get('CF_API_TOKEN'))
    return client

def update_dyndns_records(ip):
    cf_api = get_cf_api()

    zones_result = cf_api.zones.list()
    zones = zones_result.result

    for zone in zones:
        records_data = cf_api.dns.records.list(zone_id=zone.id)
        records = records_data.result
        for record in records:
            if record.comment:
                if record.comment.startswith('DynDNS:'):
                        if record.content != ip:
                            cf_api.dns.records.update(dns_record_id=record.id,
                                                zone_id=zone.id,
                                                content=ip,
                                                type=record.type,
                                                name=record.name
                                    )

def get_zones():
    cf_api = get_cf_api()
    zones = cf_api.zones.list() 

    return zones.result

def delete_dns_record(id, domain):
    cf_api = get_cf_api()

    cf_api.dns.records.delete(dns_record_id=id, zone_id=get_zoneid_from_domain(domain))

def get_zoneid_from_domain(domain):
    cf_api = get_cf_api()

    zone = cf_api.zones.list(name=domain)

    # Fixme: We should check to ensure we only get one result.
    return zone.result[0].id


def get_existing_dyndns_records():
    cf_api = get_cf_api()

    zones_result = cf_api.zones.list()
    zones = zones_result.result

    dyndns_records = []

    # Examine each domain and pull each record that is a managed DynDNS record.
    for zone in zones:
        records_data = cf_api.dns.records.list(zone_id=zone.id)
        records = records_data.result
        for record in records:
            if record.comment:
                if record.comment.startswith('DynDNS:'):
                    dyndns_records.append(record)

    return dyndns_records



def create_update_dns_record(fqdn, ip, comment, type='A'):
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
                        cf_api.dns.records.update(dns_record_id=record.id,
                                                zone_id=zone.id,
                                                content=ip,
                                                type=record.type,
                                                name=record.name
                                        )
                    break
            else:
                # No record exists, let's create it.
                cf_api.dns.records.create(zone_id=zone.id,
                                        content=ip,
                                        name=fqdn,
                                        comment=comment,
                                        type=type
                                    )
            break
    else:
        # We did not find the domain we are looking for.
        raise ValueError(f'Domain {domain_name} not found')