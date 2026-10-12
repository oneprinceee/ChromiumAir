import os
import sys

def main():
    include_dir = os.path.expandvars(r'%ProgramFiles(x86)%\Windows Kits\10\Include')
    sdk_ver = None
    if os.path.exists(include_dir):
        for cand in ['10.0.26100.0', '10.0.22621.0', '10.0.22000.0', '10.0.20348.0', '10.0.19041.0']:
            if os.path.exists(os.path.join(include_dir, cand)):
                sdk_ver = cand
                break
    print(f'Detected installed Windows SDK version: {sdk_ver}')
    if sdk_ver:
        files = [
            os.path.join('chromium_src', 'build', 'vs_toolchain.py'),
            os.path.join('chromium_src', 'build', 'toolchain', 'win', 'setup_toolchain.py')
        ]
        for fpath in files:
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                old_str = "SDK_VERSION = '10.0.28000.0'"
                new_str = f"SDK_VERSION = '{sdk_ver}'"
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated SDK_VERSION to {sdk_ver} in {fpath}')
                else:
                    print(f'Warning: SDK_VERSION not found in {fpath}')

if __name__ == '__main__':
    main()
