#!/usr/bin/env python3

import dns.zone
import dns.query
import dns.resolver
from typing import Dict, List
from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)

class ZoneTransferChecker:
    def __init__(self, domain: str, timeout: int = 3, resolver: str = None):
        self.domain = domain
        self.timeout = timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
        
        if resolver:
            self.resolver.nameservers = [resolver]
    
    def get_nameservers(self) -> List[str]:
        """Get list of nameservers for the domain"""
        try:
            answers = self.resolver.resolve(self.domain, 'NS')
            nameservers = [str(r) for r in answers]
            if nameservers:
                print(f"    {Fore.CYAN}└─{Style.RESET_ALL} Found {Fore.YELLOW}{len(nameservers)}{Style.RESET_ALL} nameservers")
                for ns in nameservers:
                    print(f"        {Fore.WHITE}├─{Style.RESET_ALL} {Fore.CYAN}{ns}{Style.RESET_ALL}")
            return nameservers
        except Exception as e:
            print(f"    {Fore.RED}└─{Style.RESET_ALL} Could not retrieve nameservers: {str(e)}")
            return []
    
    def attempt_zone_transfer(self, nameserver: str) -> Dict:
        """Attempt zone transfer from a specific nameserver"""
        try:
            # Remove trailing dot if present
            if nameserver.endswith('.'):
                nameserver = nameserver[:-1]
            
            print(f"        {Fore.CYAN}└─{Style.RESET_ALL} Attempting zone transfer from {Fore.YELLOW}{nameserver}{Style.RESET_ALL}...")
            
            # Perform zone transfer
            zone = dns.zone.from_xfr(
                dns.query.xfr(nameserver, self.domain, timeout=self.timeout, lifetime=self.timeout)
            )
            
            if zone:
                records = []
                for name, node in zone.nodes.items():
                    rdatasets = node.rdatasets
                    for rdataset in rdatasets:
                        for rdata in rdataset:
                            records.append({
                                'name': str(name),
                                'type': dns.rdatatype.to_text(rdataset.rdtype),
                                'data': str(rdata)
                            })
                
                print(f"            {Fore.GREEN}✓{Style.RESET_ALL} Zone transfer successful! Found {Fore.YELLOW}{len(records)}{Style.RESET_ALL} records")
                return {
                    'nameserver': nameserver,
                    'success': True,
                    'records': records
                }
        except Exception as e:
            print(f"            {Fore.RED}✗{Style.RESET_ALL} Zone transfer failed: {Fore.YELLOW}{str(e)}{Style.RESET_ALL}")
            return {
                'nameserver': nameserver,
                'success': False,
                'error': str(e)
            }
        
        return {
            'nameserver': nameserver,
            'success': False,
            'error': 'Zone transfer failed'
        }
    
    def check_all_nameservers(self) -> Dict:
        """Attempt zone transfer from all nameservers"""
        nameservers = self.get_nameservers()
        
        if not nameservers:
            return {'error': 'No nameservers found'}
        
        results = {}
        vulnerable_found = False
        
        for ns in nameservers:
            result = self.attempt_zone_transfer(ns)
            results[ns] = result
            
            if result['success']:
                vulnerable_found = True
        
        if vulnerable_found:
            print(f"    {Fore.GREEN}✓{Style.RESET_ALL} {Fore.RED}WARNING:{Style.RESET_ALL} Zone transfer is enabled on some nameservers!")
        else:
            print(f"    {Fore.GREEN}✓{Style.RESET_ALL} Zone transfer is {Fore.GREEN}disabled{Style.RESET_ALL} on all nameservers (good!)")
        
        return results
