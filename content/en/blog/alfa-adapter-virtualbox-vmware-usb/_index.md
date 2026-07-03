---
title: "ALFA Adapter USB Passthrough: VirtualBox & VMware Setup Guide"
description: "Step-by-step guide to ALFA USB WiFi adapter USB passthrough in VirtualBox and VMware Workstation for Kali Linux. Covers AWUS036ACH, AWUS036AXML, USB 3.0 filter, Extension Pack, and troubleshooting."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Does VirtualBox need the Extension Pack for ALFA adapters?"
    answer: "Yes. VirtualBox requires the Extension Pack for USB 2.0 and USB 3.0 passthrough. Without it, only USB 1.1 is available, which is insufficient for modern ALFA adapters."
  - question: "Should I use USB 2.0 or USB 3.0 controller for ALFA adapters?"
    answer: "AWUS036AXML must use USB 3.0 (xHCI). AWUS036ACH is a USB 2.0 device but works fine with xHCI. Setting everything to USB 3.0 is recommended."
  - question: "Does VMware Workstation need extra extensions?"
    answer: "No. VMware Workstation 17+ and Fusion 13+ have built-in USB 2.0/3.0 support. Just make sure the USB arbiter service is running."
  - question: "Why does lsusb show the adapter but there is no wlan interface?"
    answer: "USB passthrough succeeded but the driver did not load. RTL8812AU needs modprobe 88XXau or the realtek-rtl88xxau-dkms package. MT7921AUN needs modprobe mt7921u."
  - question: "What should I do if the USB adapter keeps disconnecting on a Linux host?"
    answer: "Disable USB auto-suspend by running echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend, and make sure your user is in the vboxusers group."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-virtualbox-vmware-usb.webp"
---

Running an ALFA WiFi adapter inside a virtual machine is not as simple as plugging it in and hoping the guest OS picks it up. Unlike shared folders or bridged networking, monitor mode and raw packet injection require **full USB control** — the VM must exclusively own the USB device, not share it through the host's network stack. This is called USB passthrough, and getting it right is the single most common setup failure for pentesters and CTF players working in VMs.

{{< tldr >}}
Using ALFA adapters in VirtualBox or VMware requires USB passthrough configuration. VirtualBox needs the Extension Pack with USB 3.0 enabled. VMware has built-in USB support but needs the arbiter service running. AWUS036ACH uses the 88XXau driver, AWUS036AXML uses mt7921u.
{{< /tldr >}}





This guide covers the complete passthrough setup for **VirtualBox 7.x** and **VMware Workstation 17+ / VMware Fusion 13+**, targeting Kali Linux as the guest OS. It addresses both the AWUS036ACH (RTL8812AU chipset) and the newer AWUS036AXML (MT7921AUN chipset), with adapter-specific notes where behaviour differs.

By the end, your ALFA adapter will appear inside Kali via `lsusb`, the correct driver will be loaded, and `airmon-ng` will confirm monitor mode is working.

---

## Prerequisites

Before starting, confirm your environment matches the requirements below. Missing any one item — especially the VirtualBox Extension Pack — is the root cause of most passthrough failures.

| Requirement | Details |
|---|---|
| **Hypervisor** | VirtualBox 7.x + Extension Pack **or** VMware Workstation 17+ / Fusion 13+ |
| **Guest OS** | Kali Linux 2024.x or later (tested on 2024.1–2025.1) |
| **ALFA Adapter** | AWUS036ACH, AWUS036AXML, AWUS036ACM, or any RTL8812AU / MT7921AUN device |
| **Host USB port** | USB 3.0 recommended (especially for AWUS036AXML) |
| **Host OS** | Windows 10/11, Linux, or macOS (Fusion) |
| **Sudo access** | Required inside the Kali VM |

{{< alert "circle-info" >}}
If you have not yet installed the driver inside Kali, complete the USB passthrough steps in this guide first. Once the adapter is visible inside the VM, follow the [ALFA Driver Install Guide](/en/blog/install-alfa-driver-kali-ubuntu/) to compile and load the correct driver.
{{< /alert >}}

---

## VirtualBox USB Passthrough — Step by Step

VirtualBox requires an additional component — the **Extension Pack** — to support USB 2.0 and USB 3.0 passthrough. Without it, only USB 1.1 (OHCI) is available, which is insufficient for modern ALFA adapters.

### Install the VirtualBox Extension Pack

