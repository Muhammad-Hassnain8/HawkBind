#!/usr/bin/env python3
"""
HawkBind - DNS Enumeration Tool
Created by: Muhammad Hassnain
Description: A powerful DNS enumeration tool for security professionals
"""

import argparse
import sys
import time
from colorama import init, Fore, Back, Style
from core.dns_enum import DNSEnumerator
from core.utils import banner, print_results, color_status

# Initialize Colorama - this is correct
init(autoreset=True)

def main():
    # Display colored banner
    print(banner())
    
    parser = argparse.ArgumentParser(
        description=f'{Fore.CYAN}HawkBind - Advanced DNS Enumeration Tool{Style.RESET_ALL}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.YELLOW}Examples:{Style.RESET_ALL}
  {Fore.GREEN}python3 main.py -d example.com{Style.RESET_ALL}
  {Fore.GREEN}python3 main.py -d example.com -w wordlists/subdomains.txt -t 50{Style.RESET_ALL}
  {Fore.GREEN}python3 main.py -d example.com --no-bruteforce --timeout 5{Style.RESET_ALL}
  {Fore.GREEN}python3 main.py -d example.com --dns-records A,MX,TXT --output json{Style.RESET_ALL}
        """
    )
    
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-w', '--wordlist', help='Path to subdomain wordlist')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Number of threads (default: 20)')
    parser.add_argument('--timeout', type=int, default=3, help='DNS timeout in seconds (default: 3)')
    parser.add_argument('--dns-records', help='Comma-separated DNS records (A,AAAA,MX,NS,TXT,SOA,CNAME)')
    parser.add_argument('--no-zone-transfer', action='store_true', help='Skip zone transfer attempt')
    parser.add_argument('--no-bruteforce', action='store_true', help='Skip subdomain brute-forcing')
    parser.add_argument('--output', choices=['txt', 'json', 'csv'], help='Output format')
    parser.add_argument('-o', '--output-file', help='Save results to file')
    parser.add_argument('--resolver', help='Custom DNS resolver IP')
    parser.add_argument('--recursive', action='store_true', help='Enable recursive enumeration')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        init(strip=True)
    
    # Parse DNS records if specified
    dns_records = None
    if args.dns_records:
        dns_records = [record.strip().upper() for record in args.dns_records.split(',')]
    
    # Initialize enumerator
    enumerator = DNSEnumerator(
        domain=args.domain,
        wordlist=args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        resolver=args.resolver
    )
    
    try:
        # Start enumeration
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}Target:{Style.RESET_ALL} {Fore.YELLOW}{args.domain}{Style.RESET_ALL}{' ' * (46 - len(args.domain))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}Started:{Style.RESET_ALL} {Fore.GREEN}{time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}{' ' * (37)}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        results = {
            'domain': args.domain,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'basic_records': {},
            'subdomains': [],
            'zone_transfer': None
        }
        
        # Basic DNS enumeration
        print(f"{Fore.MAGENTA}[*]{Style.RESET_ALL} {Fore.CYAN}Enumerating basic DNS records...{Style.RESET_ALL}")
        basic_records = enumerator.enumerate_basic_records(dns_records)
        results['basic_records'] = basic_records
        print_results(basic_records, 'basic')
        
        # Zone transfer attempt
        if not args.no_zone_transfer:
            print(f"\n{Fore.MAGENTA}[*]{Style.RESET_ALL} {Fore.CYAN}Attempting zone transfer...{Style.RESET_ALL}")
            zone_result = enumerator.attempt_zone_transfer()
            results['zone_transfer'] = zone_result
            if zone_result:
                print_results(zone_result, 'zone')
        
        # Subdomain brute-forcing
        if not args.no_bruteforce and args.wordlist:
            print(f"\n{Fore.MAGENTA}[*]{Style.RESET_ALL} {Fore.CYAN}Starting subdomain brute-forcing...{Style.RESET_ALL}")
            subdomains = enumerator.bruteforce_subdomains()
            results['subdomains'] = subdomains
            
            if subdomains:
                print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} {Fore.WHITE}Found {Fore.YELLOW}{len(subdomains)}{Fore.WHITE} subdomains:{Style.RESET_ALL}")
                
                # Create a beautiful table for subdomains
                print(f"\n{Fore.CYAN}    ╔{'═'*50}╗{Style.RESET_ALL}")
                for i, subdomain in enumerate(subdomains[:10], 1):
                    if i < 10:
                        print(f"{Fore.CYAN}    ║{Style.RESET_ALL} {Fore.GREEN}├─ {Style.BRIGHT}{subdomain}{Style.RESET_ALL}{' ' * (47 - len(subdomain))}{Fore.CYAN}║{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}    ║{Style.RESET_ALL} {Fore.GREEN}└─ {Style.BRIGHT}{subdomain}{Style.RESET_ALL}{' ' * (47 - len(subdomain))}{Fore.CYAN}║{Style.RESET_ALL}")
                
                if len(subdomains) > 10:
                    print(f"{Fore.CYAN}    ║{Style.RESET_ALL} {Fore.YELLOW}    ... and {len(subdomains) - 10} more{' ' * (36 - len(str(len(subdomains) - 10)))}{Fore.CYAN}║{Style.RESET_ALL}")
                print(f"{Fore.CYAN}    ╚{'═'*50}╝{Style.RESET_ALL}")
                
                # Recursive enumeration if enabled
                if args.recursive and subdomains:
                    print(f"\n{Fore.MAGENTA}[*]{Style.RESET_ALL} {Fore.CYAN}Starting recursive enumeration...{Style.RESET_ALL}")
                    recursive_results = enumerator.recursive_enumeration(subdomains[:5])  # Limit recursion
                    if recursive_results:
                        results['recursive'] = recursive_results
            else:
                print(f"\n{Fore.RED}[-]{Style.RESET_ALL} No subdomains found")
        
        # Save results if requested
        if args.output and args.output_file:
            enumerator.save_results(results, args.output_file, args.output)
            print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} {Fore.WHITE}Results saved to {Fore.YELLOW}{args.output_file}{Style.RESET_ALL}")
        
        # Summary
        print(f"\n{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.WHITE}Enumeration completed at {Fore.YELLOW}{time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.WHITE}Total subdomains found: {Fore.YELLOW}{len(results['subdomains'])}{Style.RESET_ALL}")
        
        # Calculate statistics
        total_records = 0
        for v in results['basic_records'].values():
            if isinstance(v, list):
                total_records += len(v)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.WHITE}Total DNS records found: {Fore.YELLOW}{total_records}{Style.RESET_ALL}")
        
        if results['zone_transfer']:
            successful_zone = any(v.get('success', False) for v in results['zone_transfer'].values() if isinstance(v, dict))
            if successful_zone:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.WHITE}Zone transfer: {Fore.GREEN}SUCCESSFUL{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.WHITE}Zone transfer: {Fore.RED}FAILED{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}\n")
        
        # Credit line
        print(f"{Fore.MAGENTA}⚡{Style.RESET_ALL} {Fore.WHITE}HawkBind by {Fore.YELLOW}Muhammad Hassnain{Style.RESET_ALL} {Fore.MAGENTA}⚡{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!]{Style.RESET_ALL} {Fore.YELLOW}Enumeration interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}[!]{Style.RESET_ALL} {Fore.YELLOW}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
