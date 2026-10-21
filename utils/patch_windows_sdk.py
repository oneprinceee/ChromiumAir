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

        # Match NTDDI_VERSION to SDK 10.0.26100.0 (NTDDI_WIN11_GE = 0x0A000010)
        # In SDK 10.0.26100.0, NTDDI_WIN11_BR is not defined in sdkddkver.h,
        # which causes the C preprocessor to treat it as 0 and break Windows headers.
        win_build_gn = os.path.join('chromium_src', 'build', 'config', 'win', 'BUILD.gn')
        if os.path.exists(win_build_gn):
            with open(win_build_gn, 'r', encoding='utf-8') as f:
                gn_content = f.read()
            if 'NTDDI_VERSION=NTDDI_WIN11_BR' in gn_content:
                ntddi_macro = 'NTDDI_WIN11_GE' if sdk_ver.startswith('10.0.26100') else 'NTDDI_WIN11_ZN'
                gn_content = gn_content.replace('NTDDI_VERSION=NTDDI_WIN11_BR', f'NTDDI_VERSION={ntddi_macro}')
                with open(win_build_gn, 'w', encoding='utf-8') as f:
                    f.write(gn_content)
                print(f'Updated NTDDI_VERSION define to {ntddi_macro} in {win_build_gn}')

if __name__ == '__main__':
    main()