1. Open [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Under **VirtualBox Extension Pack**, click **All supported platforms** to download the `.vbox-extpack` file. The version must exactly match your installed VirtualBox version.
3. Open VirtualBox, go to **File → Preferences → Extensions** (on macOS: **VirtualBox → Settings → Extensions**).
4. Click the **+** icon, browse to the downloaded `.vbox-extpack`, and install it. Accept the licence when prompted.

To verify the Extension Pack is active from the command line:

```bash
VBoxManage list extpacks
```

Expected output:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
If the **Usable** field shows `false`, the Extension Pack version does not match your VirtualBox version. Uninstall and reinstall the correct version.
{{< /alert >}}

### Add Your User to the vboxusers Group (Linux Hosts Only)

On Linux hosts, your user account must be a member of the `vboxusers` group to access USB devices.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

After running this, **log out and log back in** (or reboot) for the group change to take effect. You can verify with:

```bash
groups $USER
```

The output should include `vboxusers`.

### Enable the USB Controller in VM Settings

1. Shut down your Kali VM if it is running.
2. Select the VM, click **Settings → USB**.
3. Tick **Enable USB Controller**.
4. Select **USB 3.0 (xHCI) Controller** from the radio buttons.

{{< alert "circle-info" >}}
USB 3.0 (xHCI) is required for the AWUS036AXML. For the AWUS036ACH, USB 2.0 (EHCI) is technically sufficient since the adapter itself is USB 2.0, but using xHCI causes no harm and keeps your configuration consistent.
{{< /alert >}}

### Add a USB Device Filter

A USB device filter tells VirtualBox to automatically capture the ALFA adapter every time it is plugged in, without requiring manual intervention each session.

1. In the same **Settings → USB** panel, click the **+** icon (Add USB filter from device).
2. Plug in your ALFA adapter now if it is not already connected. VirtualBox will show it in the dropdown.
3. Select the device. It typically appears as **"Realtek 802.11ac NIC"** (AWUS036ACH) or **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. Click **OK** to save.

The filter stores the vendor and product ID. Next time the VM boots with the adapter plugged in, VirtualBox will automatically pass it through.

### Start the VM and Verify with lsusb

Start your Kali VM. Once the desktop loads, open a terminal and run:

```bash
lsusb
```

You should see a line resembling:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

or for AWUS036AXML:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

If the device does not appear, consult the troubleshooting table at the end of this section.

### Load the Driver

**AWUS036ACH (RTL8812AU):**

```bash
sudo modprobe 88XXau
```

If that fails (module not found), install the DKMS package first:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AUN):**

```bash
sudo modprobe mt7921u
```

The MT7921AUN driver is included in the mainline kernel since 5.18. Kali 2024.x ships with a kernel new enough to include it, but you may also need firmware:

```bash
sudo apt install -y firmware-misc-nonfree
```

### Verify Monitor Mode

With the driver loaded, confirm the interface name:

```bash
ip link show
```

Look for an interface named `wlan0`, `wlan1`, or similar. Then enable monitor mode:

```bash
sudo airmon-ng start wlan1
```

Successful output ends with the monitor interface name (e.g., `wlan1mon`). Verify:

```bash
sudo iwconfig wlan1mon
```

The **Mode** field should read `Monitor`.

### VirtualBox Common Errors

| Error | Cause | Fix |
|---|---|---|
| "No USB devices available" in USB settings | Extension Pack not installed or version mismatch | Install the matching Extension Pack version |
| Adapter not captured / not visible in lsusb | User not in `vboxusers` group (Linux host) | `sudo usermod -aG vboxusers $USER`, then log out/in |
| "USB device is busy with a previous request" | Another process on host is using the device | Unplug and replug the adapter before starting VM |
| Device keeps disconnecting inside VM | USB 3.0 controller not enabled; VM using OHCI | Switch to USB 3.0 (xHCI) in VM Settings → USB |
| Filter added but device not auto-captured | Filter created before Extension Pack installed | Delete and re-add the filter after installing Extension Pack |

---

## VMware Workstation / VMware Fusion USB Passthrough

VMware handles USB passthrough differently from VirtualBox. There is no separate extension to install — USB 2.0 and 3.0 support is built into VMware Workstation 17+ and Fusion 13+. The main mechanism is the **USB arbitrator service**, which monitors host USB events and routes devices to VMs.

### Connect the Adapter via the Device Menu

When you plug in your ALFA adapter while a VM is running, VMware typically shows a popup asking which VM should own the device. If you miss the popup:

1. With the Kali VM running, go to **VM → Removable Devices** in the menu bar.
2. Expand the list, locate your ALFA adapter (e.g., **Realtek 802.11ac NIC**).
3. Click **Connect (Disconnect from Host)**.

The device will disconnect from the host OS and become exclusively available to the VM.

### VMware Fusion (macOS)

On macOS with VMware Fusion:

1. Go to **Virtual Machine → USB & Bluetooth**.
2. Locate the ALFA adapter in the list.
3. Toggle the connection to **Connect to Linux** (or the name of your Kali VM).

