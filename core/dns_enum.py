#!/usr/bin/env python3

import dns.resolver
import dns.query
import dns.zone
import dns.reversename
import socket
import concurrent.futures
from typing import Dict, List, Optional, Any
from colorama import Fore, Back, Style, init
from .brute_force import SubdomainBruteforcer
from .zone_transfer import ZoneTransferChecker
from .utils import validate_domain, is_alive, create_progress_bar

# Initialize Colorama
init(autoreset=True)

class DNSEnumerator:
    def __init__(self, domain: str, wordlist: str = None, threads: int = 20, 
                 timeout: int = 3, resolver: str = None):
        self.domain = validate_domain(domain)
        self.wordlist = wordlist
        self.threads = threads
        self.timeout = timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
        
        if resolver:
            self.resolver.nameservers = [resolver]
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Using custom resolver: {Fore.YELLOW}{resolver}{Style.RESET_ALL}")
        
        self.bruteforcer = SubdomainBruteforcer(domain, wordlist, threads, timeout, resolver)
        self.zone_checker = ZoneTransferChecker(domain, timeout, resolver)
        
        # Common DNS record types
        self.record_types = {
            'A': self.query_a,
            'AAAA': self.query_aaaa,
            'MX': self.query_mx,
            'NS': self.query_ns,
            'TXT': self.query_txt,
            'SOA': self.query_soa,
            'CNAME': self.query_cname,
            'PTR': self.query_ptr
        }
    
    def enumerate_basic_records(self, record_types: List[str] = None) -> Dict:
        """Enumerate basic DNS records for the domain"""
        if not record_types:
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        
        results = {}
        total_records = len(record_types)
        
        for i, record_type in enumerate(record_types, 1):
            print(f"    {Fore.CYAN}└─{Style.RESET_ALL} Querying {Fore.YELLOW}{record_type}{Style.RESET_ALL} records... ", end='')
            
            if record_type in self.record_types:
                try:
                    result = self.record_types[record_type]()
                    if result:
                        print(f"{Fore.GREEN}Found {len(result)}{Style.RESET_ALL}")
                        results[record_type] = result
                    else:
                        print(f"{Fore.RED}None found{Style.RESET_ALL}")
                        results[record_type] = []
                except Exception as e:
                    print(f"{Fore.RED}Error{Style.RESET_ALL}")
                    results[record_type] = f"Error: {str(e)}"
            else:
                print(f"{Fore.RED}Invalid type{Style.RESET_ALL}")
        
        return results
    
    def query_a(self) -> List[str]:
        """Query A records"""
        try:
            answers = self.resolver.resolve(self.domain, 'A')
            return [str(r) for r in answers]
        except:
            return []
    
    def query_aaaa(self) -> List[str]:
        """Query AAAA records"""
        try:
            answers = self.resolver.resolve(self.domain, 'AAAA')
            return [str(r) for r in answers]
        except:
            return []
    
    def query_mx(self) -> List[str]:
        """Query MX records"""
        try:
            answers = self.resolver.resolve(self.domain, 'MX')
            return [f"{r.exchange} (Priority: {r.preference})" for r in answers]
        except:
            return []
    
    def query_ns(self) -> List[str]:
        """Query NS records"""
        try:
            answers = self.resolver.resolve(self.domain, 'NS')
            return [str(r) for r in answers]
        except:
            return []
    
    def query_txt(self) -> List[str]:
        """Query TXT records"""
        try:
            answers = self.resolver.resolve(self.domain, 'TXT')
            return [str(r) for r in answers]
        except:
            return []
    
    def query_soa(self) -> List[str]:
        """Query SOA records"""
        try:
            answers = self.resolver.resolve(self.domain, 'SOA')
            soa = answers[0]
            return [f"Primary NS: {soa.mname}, Hostmaster: {soa.rname}"]
        except:
            return []
    
    def query_cname(self) -> List[str]:
        """Query CNAME records"""
        try:
            answers = self.resolver.resolve(self.domain, 'CNAME')
            return [str(r) for r in answers]
        except:
            return []
    
    def query_ptr(self) -> List[str]:
        """Query PTR records (reverse DNS)"""
        try:
            a_records = self.query_a()
            ptr_records = []
            for ip in a_records:
                try:
                    rev_name = dns.reversename.from_address(ip)
                    answers = self.resolver.resolve(rev_name, 'PTR')
                    ptr_records.extend([f"{ip} -> {str(r)}" for r in answers])
                except:
                    continue
            return ptr_records
        except:
            return []
    
    def attempt_zone_transfer(self) -> Dict:
        """Attempt DNS zone transfer"""
        return self.zone_checker.check_all_nameservers()
    
    def bruteforce_subdomains(self) -> List[str]:
        """Bruteforce subdomains using wordlist"""
        if not self.wordlist:
            return []
        return self.bruteforcer.bruteforce()
    
    def recursive_enumeration(self, subdomains: List[str], depth: int = 2) -> Dict:
        """Perform recursive enumeration on discovered subdomains"""
        results = {}
        
        for subdomain in subdomains:
            print(f"  {Fore.MAGENTA}[*]{Style.RESET_ALL} Recursively enumerating {Fore.YELLOW}{subdomain}{Style.RESET_ALL}...")
            sub_enumerator = DNSEnumerator(
                subdomain,
                self.wordlist,
                self.threads,
                self.timeout
            )
            sub_results = sub_enumerator.bruteforce_subdomains()
            if sub_results:
                results[subdomain] = sub_results
                print(f"    {Fore.GREEN}✓{Style.RESET_ALL} Found {Fore.YELLOW}{len(sub_results)}{Style.RESET_ALL} subdomains under {subdomain}")
        
        return results
    
    def save_results(self, results: Dict, filename: str, format: str = 'txt'):
        """Save results to file in specified format"""
        import json
        import csv
        
        print(f"  {Fore.MAGENTA}[*]{Style.RESET_ALL} Saving results to {Fore.YELLOW}{filename}{Style.RESET_ALL} ({format.upper()})...")
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
        
        elif format == 'csv':
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Value'])
                for record_type, values in results['basic_records'].items():
                    if isinstance(values, list):
                        for value in values:
                            writer.writerow([record_type, value])
                for subdomain in results['subdomains']:
                    writer.writerow(['SUBDOMAIN', subdomain])
        
        else:  # txt format
            with open(filename, 'w') as f:
                f.write("╔══════════════════════════════════════════════════════════════╗\n")
                f.write(f"║ HawkBind Results for {results['domain']}{' ' * (41 - len(results['domain']))}║\n")
                f.write(f"║ Timestamp: {results['timestamp']}{' ' * (36 - len(results['timestamp']))}║\n")
                f.write("╚══════════════════════════════════════════════════════════════╝\n\n")
                
                f.write("BASIC DNS RECORDS:\n")
                f.write("─" * 50 + "\n")
                for record_type, values in results['basic_records'].items():
                    f.write(f"\n{record_type} Records:\n")
                    if isinstance(values, list):
                        for value in values:
                            f.write(f"  ├─ {value}\n")
                    else:
                        f.write(f"  └─ {values}\n")
                
                f.write("\nSUBDOMAINS FOUND:\n")
                f.write("─" * 50 + "\n")
                for subdomain in results['subdomains']:
                    f.write(f"  ├─ {subdomain}\n")
