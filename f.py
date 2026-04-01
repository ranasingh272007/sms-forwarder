#!/usr/bin/env python3
"""
SMS Forwarder - Forwards SMS to target number
"""

import os
import sys
import json
import time
from datetime import datetime

# Target number (default 9019005721)
TARGET = sys.argv[1] if len(sys.argv) > 1 else "9019005721"

class SMSForwarder:
    def __init__(self):
        self.processed = set()
        self.load_processed()
        
    def load_processed(self):
        try:
            with open('.forwarded', 'r') as f:
                self.processed = set(f.read().splitlines())
        except:
            pass
            
    def save_processed(self, sid):
        with open('.forwarded', 'a') as f:
            f.write(str(sid) + '\n')
            
    def get_sms(self):
        try:
            result = os.popen('termux-sms-list -l 10').read()
            if result:
                return json.loads(result)
        except:
            pass
        return []
        
    def send_sms(self, msg):
        try:
            msg = msg.replace('"', '\\"').replace('\n', ' ')
            os.system(f'termux-sms-send -n {TARGET} "{msg}"')
            return True
        except:
            return False
            
    def run(self):
        print("\n" + "="*50)
        print("📱 SMS FORWARDER ACTIVE")
        print(f"➡️  Forwarding to: {TARGET}")
        print("⏹️  Press Ctrl+C to stop")
        print("="*50 + "\n")
        
        while True:
            try:
                sms_list = self.get_sms()
                for sms in sms_list:
                    sid = str(sms.get('_id', ''))
                    if sid and sid not in self.processed:
                        number = sms.get('number', 'Unknown')
                        body = sms.get('body', '')
                        time_str = datetime.now().strftime("%H:%M:%S")
                        
                        msg = f"[SMS] {time_str} | From: {number}\n{body}"
                        
                        if self.send_sms(msg):
                            self.save_processed(sid)
                            self.processed.add(sid)
                            print(f"✓ Forwarded: {number} - {body[:30]}...")
                            
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n\n⏹️  Forwarder stopped")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    forwarder = SMSForwarder()
    forwarder.run()
