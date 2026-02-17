#!/usr/bin/env python3

import dns.resolver
import concurrent.futures
import threading
from typing import List, Set
import time
from colorama import Fore, Back, Style, init
from core.utils import create_progress_bar

# Initialize Colorama
init(autoreset=True)

class SubdomainBruteforcer:
    def __init__(self, domain: str, wordlist: str, threads: int = 20, 
                 timeout: int = 3, resolver: str = None):
        self.domain = domain
        self.wordlist = wordlist
        self.threads = threads
        self.timeout = timeout
        self.found_subdomains = set()
        self.lock = threading.Lock()
        self.checked_count = 0
        self.total_count = 0
        
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
        
        if resolver:
            self.resolver.nameservers = [resolver]
    
    def check_subdomain(self, subdomain: str) -> bool:
        """Check if a subdomain exists"""
        try:
            full_domain = f"{subdomain}.{self.domain}"
            answers = self.resolver.resolve(full_domain, 'A')
            if answers:
                with self.lock:
                    self.found_subdomains.add(full_domain)
                    # Print found subdomain immediately with color
                    print(f"\n    {Fore.GREEN}✓ Found:{Style.RESET_ALL} {Fore.YELLOW}{full_domain}{Style.RESET_ALL}")
                return True
        except:
            pass
        finally:
            with self.lock:
                self.checked_count += 1
        return False
    
    def load_wordlist(self) -> List[str]:
        """Load subdomain wordlist"""
        try:
            with open(self.wordlist, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip()]
                print(f"    {Fore.CYAN}└─{Style.RESET_ALL} Loaded {Fore.YELLOW}{len(subdomains)}{Style.RESET_ALL} subdomains from wordlist")
                return subdomains
        except FileNotFoundError:
            print(f"    {Fore.RED}└─{Style.RESET_ALL} Wordlist not found: {Fore.YELLOW}{self.wordlist}{Style.RESET_ALL}")
            return []
        except Exception as e:
            print(f"    {Fore.RED}└─{Style.RESET_ALL} Error loading wordlist: {str(e)}")
            return []
    
    def bruteforce(self) -> List[str]:
        """Perform subdomain bruteforcing"""
        subdomains = self.load_wordlist()
        if not subdomains:
            return []
        
        self.total_count = len(subdomains)
        
        print(f"    {Fore.CYAN}└─{Style.RESET_ALL} Starting bruteforce with {Fore.YELLOW}{self.threads}{Style.RESET_ALL} threads...")
        
        start_time = time.time()
        
        # Progress tracking
        print(f"\n    {Fore.CYAN}Progress:{Style.RESET_ALL}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all tasks
            future_to_subdomain = {
                executor.submit(self.check_subdomain, subdomain): subdomain 
                for subdomain in subdomains
            }
            
            # Process results with progress bar
            for future in concurrent.futures.as_completed(future_to_subdomain):
                if self.checked_count % 10 == 0 or self.checked_count == self.total_count:
                    progress_bar = create_progress_bar(self.checked_count, self.total_count)
                    print(f"\r    {progress_bar} ", end='', flush=True)
        
        elapsed_time = time.time() - start_time
        print(f"\n    {Fore.GREEN}✓{Style.RESET_ALL} Bruteforce completed in {Fore.YELLOW}{elapsed_time:.2f}{Style.RESET_ALL} seconds")
        print(f"    {Fore.GREEN}✓{Style.RESET_ALL} Found {Fore.YELLOW}{len(self.found_subdomains)}{Style.RESET_ALL} subdomains")
        
        return sorted(list(self.found_subdomains))
