#!/usr/bin/env python3

import re
import socket
from colorama import Fore, Back, Style, init
from typing import Dict, List, Any

# Initialize Colorama
init(autoreset=True)

def banner() -> str:
    """Display HawkBind banner with colors"""
    return f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗{Fore.GREEN}██████╗ ██╗███╗   ██╗██████╗ {Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}██║  ██║██╔══██╗██║    ██║██║ ██╔╝{Fore.GREEN}██╔══██╗██║████╗  ██║██╔══██╗{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}███████║███████║██║ █╗ ██║█████╔╝ {Fore.GREEN}██████╔╝██║██╔██╗ ██║██║  ██║{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}██╔══██║██╔══██║██║███╗██║██╔═██╗ {Fore.GREEN}██╔══██╗██║██║╚██╗██║██║  ██║{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}██║  ██║██║  ██║╚███╔███╔╝██║  ██╗{Fore.GREEN}██████╔╝██║██║ ╚████║██████╔╝{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝{Fore.GREEN}╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝ {Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.CYAN}              DNS ENUMERATION TOOL v1.0{Style.RESET_ALL}                      {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}║{Style.RESET_ALL} {Fore.MAGENTA}                 Created by: Muhammad Hassnain{Style.RESET_ALL}                  {Fore.RED}║{Style.RESET_ALL}
{Fore.RED}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """

def validate_domain(domain: str) -> str:
    """Validate domain format"""
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9]'  # First character
        r'(?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)'  # Subdomain
        r'+[a-zA-Z]{2,}$'  # TLD
    )
    
    if not pattern.match(domain):
        raise ValueError(f"Invalid domain format: {domain}")
    
    return domain.lower()

def is_alive(host: str, port: int = 80, timeout: int = 2) -> bool:
    """Check if host is alive"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def color_status(status: str) -> str:
    """Return colored status indicator"""
    status_colors = {
        'success': f"{Fore.GREEN}✓{Style.RESET_ALL}",
        'error': f"{Fore.RED}✗{Style.RESET_ALL}",
        'warning': f"{Fore.YELLOW}⚠{Style.RESET_ALL}",
        'info': f"{Fore.BLUE}ℹ{Style.RESET_ALL}",
        'found': f"{Fore.GREEN}[+]{Style.RESET_ALL}",
        'not_found': f"{Fore.RED}[-]{Style.RESET_ALL}",
        'scanning': f"{Fore.MAGENTA}[*]{Style.RESET_ALL}"
    }
    return status_colors.get(status, status)

def print_results(results: Any, result_type: str):
    """Print results in formatted colored way"""
    if result_type == 'basic':
        for record_type, values in results.items():
            if values and isinstance(values, list):
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {Fore.CYAN}{record_type}{Style.RESET_ALL} {Fore.WHITE}Records:{Style.RESET_ALL}")
                
                # Color-code different record types
                record_color = {
                    'A': Fore.YELLOW,
                    'AAAA': Fore.MAGENTA,
                    'MX': Fore.GREEN,
                    'NS': Fore.BLUE,
                    'TXT': Fore.CYAN,
                    'SOA': Fore.RED,
                    'CNAME': Fore.LIGHTMAGENTA_EX,
                    'PTR': Fore.LIGHTCYAN_EX
                }.get(record_type, Fore.WHITE)
                
                for i, value in enumerate(values[:5]):
                    prefix = "├─" if i < min(4, len(values) - 1) else "└─"
                    if i < 4 or len(values) <= 5:
                        print(f"      {Fore.WHITE}{prefix}{Style.RESET_ALL} {record_color}{value}{Style.RESET_ALL}")
                    else:
                        print(f"      {Fore.WHITE}└─{Style.RESET_ALL} {Fore.YELLOW}... and {len(values) - 4} more{Style.RESET_ALL}")
                        break
            else:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} {Fore.CYAN}{record_type}{Style.RESET_ALL} {Fore.WHITE}Records:{Style.RESET_ALL} {Fore.RED}None found{Style.RESET_ALL}")
    
    elif result_type == 'zone':
        for nameserver, result in results.items():
            if isinstance(result, dict) and result.get('success'):
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {Fore.CYAN}Zone transfer from {Fore.YELLOW}{nameserver}{Style.RESET_ALL}:")
                print(f"  {Fore.CYAN}  ╔{'═'*60}╗{Style.RESET_ALL}")
                
                records = result.get('records', [])
                for i, record in enumerate(records[:10]):
                    prefix = "║  ├─" if i < min(9, len(records) - 1) else "║  └─"
                    record_str = f"{record['name']} ({Fore.MAGENTA}{record['type']}{Style.RESET_ALL}) -> {Fore.GREEN}{record['data']}{Style.RESET_ALL}"
                    print(f"  {Fore.CYAN}║{Style.RESET_ALL}   {prefix} {record_str}")
                
                if len(records) > 10:
                    print(f"  {Fore.CYAN}║{Style.RESET_ALL}      {Fore.YELLOW}... and {len(records) - 10} more records{Style.RESET_ALL}")
                print(f"  {Fore.CYAN}  ╚{'═'*60}╝{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} {Fore.CYAN}Zone transfer from {Fore.YELLOW}{nameserver}{Style.RESET_ALL}: {Fore.RED}Failed{Style.RESET_ALL}")

def create_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Create a colored progress bar"""
    if total == 0:
        return f"{Fore.YELLOW}0%{Style.RESET_ALL}"
    
    progress = int((current / total) * width)
    bar = f"{Fore.GREEN}{'█' * progress}{Fore.WHITE}{'░' * (width - progress)}{Style.RESET_ALL}"
    percentage = (current / total) * 100
    return f"{bar} {Fore.YELLOW}{percentage:.1f}%{Style.RESET_ALL}"