Alternatively, in Fusion's VM Settings under **USB & Bluetooth**, enable **Automatically connect new USB devices** to have Fusion pass through devices to the active VM without prompting.

### Verify and Load Driver

Once connected, verify inside Kali:

```bash
lsusb
```

Then load the appropriate driver as described in the VirtualBox section above (steps 3.6 and 3.7 apply identically).

### Check the VMware USB Arbitrator Service

If the ALFA adapter does not appear in the **Removable Devices** menu, the USB arbitrator service may not be running. On Linux hosts:

```bash
sudo systemctl status vmware-usbarbitrator
```

If it is stopped:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

On Windows hosts, open **Services** (`services.msc`), locate **VMware USB Arbitration Service**, and set it to **Automatic (start)**.

### Enable USB 3.0 in VMware

For the AWUS036AXML and other USB 3.0 devices, verify that your VM hardware version supports xHCI. Open the `.vmx` file for your Kali VM (located in the VM's folder) and confirm or add:

```
usb_xhci.present = "TRUE"
```

In VMware Workstation GUI: **VM → Settings → USB Controller**, and select **USB 3.1** from the dropdown. The VM must be powered off to change this setting.

{{< alert "triangle-exclamation" >}}
VMware hardware version 14 or later is required for USB 3.0 (xHCI) support. If your VM was created with an older hardware version, upgrade it via **VM → Manage → Change Hardware Compatibility**.
{{< /alert >}}

### VMware Common Errors

| Error | Cause | Fix |
|---|---|---|
| Adapter not in Removable Devices menu | USB arbitrator not running | Start `vmware-usbarbitrator` service |
| Device connects then immediately disconnects | Host OS driver takes the device back | Disable the host WiFi driver for the adapter, or unplug and reconnect faster |
| "Device already in use by host" | Host OS claimed the device | Eject from host (e.g., disable host network adapter) before connecting in VM |
| No USB 3.0 speed inside VM | VM hardware version < 14 or xHCI not enabled | Upgrade hardware version, add `usb_xhci.present = "TRUE"` to .vmx |
| Monitor mode fails even after passthrough | Wrong or missing driver inside Kali | Follow the [Driver Install Guide](/en/blog/install-alfa-driver-kali-ubuntu/) |

---

## Adapter-Specific Notes

### AWUS036ACH (RTL8812AU)

The AWUS036ACH is a **USB 2.0** device and is one of the most well-tested adapters in VM environments. Both VirtualBox and VMware handle it reliably.

- USB controller: either USB 2.0 (EHCI) or USB 3.0 (xHCI) works fine.
- Driver package: `realtek-rtl88xxau-dkms` (available in Kali repos). Module name: `88XXau`.
- On some newer kernels (6.x), the DKMS package may need a patch. Check the [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) GitHub page for the latest status.
- Monitor mode and packet injection are very stable in VM passthrough.

You can find the adapter in our store: [ALFA AWUS036ACH](/en/products/alfa/awus036ach/).

### AWUS036AXML (MT7921AUN)

The AWUS036AXML is a **USB 3.0** device supporting WiFi 6E. It is newer and has some edge cases in VM environments.

- USB controller: **must** use USB 3.0 (xHCI). USB 2.0 passthrough causes the device to operate at reduced capability and may cause firmware load failures.
- Driver: `mt7921u` is in the mainline kernel (5.18+). Kali 2024.x includes it. Firmware package: `firmware-misc-nonfree`.
- **Known issue**: Some early AWUS036AXML units experience periodic freezing under VirtualBox USB 3.0 arbitration. If you see the interface disappearing and reappearing in `ip link`, try switching the VirtualBox USB controller to USB 2.0 as a diagnostic step. If that stabilises it, this is a VirtualBox xHCI arbitration issue rather than a driver problem.
- VMware Workstation tends to handle the AWUS036AXML more reliably than VirtualBox for USB 3.0 passthrough.

Full review: [AWUS036AXML WiFi 6E Review](/en/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (MT7612U, Dual Antenna)

The AWUS036ACM uses the MediaTek MT7612U chipset with an in-kernel driver (`mt76x2u`, mainlined since kernel 4.19). No driver installation is needed — once passthrough is configured, the adapter is plug-and-play inside the VM. If the module does not load automatically, run `sudo modprobe mt76x2u`. The AWUS036ACM has two RP-SMA antenna ports.

---

## Performance Tips

Getting the adapter into the VM is step one. Getting stable performance during actual pentesting or capture sessions requires a few additional tuning steps.

**Use the correct USB filter type.** For the AWUS036AXML, always use a USB 3.0 filter in VirtualBox (ensure the xHCI controller is selected). A USB 2.0 filter on a USB 3.0 device will cause the device to negotiate at USB 2.0 speed, halving throughput.

**Disable USB autosuspend on the host.** Linux hosts may aggressively suspend the USB device, causing the VM to lose it. Disable this at the host level:

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

To persist across reboots, add to `/etc/rc.local` or create a udev rule.

**Allocate adequate VM resources.** Packet injection and capture workloads are CPU-intensive. Allocate at minimum:
- **2 CPU cores** (4 recommended for parallel tools like `hcxdumptool` + `hashcat`)
- **2 GB RAM** (4 GB if running a full Kali desktop with GUI tools)

**Take a VM snapshot before engagements.** Before starting any pentest session, snapshot your Kali VM. If a driver crash or rogue firmware update corrupts your setup, reverting the snapshot gets you back to a known-good state in seconds.

**Keep the adapter cool.** ALFA adapters with high-gain antennas generate heat during sustained injection. In a VM, the host OS may throttle the USB device if it detects thermal or power issues. Use the adapter in a well-ventilated environment.

{{< alert "circle-info" >}}
For capture sessions longer than 30 minutes, consider using a powered USB hub between the adapter and your host. It provides stable power and prevents voltage drops that can cause the adapter to disconnect during critical captures.
{{< /alert >}}

---

## Bare Metal vs VM: Honest Comparison

Virtual machines introduce a layer of complexity between your adapter and the kernel. Here is an honest assessment for security professionals making infrastructure decisions:

| Feature | Bare Metal Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **Driver support** | Full, direct | Good (with Extension Pack) | Good (built-in USB) |
| **Monitor mode stability** | Excellent | Good | Good–Excellent |
| **Packet injection reliability** | Excellent | Good (occasional frame loss) | Good–Excellent |
| **USB 3.0 throughput** | Full speed | Near-full | Near-full |
| **Setup time** | High (dedicated hardware) | Low–Medium | Low–Medium |
| **Portability** | Low (dedicated machine) | High (snapshots, portability) | High |
| **Resource overhead** | None | Medium | Low–Medium |
| **CTF / lab use** | Overkill | Ideal | Ideal |
| **Professional engagements** | Recommended | Acceptable | Acceptable |

**Conclusion:** For CTF competitions, lab practice, and learning environments, a VM with proper USB passthrough is convenient and capable. For professional penetration testing engagements where reliability and forensic integrity matter, a dedicated Kali laptop or bare-metal install is the more dependable choice. The frame loss and occasional USB arbitration hiccups in VMs can affect the reliability of time-sensitive attacks like PMKID capture or deauthentication flooding.

---

## Troubleshooting Quick Reference

| Symptom | Most Likely Cause | Solution |
|---|---|---|
| `lsusb` shows nothing inside Kali | USB passthrough not configured | Add USB filter (VBox) or connect via Removable Devices (VMware) |
| "No USB devices" in VirtualBox USB settings | Extension Pack missing or version mismatch | Install matching Extension Pack |
| Adapter visible in `lsusb` but no `wlan` interface | Driver not loaded | `sudo modprobe 88XXau` or `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | DKMS package not installed | `sudo apt install realtek-rtl88xxau-dkms` |
| Interface appears then disappears | USB autosuspend or VBox xHCI arbitration | Disable autosuspend; try USB 2.0 controller for ACH |
| `airmon-ng` starts but monitor mode fails silently | Wrong driver or conflicting network manager | `sudo airmon-ng check kill`, then retry |
| VirtualBox USB filter does not capture on boot | Filter added before Extension Pack | Delete filter, install Extension Pack, re-add filter |
| VMware loses device during long sessions | VMware USB arbitrator service stops | Re-enable and set to auto-start |

---

{{< faq >}}

## Next Steps

With USB passthrough configured and monitor mode verified, you are ready to proceed:

- **Install or update the driver:** [ALFA Driver Install Guide for Kali & Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- **Full AWUS036ACH setup walkthrough:** [AWUS036ACH Kali Linux Setup Guide](/en/blog/awus036ach-kali-linux-setup/)
- **Hardware review of the AWUS036AXML:** [AWUS036AXML WiFi 6E Review](/en/blog/awus036axml-wifi-6e-review/)

If you are evaluating which adapter to buy for VM-based pentesting, the AWUS036ACH remains the most reliable choice due to its mature USB 2.0 passthrough behaviour and battle-tested driver. The AWUS036AXML is the better performer once everything is working, but requires more careful USB 3.0 configuration.

## References

1. [VirtualBox Official Downloads](https://www.virtualbox.org/wiki/Downloads)
2. [VMware Workstation Product Page](https://www.vmware.com/products/workstation-pro.html)
3. [aircrack-ng rtl8812au Driver Project](https://github.com/aircrack-ng/rtl8812au)
4. [ALFA Network Official Website](https://www.alfa.com.tw/)
5. [Kali Linux Official Documentation](https://www.kali.org/docs/)
